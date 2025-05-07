#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  1 11:28:09 2025

@author: trouve
"""

import torch
import time
from pykeops.torch import LazyTensor
from pykeops.torch import Vi, Vj
from matplotlib import pyplot as plt

        
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__} exécutée en {end_time - start_time:.6f} secondes")
        return result
    return wrapper


class DiffealModel:
    def __init__(self, d):
        self.d = d
        self.F = None # forward dynamic
        self.g = None # global loss
        self.kernel = None
        self.optimizer = None
        self.n_iter = None
       
        
    def set_loss(self, x_T, w_T, kernel = "gaussian", 
                 parameter_loss = None, lam=1):
        self.x_T, self.w_T, self.lam = x_T, w_T, lam
        if kernel == "gaussian":
            self.kernel = "gaussian"
            K = Make_GaussKernelSingle(parameter_loss,self.d)
            self.parameter_loss = parameter_loss
            self.g = global_loss(x_T,w_T, K, lam=lam)
            
 
    def set_dyn(self, sig, slam, smu, N):
        self.N = N
        self.dt = 1.0/N
        self.sig = sig
        self.slam = slam
        self.smu = smu
        self.F = make_F(sig, slam, smu, self.d)
    
        
    def forward(self):
        z0, apx, apN = self.z0, self.apx, self.apN
        z = []
        for zk0 in z0:
          z.append(zk0.clone())

        trajectory = [z]

        for i in range(self.N):
            px = apx[i,:,:]
            pN = apN[i,:,:]
            ai = [px,pN]
            new_z=[]
            for (zk,dzk) in zip(z,self.F(z, ai)):
                new_z.append(zk + self.dt * dzk)  # Mise à jour de z selon le schéma mid-point
            z = new_z
            trajectory.append(z)
        return trajectory
    
    def set_optimizer(self, z0, max_iter = 20):
        N, n, d  = self.N, z0[0].shape[0], self.d
        self.n = n
        self.apx = torch.zeros(N,n,d, requires_grad=True)
        self.apN = torch.zeros(N,n,d*d, requires_grad=True)
        self.z0 = z0
        self.max_iter = max_iter
        
        print("g(z0)", self.g(z0).detach().cpu().numpy())
        self.optimizer = torch.optim.LBFGS(
            [self.apx,self.apN], lr=1, max_iter=max_iter, line_search_fn='strong_wolfe')
        
        def closure():
            #print("entering closure")
            self.optimizer.zero_grad()
            traj = self.forward()
            loss = self.g(traj[-1])  # Fonction de coût
            #print('loss: ', loss.cpu().detach())
            loss.backward()  # Auto-différentiation
            return loss
        
        self.closure = closure  
    
    def optimize(self, n_iter=None):
        if n_iter is not None:
            self.n_iter = n_iter
        for i in range(self.n_iter):
            loss = self.optimizer.step(self.closure)
            print(f"Step {i+1}: , loss = {loss.item():.6f}")
            traj = self.forward()
            self.plot_final(traj)
            
    def plot_final(self, traj, cmap='coolwarm', Fplot='2d'):
    
      x = traj[-1][0].detach().cpu().numpy()
      w = (traj[-1][1]**2).detach().cpu().numpy()
      dx_T = self.x_T.detach().cpu().numpy()
      dw_T = self.w_T.detach().cpu().numpy()
      x0, w0 = self.z0[0].detach().cpu().numpy(), self.z0[1].detach().cpu().numpy()**2
      fig, axs = plt.subplots(1, 3, figsize=(10, 4))
      if Fplot=='2d':
        axs[0].scatter(x0[:,0], x0[:,1], s=5., c=w0, cmap=cmap)
        axs[1].scatter(x[:,0], x[:,1], s=5., c=w, cmap=cmap)
        axs[2].scatter(dx_T[:,0], dx_T[:,1], s=5., c=dw_T, cmap=cmap)
      elif Fplot=='3d':
        ax = plt.axes(projection='3d')
        ax.scatter3D(x[:,0], x[:,1], x[:,2], c=w, cmap=cmap)
      #ax.view_init(elev=0, azim=-90, roll=0)
      axs[0].set_aspect('equal', 'box')
      axs[1].set_aspect('equal', 'box')
      axs[2].set_aspect('equal', 'box')
      plt.show()

   

# Dynamique Diffeo-Elastique
def make_F(sig, slam, smu, d):
  # slam =sqrt(lam), smu = sqrt(mu)
  def F(z, a):
    #w=sw**2
    x, sw, e = z
    #print("F  a len", len(a))
    px, pN = a
    x_i = LazyTensor( x[:,None,:] )/sig
    x_j = LazyTensor( x[None,:,:] )/sig
    px_i = LazyTensor( px[:,None,:] )
    px_j = LazyTensor( px[None,:,:] )
    sw_i = LazyTensor( sw[:,None,:] )

    n = x.shape[0]

    I =  torch.ones(n,1)*torch.eye(d).flatten()[None,:]
    I_ij = LazyTensor(I[None,:,:])

    # Symetrisation of N
    N = pN.view(n,d,d)
    N = 0.5*(N+N.transpose(1,2)).view(n,d*d)
    N_i = LazyTensor(N[:,None,:])
    N_j = LazyTensor(N[None,:,:])

    Z_ij = (x_i - x_j)
    D2_ij = (Z_ij**2).sum(dim=2)
    G_ij = (- 0.5*D2_ij).exp()

        # first term of rhs in (8)
    hp_ij = (px_i*px_j).sum(dim=2)

    # second term
    hcross_ij= +2*N_j.matvecmult(px_i)*Z_ij/sig

    # third term
    ZZmI_ij = Z_ij.tensorprod(Z_ij)-I_ij
    NN_ji = N_j.keops_tensordot(N_i,[d,d],[d,d],[1],[0])
    htr_ij = -(NN_ji*ZZmI_ij).sum(dim=2)/sig**2

    if (True):
        Luu = ((G_ij*(hp_ij+ hcross_ij+ htr_ij)).sum(dim=1)).sum()
    else:
        Luu = ((G_ij*hp_ij).sum(dim=1)).sum()

 ## xiq(u)
    xiqx = (G_ij*(px_j - N_j.matvecmult(-Z_ij)/sig)).sum(dim=1) #
    xiqsw = 0.5*(G_ij*sw_i*(-(px_j*Z_ij).sum(dim=2)/sig
            -(N_j*ZZmI_ij).sum(dim=2)/sig**2)).sum(dim=1)

    ## Aq
    Aql = slam*sw.flatten()*xiqsw
    smwp_ij = LazyTensor((smu*sw.flatten())[:,None,None])*px_j
    Aqm = -(smwp_ij.tensorprod(Z_ij) + Z_ij.tensorprod(smwp_ij))/(2*sig)
    smwN_ij = LazyTensor((smu*sw.flatten())[:,None,None])*N_j
    Aqm += -(smwN_ij.keops_tensordot(ZZmI_ij,[d,d],[d,d],[1],[0])
      +ZZmI_ij.keops_tensordot(smwN_ij,[d,d],[d,d],[1],[0]))/(2*sig**2)
    ## Aqm
    Aqm = (G_ij*Aqm).sum(dim=1)
    AqAq = (Aql**2).sum() + (Aqm**2).sum()


    return [xiqx, xiqsw, 0.5* Luu + 0.5*AqAq]

  return F

def Make_GaussKernelSingle(sig,d):
    def GaussKernelSingle(x,y,u,v):
    # u and v are the feature vectors
       x_i = LazyTensor( x[:,None,:] )/sig
       y_j = LazyTensor( y[None,:,:] )/sig
       u_i = LazyTensor( u[:,None,:] )
       v_j = LazyTensor( v[None,:,:] )
       Z_ij = (x_i - y_j)
       D2_ij = (Z_ij**2).sum(dim=2)
       G_ij = (- 0.5*D2_ij).exp()
       K = G_ij * u_i * v_j
       return K.sum_reduction(axis=1)
    return GaussKernelSingle

# GaussLinKernel
def GaussLinKernel(sigma,d,l,beta):
    # u and v are the feature vectors
    x, y, u, v = Vi(0, d), Vj(1, d), Vi(2, l), Vj(3, l)
    D2 = x.sqdist(y)
    for sInd in range(len(sigma)):
        sig = sigma[sInd]
        K = (-D2 / (2.0*sig*sig)).exp() * (u * v).sum()
        if sInd == 0:
            retVal = beta[sInd]*K
        else:
            retVal += beta[sInd]*K
    return (retVal).sum_reduction(axis=1)


def lossVarifoldNorm(x_T,w_T,K):
    #print(w_T*zeta_T.cpu().numpy())
    cst = (K(x_T,x_T,w_T,w_T)).sum()
    print("cst is ")
    print(cst.detach().cpu().numpy())

    def loss(xw):
        x, w = xw
        k1 = K(x, x, w, w)
        k2 = K(x, x_T, w, w_T)

        return (
            (1.0/2.0)*(cst
            + k1.sum()
            - 2.0 * k2.sum())
        )

    return cst.detach().cpu().numpy(), loss

def global_loss(x_T,w_T,K, lam=1):
    cst, loss_var = lossVarifoldNorm(x_T,w_T,K)
    def loss(z):
      (x,sw,e) = z
      print('e=',e.detach().cpu().numpy())
      return e + lam*loss_var([x,sw**2])
    return loss


# def forwardbis(z0,apX,apN):
#     z = []
#     for zk0 in z0:
#       z.append(zk0.clone())

#     trajectory = [z]

#     for i in range(N):
#         #print('i=',i)
#         mid_z = []
#         px = apx[i,:,:]
#         pN = apN[i,:,:]
#         ai = [px,pN]
#         for (zk,dzk) in zip(z,F(z,ai)):
#             #print('dzd', dzk)
#             mid_z.append(zk + (dt / 2) * dzk)  # Calcul du mid-point
#         new_z=[]
#         for (zk,dzk) in zip(z,F(mid_z, ai)):
#             new_z.append(zk + dt * dzk)  # Mise à jour de z selon le schéma mid-point
#         z = new_z
#         trajectory.append(z)
#     return trajectory



