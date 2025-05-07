#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  1 11:30:21 2025

@author: trouve
"""
import torch

# %%
def experiment_a(L,m, scaling):
  # Construit une grille [_L,L]^2  de taille m*m
  Lx = torch.linspace(-L,L,m)
  Ly = torch.linspace(-L,L,m)
  xx, yy = torch.meshgrid(Lx, Ly, indexing='ij')
  x = torch.stack([xx, yy], dim=-1)  # (m, m, 2)
  # Aplati pour avoir un tableau de shape (m*m, 2)
  x = x.view(-1, 2)
  w = torch.ones(m**2,1)*(L/m)**2
  e = torch.zeros(1)
  z0 = [x,w.sqrt(),e]
  x_T = scaling*x.clone().detach()
  w_T = (scaling**2)*w.clone().detach()
  xw_T = [x_T,w_T]
  return [z0, xw_T]

def  openspan(X,y0,alpha):
    x, y  = X[:,0], X[:,1]
    th = torch.atan(x/y0)
    nx = y*(alpha*th).sin()
    ny = y*(alpha*th).cos()
    jac = alpha*y/(y0*(1+th**2))
    return (torch.stack([nx,ny], dim=-1),jac)

def experiment_b(L,m, scaling):
  # Construit une grille [_L,L]^2  de taille m*m
  Lx = torch.linspace(-L,L,m)
  Ly = torch.linspace(3*L,5*L,m)
  xx, yy = torch.meshgrid(Lx, Ly, indexing='ij')
  x = torch.stack([xx, yy], dim=-1)  # (m, m, 2)
  # Aplati pour avoir un tableau de shape (m*m, 2)
  x = x.view(-1, 2)
  w = torch.ones(m**2,1)*(L/m)**2
  e = torch.zeros(1)
  z0 = [x,w.sqrt(),e]
  [x_T, jac]= openspan(scaling*x.clone().detach(),scaling*3*L, 1)
  w_T = ((scaling**2)*jac[:,None]*w).clone().detach()
  xw_T = [x_T,w_T]
  return [z0, xw_T]

def experiment_c(L,m):
  # Construit une grille [_L,L]^2  de taille m*m
  Holes_S = [(0.5,0.2, 0.3), (-0.5,0.3,0.2), (0,-0.5,0.3) ]
  Holes_T = [(0.6,0.2, 0.3), (-0.3,0.3,0.4), (0,-0.5,0.2)]
  Lx = torch.linspace(-L,L,m)
  Ly = torch.linspace(-L,L,m)
  xx, yy = torch.meshgrid(Lx, Ly, indexing='ij')
  x = torch.stack([xx, yy], dim=-1)  # (m, m, 2)
  # Aplati pour avoir un tableau de shape (m*m, 2)
  x = x.view(-1, 2)
  w = torch.ones(m**2,1)*(L/m)**2
  x_T = x.clone().detach()
  w_T = w.clone().detach()
  for (a,b,r) in Holes_S:
      w[((x[:,0]-a)**2+(x[:,1]-b)**2)<=r**2,:]=0.1*(L/m)**2
  for (a,b,r) in Holes_T:
      w_T[((x_T[:,0]-a)**2+(x_T[:,1]-b)**2)<=r**2,:]=0.1*(L/m)**2
  e = torch.zeros(1)
  z0 = [x,w.sqrt(),e]
  xw_T = [x_T,w_T]
  return [z0, xw_T]

def experiment_d(L,m):
  # Construit une grille [_L,L]^2  de taille m*m
  Holes_S = [(0.5,0.2, 0.3), (-0.5,0.3,0.2), (0,-0.5,0.3) ]
  Holes_T = [(0.6,0.2, 0.3), (-0.3,0.3,0.4), (0.2,-0.3,0.2)]
  Lx = torch.linspace(-L,L,m)
  Ly = torch.linspace(-L,L,m)
  xx, yy = torch.meshgrid(Lx, Ly, indexing='ij')
  x = torch.stack([xx, yy], dim=-1)  # (m, m, 2)
  # Aplati pour avoir un tableau de shape (m*m, 2)
  x = x.view(-1, 2)
  w = torch.ones(m**2,1)*(L/m)**2
  x_T = x.clone().detach()
  w_T = w.clone().detach()
  for (a,b,r) in Holes_S:
      w[((x[:,0]-a)**2+(x[:,1]-b)**2)<=r**2,:]=0.1*(L/m)**2
  for (a,b,r) in Holes_T:
      w_T[((x_T[:,0]-a)**2+(x_T[:,1]-b)**2)<=r**2,:]=0.1*(L/m)**2
  e = torch.zeros(1)
  z0 = [x,w.sqrt(),e]
  xw_T = [x_T,w_T]
  return [z0, xw_T]

def experiment_e(L,m):
  # Construit une grille [_L,L]^2  de taille m*m
  Holes_S = [(0.4,0.2, 0.15), (-0.5,0.3,0.2), (0,-0.5,0.3) ]
  Holes_T = [(0.6,0.2, 0.3), (-0.3,0.3,0.4), (0.2,-0.3,0.2)]
  Lx = torch.linspace(-L,L,m)
  Ly = torch.linspace(-L,L,m)
  xx, yy = torch.meshgrid(Lx, Ly, indexing='ij')
  x = torch.stack([xx, yy], dim=-1)  # (m, m, 2)
  # Aplati pour avoir un tableau de shape (m*m, 2)
  x = x.view(-1, 2)
  w = torch.ones(m**2,1)*(L/m)**2
  x_T = x.clone().detach()
  w_T = w.clone().detach()
  for (a,b,r) in Holes_S:
      w[((x[:,0]-a)**2+(x[:,1]-b)**2)<=r**2,:]=0.1*(L/m)**2
  for (a,b,r) in Holes_T:
      w_T[((x_T[:,0]-a)**2+(x_T[:,1]-b)**2)<=r**2,:]=0.1*(L/m)**2
  e = torch.zeros(1)
  z0 = [x,w.sqrt(),e]
  xw_T = [x_T,w_T]
  return [z0, xw_T]

