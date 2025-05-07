import numpy as np
from typing import Callable
from scipy.special import roots_legendre
from numpy.polynomial.legendre import leggauss
import multiprocessing as mp
from numba import jit, prange


def grad_adaptive(f:Callable,x,h=1e-5):
    """
    Compute the gradient of a function f at point x using an adaptive step size and Richardson extrapolation.

    Parameters:
    f : callable
        The function for which to compute the gradient.
    x : np.ndarray
        The point at which to compute the gradient.
    h : float, optional
        The step size for finite difference approximation (default is 1e-5).

    Returns: list
        The gradient of f at point x.
    """
    n = len(x)
    grad = []
    
    for i in range(n):
        step = np.zeros_like(x)
        step[i] = h
        D1 = ( -f(x+2*step) + 8*f(x+step) - 8*f(x-step) + f(x-2*step) ) / (12*h)
        D2 = (-f(x+step) + 8*f(x+step/2) - 8*f(x-step/2) + f(x-step)) / (12*(h/2))
        grad.append((4*D2 - D1) / 3)
    
    return grad

def Integral_Gauss_Legender_parallel(fun:Callable,k_min,k_max,n=50,num_processes=4):
    """
    Compute the integral of a function using the Gauss-Legendre method with parallel processing.
    Parameters:
    fun : callable
        The function to integrate.
    k_min : float
        The lower limit of integration.
    k_max : float
        The upper limit of integration.
    n : int, optional
        The number of points for Gauss-Legendre quadrature (default is 50).
    num_processes : int, optional
        The number of parallel processes to use (default is 4).
    """
    
    @jit(nopython=True, parallel=True)
    def integrate_1d_numba(f_vals, w_mapped):
        """使用 JIT 加速 1D Gauss-Legendre 积分"""
        integral = 0.0
        for i in prange(len(f_vals)):  # 并行计算积分
            integral += w_mapped[i] * f_vals[i]
        return integral

    def integrate_1d(fun, k_min, k_max, n=50):
        """计算 1D Gauss-Legendre 积分"""
        x, w = roots_legendre(n)  # 预计算 Gauss-Legendre 节点和权重
        x_mapped = 0.5 * (k_max - k_min) * x + 0.5 * (k_max + k_min)
        w_mapped = 0.5 * (k_max - k_min) * w

        f_vals = np.array([fun(xi) for xi in x_mapped])  # 计算函数值
        return integrate_1d_numba(f_vals, w_mapped)  # 用 numba 加速加权求和

    @jit(nopython=True, parallel=True)
    def integrate_2d_numba(f_vals, w_mapped):
        """使用 JIT 加速 2D Gauss-Legendre 积分"""
        integral = 0.0
        for i in prange(f_vals.shape[0]):
            for j in prange(f_vals.shape[1]):
                integral += w_mapped[i, j] * f_vals[i, j]
        return integral

    def integrate_2d(fun, x_min, x_max, y_min, y_max, n=50):
        """计算 2D Gauss-Legendre 积分"""
        x, w_x = roots_legendre(n)
        y, w_y = roots_legendre(n)

        x_mapped = 0.5 * (x_max - x_min) * x + 0.5 * (x_max + x_min)
        y_mapped = 0.5 * (y_max - y_min) * y + 0.5 * (y_max + y_min)

        wx, wy = np.meshgrid(w_x, w_y, indexing='ij')  # 计算权重矩阵
        w_mapped = 0.25 * (x_max - x_min) * (y_max - y_min) * wx * wy

        f_vals = np.array([[fun(xi, yj) for yj in y_mapped] for xi in x_mapped])  # 计算函数值
        return integrate_2d_numba(f_vals, w_mapped)

    @jit(nopython=True, parallel=True)
    def integrate_3d_numba(f_vals, w_mapped):
        """使用 JIT 加速 3D Gauss-Legendre 积分"""
        integral = 0.0
        for i in prange(f_vals.shape[0]):
            for j in prange(f_vals.shape[1]):
                for k in prange(f_vals.shape[2]):
                    integral += w_mapped[i, j, k] * f_vals[i, j, k]
        return integral

    def integrate_3d(fun, x_min, x_max, y_min, y_max, z_min, z_max, n=30):
        """计算 3D Gauss-Legendre 积分"""
        x, w_x = roots_legendre(n)
        y, w_y = roots_legendre(n)
        z, w_z = roots_legendre(n)

        x_mapped = 0.5 * (x_max - x_min) * x + 0.5 * (x_max + x_min)
        y_mapped = 0.5 * (y_max - y_min) * y + 0.5 * (y_max + y_min)
        z_mapped = 0.5 * (z_max - z_min) * z + 0.5 * (z_max + z_min)

        wx, wy, wz = np.meshgrid(w_x, w_y, w_z, indexing='ij')
        w_mapped = (1/8) * (x_max - x_min) * (y_max - y_min) * (z_max - z_min) * wx * wy * wz

        f_vals = np.array([[[fun(xi, yj, zk) for zk in z_mapped] for yj in y_mapped] for xi in x_mapped])  # 计算函数值
        return integrate_3d_numba(f_vals, w_mapped)

    if isinstance(k_min, (int, float)) and isinstance(k_max, (int, float)):  # 1D
        return integrate_1d(fun, k_min, k_max, n)
    elif isinstance(k_min, tuple) and isinstance(k_max, tuple) and len(k_min) == 2 and len(k_max) == 2:  # 2D
        return integrate_2d(fun, k_min[0], k_max[0], k_min[1], k_max[1],n)
    elif isinstance(k_min, tuple) and isinstance(k_max, tuple) and len(k_min) == 3 and len(k_max) == 3:  # 3D
        return integrate_3d(fun, k_min[0], k_max[0], k_min[1], k_max[1], k_min[2], k_max[2], n)
    else:
        raise ValueError("Invalid dimension for integral bounds.")

def gauss_legendre_adaptive(fun, k_min, k_max, tol=1e-4, n=50, depth=0, max_depth=10):
    """
    自适应 1D Gauss-Legendre 积分
    """
    x, w = roots_legendre(n)
    x_mapped = 0.5 * (k_max - k_min) * x + 0.5 * (k_max + k_min)
    w_mapped = 0.5 * (k_max - k_min) * w
    f_vals = np.array([fun(xi) for xi in x_mapped])
    integral = np.dot(w_mapped, f_vals)
    
    # 细分左右区间
    mid = 0.5 * (k_min + k_max)
    left_integral = gauss_legendre_adaptive(fun, k_min, mid, tol, n, depth+1, max_depth) if depth < max_depth else 0
    right_integral = gauss_legendre_adaptive(fun, mid, k_max, tol, n, depth+1, max_depth) if depth < max_depth else 0
    
    return left_integral + right_integral if abs(left_integral + right_integral - integral) > tol else integral

def gauss_legendre_adaptive_2d(fun, x_min, x_max, y_min, y_max, tol=1e-6, n=20):
    """
    自适应 2D Gauss-Legendre 积分
    """
    def integrate_1d(y):
        return gauss_legendre_adaptive(lambda x: fun(x, y), x_min, x_max, tol, n)
    
    return gauss_legendre_adaptive(integrate_1d, y_min, y_max, tol, n)

def gauss_legendre_adaptive_3d(fun, x_min, x_max, y_min, y_max, z_min, z_max, tol=1e-6, n=10):
    """
    自适应 3D Gauss-Legendre 积分
    """
    def integrate_2d(z):
        return gauss_legendre_adaptive_2d(lambda x, y: fun(x, y, z), x_min, x_max, y_min, y_max, tol, n)
    
    return gauss_legendre_adaptive(integrate_2d, z_min, z_max, tol, n)