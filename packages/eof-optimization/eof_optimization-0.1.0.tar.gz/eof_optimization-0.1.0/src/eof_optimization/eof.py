import torch

from typing import Union, Optional
from qutip import Qobj
from math import sqrt
import numpy as np

class EoF:
    def __init__(self,
                 DM: Qobj,
                 M: int,
                 return_torch_tensors:Optional[bool] =False,
                 device:Optional[Union[str, torch.device]] = 'cpu',
                 dims_sys=None,
                 dtype:Optional[torch.dtype]=torch.float64
                 ):
        """
        Inicializa la clase para calcular el EoF con PyTorch.
        Args:
            DM (qutip.Qobj): Matriz de densidad.
            echo (bool): Indica si se imprimirán los tiempos de ejecución.
            echo_tangle (bool): Indica si se imprimirá el valor del tangle.
            return_torch_tensors (bool): Indica si se retornarán los valores como tensores de PyTorch.
            tangle (bool): Indica si se calculará el tangle, en caso contrario se calculará la entropía de von Neumann.
            device (torch.device): Dispositivo donde se realizarán los cálculos.
            dims_sys (list): Dimensiones de los subsistemas A y B.
            M (int):
        """
        
        self.device = device
        
        
        def extract_eigs_as_torch_tensor(DM):
            Eig = DM.eigenstates()
            return torch.tensor(Eig[0].real, dtype=torch.complex128, device=self.device), torch.tensor( # this is not the problem
                [[b[0] for b in a.data.to_array()] for a in Eig[1]], dtype=torch.complex128, device=self.device
            )
        
        self.P, self.ST = extract_eigs_as_torch_tensor(DM)

        if dims_sys is None:
            dim = int(sqrt(len(self.P)))
            dims_sys = [dim,dim]
        
        self.dim_sys_A = dims_sys[0]
        self.dim_sys_B = dims_sys[1]

        if M < len(self.P):
            raise ValueError("M no puede ser menor a N")

        self.M = M
        
        self.dtype = dtype
        self.return_torch_tensors = return_torch_tensors

    def dagger(self, A: torch.Tensor) -> torch.Tensor:
        """
        Calcula la adjunta transpuesta de un tensor.
        Args:
            A (torch.Tensor): Tensor a calcular la adjunta transpuesta.
        Returns:
            torch.Tensor: Adjunta transpuesta de A.
        """
        
        return A.conj().permute(*torch.arange(A.ndim - 1, -1, -1))

    def partial_trace(self, rho: torch.Tensor) -> torch.Tensor:
        """
        Realiza el trazo parcial sobre el subsistema B.
        Args:
            rho (torch.Tensor): Matriz de densidad conjunta (AB).
        Returns:
            torch.Tensor: Matriz de densidad reducida sobre el subsistema A.
        """
        
        dim_A = self.dim_sys_A
        dim_B = self.dim_sys_B
        reshaped_rho = rho.reshape(dim_A, dim_B, dim_A, dim_B)
        return torch.einsum('ijik->jk', reshaped_rho)
    
    
    def metric_tangle(self, rho_Aj: torch.Tensor) -> torch.Tensor:
        """
        Calcula el tangle de un estado cuántico.
        Args:
            rho_Aj (torch.Tensor): Matriz de densidad.
        Returns:
            torch.Tensor: Tangle del estado cuántico.
        """
        
        return torch.trace(torch.matmul(rho_Aj, rho_Aj))
    
    def metric_entanglement(self, rho_Aj: torch.Tensor) -> torch.Tensor:
        """
        Calcula la entropía de von Neumann de un estado cuántico.
        Args:
            rho_Aj (torch.Tensor): Matriz de densidad.
        Returns:
            torch.Tensor: Entropía de von Neumann del estado cuántico.
        """
        
        eigvals = torch.linalg.eigvalsh(rho_Aj)
        eigvals = eigvals[eigvals > 1e-12]
        entropy = -torch.sum(eigvals * torch.log2(eigvals))
        return entropy


    def EoF_PyTorch(self, Ang: torch.Tensor) -> torch.Tensor:
        """
        Calcula el EoF de un estado cuántico.
        Args:
            Ang (torch.Tensor): Arreglo de ángulos. Deben ser valores entre 0 y 1.
        Returns:
            torch.Tensor: EoF del estado cuántico.
        """
        d = int(len(self.P))
        
        As = torch.stack([
            torch.exp(1j * 2 * torch.pi * Ang[1]) * torch.sin(2 * torch.pi * Ang[0]),
            torch.exp(1j * 2 * torch.pi * Ang[2]) * torch.cos(2 * torch.pi * Ang[0]),
            (torch.exp(1j * 2 * torch.pi * Ang[2]) * torch.cos(2 * torch.pi * Ang[0])).conj(),
            -(torch.exp(1j * 2 * torch.pi * Ang[1]) * torch.sin(2 * torch.pi * Ang[0])).conj()
        ])
        
        U = torch.eye(self.M, dtype=torch.complex128, device=self.device)

        i = 0
        for k1 in range(self.M-1):
            for k2 in range(1, self.M-k1):
                
                x1 = k1
                x2 = k1 + k2
                
                U_temp = U.clone()
                
                if x1 == x2:
                    U_temp[:, x2] = U[:, x2] * As[3, i]
                else:
                    temp1 = U[:, x1] * As[0, i] + U[:, x2] * As[1, i]
                    temp2 = U[:, x1] * As[2, i] + U[:, x2] * As[3, i]
                    U_temp[:, x1] = temp1
                    U_temp[:, x2] = temp2
                #assert torch.max(torch.abs(torch.matmul(U_temp,U_temp.T.conj()) - 
                #torch.eye(d, dtype=torch.complex128, device=self.device))) < 1e-9,
                # "La matriz U_temp no es unitaria"
                U = U_temp
                i += 1

        sqrtP = torch.sqrt(self.P)
        U_trimmed = U[:, :d]
        weighted_U = sqrtP * U_trimmed
        STauxs = weighted_U @ self.ST
        E = 0
        acum = torch.zeros(d, dtype=torch.complex128, device=self.device)
        for k1 in range(self.M):
            STaux = STauxs[k1]
            DMt = torch.outer(STaux, self.dagger(STaux))
            acum = torch.add(acum, DMt)
            p_j = torch.trace(DMt).real
            trace_rho_Aj = torch.tensor(0.0, dtype=torch.float64, device=self.device)
            
            if p_j > 1e-9:
                DMt /= p_j
                rho_Aj = self.partial_trace(DMt)
                trace_rho_Aj = self.metric_entanglement(rho_Aj)
            E += torch.real(p_j * trace_rho_Aj)
        return E
        

    def Phi(self, Ang: Union[np.ndarray, torch.Tensor]) -> Union[np.ndarray, torch.Tensor]:
        """
        Calcula el valor de Phi para un conjunto de ángulos.
        
        Args:
            Ang (np.ndarray o torch.Tensor): Arreglo de ángulos.
        
        Returns:
            np.ndarray o torch.Tensor: Valor de Phi.
        """
        
        if not isinstance(Ang, torch.Tensor):
            Ang = torch.tensor(Ang, dtype=torch.complex128, device=self.device)
        Ang = Ang.reshape(3, -1)

        if self.return_torch_tensors:
            return self.EoF_PyTorch(Ang)
        return self.EoF_PyTorch(Ang).detach().cpu().numpy()
    
    def PhiGradPhi(self, Ang: Union[np.ndarray, torch.Tensor]) -> Union[
        tuple[torch.Tensor, torch.Tensor], 
        tuple[np.ndarray, np.ndarray]
    ]:
        """
        Calcula el gradiente de Phi con respecto a Ang usando el autograd de PyTorch.
        
        Args:
            Ang (np.ndarray o torch.Tensor): Arreglo de ángulos.
            
        Returns:
            np.ndarray: Valor de Phi.
            np.ndarray: Gradiente de Phi.
        """
        if not isinstance(Ang, torch.Tensor):
            Ang = torch.tensor(Ang, dtype=torch.complex128, device=self.device)
        Ang = Ang.reshape(3, -1)
        
        Ang = Ang.clone().detach().requires_grad_(True)
        
        phi_value = self.EoF_PyTorch(Ang)
        
        phi_value.backward()
        gradient = Ang.grad
        
        if self.return_torch_tensors:
            return phi_value.detach(), gradient.detach().flatten()
        
        phi_value_np = phi_value.detach().cpu().numpy()
        gradient_np = gradient.detach().flatten().cpu().numpy()
        
        return phi_value_np, gradient_np