import torch
import numpy as np
from torch.func import vmap
import math

class HistoryBuffer:
    def __init__(self, device, dtype, initial_capacity=1024):
        # buffer de forma [capacidad, 2] para (f_e, f_best)
        self.device = torch.device(device)
        self.dtype = dtype
        self.capacity = initial_capacity
        self.size = 0
        self.buffer = torch.zeros(self.capacity, 2,
                                  device=self.device,
                                  dtype=self.dtype)

    def append(self, fe: float, f: float):
        # si ya no cabe, duplicamos la capacidad
        if self.size >= self.capacity:
            self._grow()
        # escribimos en la fila 'size'
        self.buffer[self.size, 0] = fe
        self.buffer[self.size, 1] = f
        self.size += 1

    def _grow(self):
        new_cap = self.capacity * 2
        new_buf = torch.zeros(new_cap, 2,
                              device=self.device,
                              dtype=self.dtype)
        # copiamos lo que ya teníamos
        new_buf[:self.capacity] = self.buffer
        self.buffer = new_buf
        self.capacity = new_cap

    def get_tensor(self) -> torch.Tensor:
        # devuelve sólo las filas usadas
        return self.buffer[:self.size]

    def to_numpy(self) -> 'np.ndarray':
        return self.get_tensor().cpu().numpy()

class FitnessHistory:
    def __init__(self, device, dtype, n):
        self.device = torch.device(device)
        self.dtype = dtype
        self.n = n
        self.buffer = torch.zeros(self.n, device=self.device, dtype=self.dtype)
        self.last = -1  # aún no hay valores insertados
        self.count = 0  # número real de valores insertados (máximo n)

    def full(self):
        return self.count == self.n

    def append(self, new_val):
        self.last = (self.last + 1) % self.n
        self.buffer[self.last] = new_val
        if self.count < self.n:
            self.count += 1

    def ObtainLast(self):
        if self.count == 0:
            raise ValueError("No hay valores en el historial.")
        return self.buffer[self.last]

    def ObtainMinusN(self):
        if not self.full():
            raise ValueError("El buffer aún no está lleno.")
        idx = (self.last + 1) % self.n  # índice más antiguo en el buffer
        return self.buffer[idx]

def slr_es(f, n, bounds=None, max_iter=int(1e10), min_obj=None,
                   max_f_e=None, device='cpu', batch=False,
                   dtype=torch.float64, lambd=None, mu=None,
                   c_sigma=None, q_star=None, d_sigma=None,
                   c=None, c_1=None, T=None, alpha0=None,
                   alpha1=None, alpha2=None, m_0=0.0,
                   sigma=None, mu_eff=None
                  ):
    
    lower = None
    upper = None
    if bounds is not None:
        lu = list(zip(*bounds))
        lower = torch.tensor(lu[0], device=device, dtype=dtype)
        upper = torch.tensor(lu[1], device=device, dtype=dtype)

        if (torch.any(torch.isinf(lower)) or torch.any(torch.isinf(upper)) or torch.any(
                torch.isnan(lower)) or torch.any(torch.isnan(upper))):
            raise ValueError('Some bounds values are inf values or nan values')
        # Checking that bounds are consistent
        if not torch.all(lower < upper):
            raise ValueError('Bounds are not consistent min < max')
        # Checking that bounds are the same length
        if not len(lower) == len(upper):
            raise ValueError('Bounds do not have the same dimensions')

    if lambd is None:
        lambd = int(4 + 3 * math.log(n))
    if mu is None:
        mu = lambd // 2

    i_arange = torch.arange(1, mu + 1, device=device, dtype=dtype)
    scalar = torch.tensor(mu + 0.5, device=device, dtype=dtype)
    weights = torch.log(scalar) - torch.log(i_arange)
    weights /= torch.sum(weights)  # normalizamos para que sumen 1
    
    if mu_eff is None:
        mu_eff = (1.0 / torch.sum(weights**2)).item()

    if c_sigma is None:
        c_sigma = 0.3
        
    if q_star is None:
        q_star = 0.3
        
    if d_sigma is None:
        d_sigma = 1.0

    if c is None:
        c = mu_eff / (n + 2 * mu_eff)

    if c_1 is None:
        c_1 = 1.0 / (3.0 * math.sqrt(n) + 5.0)

    if T is None:
        T = int(mu_eff / c)

    memory_size = lambd

    if alpha0 is None:
        alpha0 = 1.0 - c_1

    if alpha1 is None:
        alpha1 = math.sqrt(c_1)

    if alpha2 is None:
        alpha2 = math.sqrt(c_1 * (1.0 - c_1))    

    # Estado interno
    m = torch.randn(n, device=device, dtype=dtype) + m_0
    
    if sigma is None:
        sigma = 0.3
        
    D = torch.ones(n, device=device, dtype=dtype)
    p_c = torch.zeros(n, device=device, dtype=dtype)
    s_sigma = q_star
    V = torch.zeros((memory_size, n), device=device, dtype=dtype)

    t = 0
    prev_f = None

    f_best = float('inf')
    best_overall = None
    #history = []

    history = HistoryBuffer(device='cpu', dtype=dtype)
    
    fe_count = 0
    stop_reason = None
    t = 0
    for _ in range(max_iter):
        Z = torch.randn((lambd, n), device=device, dtype=dtype)
        R = torch.randn((2, lambd), device=device, dtype=dtype)
        Y = (alpha0 * Z * D.unsqueeze(0)
             + alpha1 * R[0].unsqueeze(1) * p_c.unsqueeze(0)
             + alpha2 * R[1].unsqueeze(1) * V)
        X = m.unsqueeze(0) + sigma * Y
        if bounds is not None:
            X = torch.clamp(X, min=lower, max=upper)
        
        if batch:
            fitness = f(X)
        else:
            fitness = vmap(f)(X)

        fitness, idx = torch.topk(fitness, mu, largest=False)
        X = X[idx]
        fe_count += lambd

        m_new = torch.sum(X * weights.unsqueeze(1), dim=0)
        diff = m_new - m
        p_c = (1.0 - c) * p_c + math.sqrt(c * (2.0 - c) * mu_eff) * diff / sigma

        u = p_c / D
        D = torch.sqrt((1.0 - c_1) * D**2 + c_1 * u**2)

        if t % T == 0:
            V[:-1] = V[1:].clone()
            V[-1] = p_c.clone()
        
        if prev_f is not None:
            cmp_curr = prev_f.unsqueeze(0) <= fitness.unsqueeze(1)
            R_curr = torch.sum(cmp_curr, dim=1)
            cmp_prev = fitness.unsqueeze(0) <= prev_f.unsqueeze(1)
            R_prev = torch.sum(cmp_prev, dim=1)
            q = (weights * (R_prev - R_curr)).sum().item() / mu
            s_sigma = (1.0 - c_sigma) * s_sigma + c_sigma * (q - q_star)
            sigma *= math.exp(s_sigma / d_sigma)

        m = m_new
        prev_f = fitness.clone()

        curr_f0 = fitness[0].item()
        if curr_f0 < f_best:
            f_best = curr_f0
            best_overall = X[0].clone()
        
        t += 1
        
        history.append(fe_count, curr_f0)

        if min_obj is not None and torch.abs(f_best <= min_obj):
            stop_reason = "min founded"
            break
        
        if max_f_e is not None and fe_count >= max_f_e:
            stop_reason = "max FE reached"
            break

    if t >= max_iter:
        stop_reason = "max it reached"
    
    return {
        "x": best_overall.cpu().numpy(),
        "f": f_best,
        "it": t,
        "amount_f_e": fe_count,
        "history": history.to_numpy(),
        "stop_reason": stop_reason
    }

def slr_es_multimodal(f, n, bounds=None, max_iter=int(1e10), min_obj=None,
                   max_f_e=None, device='cpu', batch=False,
                   dtype=torch.float64, lambd=None, mu=None,
                   c_sigma=None, q_star=None, d_sigma=None,
                   c=None, c_1=None, T=None, alpha0=None,
                   alpha1=None, alpha2=None, m_0=0.0,
                   sigma=None, mu_eff=None, epsilon1=1e-12,
                    epsilon2=1e-12, epsilon3=1e-6, max_restarts=10,
                    callback_local_min=None, callback_save_progress=None
                        ):
    lower = None
    upper = None
    if bounds is not None:
        lu = list(zip(*bounds))
        lower = torch.tensor(lu[0], device=device, dtype=dtype)
        upper = torch.tensor(lu[1], device=device, dtype=dtype)

        if (torch.any(torch.isinf(lower)) or torch.any(torch.isinf(upper)) or torch.any(
                torch.isnan(lower)) or torch.any(torch.isnan(upper))):
            raise ValueError('Some bounds values are inf values or nan values')
        # Checking that bounds are consistent
        if not torch.all(lower < upper):
            raise ValueError('Bounds are not consistent min < max')
        # Checking that bounds are the same length
        if not len(lower) == len(upper):
            raise ValueError('Bounds do not have the same dimensions')

    lambda_0 = None
    if lambd is None:
        lambda_0 = int(4 + 3 * math.log(n))
    else:
        lambda_0 = lambd

    if d_sigma is None:
        d_sigma_0 = 0.1
    else:
        d_sigma_0 = d_sigma

    t_overall = 0

    best_overall = None
    f_best = float('inf')
    history = HistoryBuffer(device='cpu', dtype=dtype)
    fe_count = 0
    stop_reason = None
    restart = 0
    
    need_to_stop = False
    while (not need_to_stop) and restart < max_restarts:
        
        lambd = min(n, 2 ** restart * lambda_0)
        d_sigma = min(n / 2, 2 ** restart * d_sigma_0)

        if mu is None:
            mu = lambd // 2
    
        i_arange = torch.arange(1, mu + 1, device=device, dtype=dtype)
        scalar = torch.tensor(mu + 0.5, device=device, dtype=dtype)
        weights = torch.log(scalar) - torch.log(i_arange)
        weights /= torch.sum(weights)  # normalizamos para que sumen 1
        
        if mu_eff is None:
            mu_eff = (1.0 / torch.sum(weights**2)).item()
    
        if c_sigma is None:
            c_sigma = 0.3
            
        if q_star is None:
            q_star = 0.3
            
        if d_sigma is None:
            d_sigma = 0.1
    
        if c is None:
            c = mu_eff / (n + 2 * mu_eff)
    
        if c_1 is None:
            c_1 = 1.0 / (3.0 * math.sqrt(n) + 5.0)
    
        if T is None:
            T = int(mu_eff / c)
        memory_size = lambd
    
        if alpha0 is None:
            alpha0 = 1.0 - c_1
    
        if alpha1 is None:
            alpha1 = math.sqrt(c_1)
    
        if alpha2 is None:
            alpha2 = math.sqrt(c_1 * (1.0 - c_1))

        m = torch.randn(n, device=device, dtype=dtype) + m_0
        
        if sigma is None:
            sigma = 0.3
            
        D = torch.ones(n, device=device, dtype=dtype)
        p_c = torch.zeros(n, device=device, dtype=dtype)
        s_sigma = q_star
        V = torch.zeros((memory_size, n), device=device, dtype=dtype)
        
        prev_f = None
        fitness_history = FitnessHistory('cpu', dtype, n)
    
        t = 0
        for it in range(max_iter):
            #Z = torch.randn((lambd, n), device=device, dtype=dtype)
            Z = (torch.rand((lambd, n), device=device, dtype=dtype)*2)-1
            R = torch.randn((2, lambd), device=device, dtype=dtype)
            Y = (alpha0 * Z * D.unsqueeze(0)
                 + alpha1 * R[0].unsqueeze(1) * p_c.unsqueeze(0)
                 + alpha2 * R[1].unsqueeze(1) * V)
            X = m.unsqueeze(0) + sigma * Y
            #X = torch.clamp(X, min=lower, max=upper)
            
            if batch:
                fitness = f(X)
            else:
                fitness = torch.tensor([f(x) for x in X], device=device, dtype=dtype)
    
            fitness, idx = torch.topk(fitness, mu, largest=False)
            X = X[idx]
            fe_count += lambd
                
            m_new = torch.sum(X * weights.unsqueeze(1), dim=0)
            diff = m_new - m
            p_c = (1.0 - c) * p_c + math.sqrt(c * (2.0 - c) * mu_eff) * diff / sigma
    
            u = p_c / D
            D = torch.sqrt((1.0 - c_1) * D**2 + c_1 * u**2)

            if t % T == 0:
                V[:-1] = V[1:].clone()
                V[-1] = p_c.clone()
            
            if prev_f is not None:
                cmp_curr = prev_f.unsqueeze(0) <= fitness.unsqueeze(1)
                R_curr = torch.sum(cmp_curr, dim=1)
                cmp_prev = fitness.unsqueeze(0) <= prev_f.unsqueeze(1)
                R_prev = torch.sum(cmp_prev, dim=1)
                q = (weights * (R_prev - R_curr)).sum().item() / mu
                s_sigma = (1.0 - c_sigma) * s_sigma + c_sigma * (q - q_star)
                sigma *= math.exp(s_sigma / d_sigma)

            m = m_new
            prev_f = fitness.clone()
    
            curr_f0 = fitness[0].item()
            if curr_f0 < f_best:
                f_best = curr_f0
                best_overall = X[0].clone()
            
            t += 1
            t_overall += 1
            
            
            history.append(fe_count, curr_f0)

            fitness_history.append(fitness[0])

            if sigma < epsilon1:
                break

            if fitness_history.full():

                diff = torch.abs(fitness_history.ObtainLast() - fitness_history.ObtainMinusN())

                if diff < epsilon2:
                    break

                rel_improvement = diff / torch.abs(fitness_history.ObtainMinusN())
                if rel_improvement < epsilon3:
                    break

            if max_f_e is not None and max_f_e <= fe_count:
                stop_reason = "max FE reached"
                need_to_stop = True
                break

            if max_iter <= t_overall:
                stop_reason = "max it reached"
                need_to_stop = True
                break
                
            if min_obj is not None and f_best <= min_obj:
                stop_reason = "min founded"
                need_to_stop = True
                break

        if callback_local_min is not None:
            if callback_local_min(best_overall.cpu().numpy(), f_best):
                stop_reason = "callback end optimization"
                need_to_stop = True
                break

        if callback_save_progress is not None:
            data_to_save = {
                "x": best_overall.cpu().numpy(),
                "f": f_best,
                "it": t_overall,
                "amount_f_e": fe_count,
                "history": history.to_numpy(),
                "stop_reason": stop_reason
            }
            callback_save_progress(data_to_save)

        restart += 1

    return {
        "x": best_overall.cpu().numpy(),
        "f": f_best,
        "it": t_overall,
        "amount_f_e": fe_count,
        "history": history.to_numpy(),
        "stop_reason": stop_reason
    }


