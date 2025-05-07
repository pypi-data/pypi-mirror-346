import numpy as np
from typing import Callable
from .Function import grad_adaptive
from functools import lru_cache

class QuantumGeometry:
    def __init__(self,hamiltonian:Callable):
        """
        Initialize with a hamiltonian, kpoints and band indices.

        Parameters:
        hamiltonian : function handle
            A function that takes a kpoint as input and returns the Hamiltonian matrix.
        kpoints : np.ndarray
            An array of kpoints.
        band_indices : list[int] default=None
        """
        self.hamiltonian = hamiltonian
        # self.band_indices = band_indices
        # self.kpoints = kpoints

    # @lru_cache(maxsize=1000)
    def get_energy_band(self,kpoint):
        """
        Compute the energy and wave-function at a given kpoint.
        """
        kpoint = tuple(kpoint)
        H = self.hamiltonian(kpoint)
        energy, U = np.linalg.eigh(H)
        return energy, U


    def velocity(self,kpoint):
        """
        Compute the velocity at a given kpoint.

        Parameters:
        kpoint : np.ndarray
            The kpoint at which to compute the velocity.

        Returns: list
            The velocity at the given kpoint.
        """
        kpoint = tuple(kpoint)
        v_opetator = grad_adaptive(self.hamiltonian,kpoint)
        _, U = self.get_energy_band(kpoint)
        
        return [U.T.conj() @ V @ U for V in v_opetator] # U^dag * dH/dk * U
    
    def inter_band_berry_connection(self,kpoint):
        """
        Compute the inter-band Berry connection at a given kpoint.
        
        Parameters:
        kpoint : np.ndarray
            The kpoint

        Return: list
            r_nm 
        """
        E,_ = self.get_energy_band(kpoint)
        vnm = self.velocity(kpoint)
        E_nm = np.expand_dims(E,axis=1) - np.expand_dims(E,axis=0) + 1j*1e-10 # E_nm = E_n - E_m
        delta_bar = np.ones(E_nm.shape)-np.eye(E_nm.shape[0])
        return [-1j*delta_bar*vnm[i]/E_nm for i in range(len(vnm))]
        


    def LocalQuantumGeometry(self,kpoint,direction):
        """
        Compute the local quantum geometry at a given kpoint and band index.
        The local quantum geometry is defined as the z_{nm}^{ab} = r^a_{nm}r^b_{mn} where n \ne m

        Parameters:
        kpoint : np.ndarray
            The kpoint at which to compute the quantum geometry.
        direction : np.ndarray
            The direction in which to compute the quantum geometry. Should be a 1x2 array with values in {1,2,3}.
        
        Returns: np.ndarray
            The local quantum geometry at the given kpoint and band index. z_nm^ab, where a = direction[0], b = direction[1]
        """
        if direction.shape != (1,2):
            raise ValueError("Direction must be a 1x2 array, but got {direction.shape}")
        valid_values = [0,1,2]
        if not np.all(np.isin(direction, valid_values)):
            raise ValueError(f"Direction must be in {valid_values}, but got {direction}")
        a,b = direction[0],direction[1]
        rnm = self.inter_band_berry_connection(kpoint)


        gnm_ab = rnm[a] * rnm[b].conj()  # znm^{ab} = r_nm^a r_mn^b
        return gnm_ab

    def Local_S_QuantumGeometry(self,kpoint,spin:list):
        """
        Compute the local S quantum geometry at a given kpoint.  Sigma_nm^ab = s_nm^a s_mn^b

        Parameters:
        kpoint : np.ndarray
            The kpoint at which to compute the quantum geometry.
        spin : list
            [spin_a,spin_b] where spin_a and spin_b are the spin matrix
        
        Returns: np.ndarray
            The local S quantum geometry at the given kpoint and spin. S_nm^ab, where a,b coms from the spin list.
        """
        if len(spin) != 2:
            raise ValueError("Spin must be a list of length 2, but got {len(spin)}")
        E, U = self.get_energy_band(kpoint)
        snm_a = U.T.conj()@spin[0]@U
        snm_b = U.T.conj()@spin[1]@U
        return snm_a * snm_b.conj()
    
    def Local_Zeeman_QuantumGeometry(self,kpoint,rs_list:list):
        """
        Local_Zeeman_QuantumGeometry compute the Zeeman QGT  z_nm^ab = r_nm^a s_mn^b

        Parameters:
        kpoints : np.ndarray
        rs_list : list
            [1,sx];
        
        Returns: np.ndarray

        """

        if len(rs_list)!=2:
            raise ValueError("rs_list must be a list of length 2, but got {len(rs_list)}")
        valid_values = [0,1,2]

        if not np.all(np.isin(rs_list[0], valid_values)):
            raise ValueError("The first term must be in [1,2,3], and the second term must be matrix")
        _,U = self.get_energy_band(kpoint)
        rnm_a = self.inter_band_berry_connection(kpoint)[rs_list[0]]
        snm_b = U.T.conj()@rs_list[1]@U
        return rnm_a*snm_b.conj()
    
    def LocalBerryCurvature(self,kpoint,direction):
        """
        Compute the Berry curvature at a given kpoint and band index.

        Parameters:
        """
        return -2*np.imag(self.LocalQuantumGeometry(kpoint,direction))
    
    def LocalQuantumMetric(self,kpoint,direction):
        """
        Compute the local quantum metric at a given kpoint and band index.

        Parameters:
        """
        return np.real(self.LocalQuantumGeometry(kpoint,direction))
    
    def Local_S_Berrycurvature(self,kpoint,spin:list):
        """
        Compute the local S Berry curvature at a given kpoint and band index.

        Parameters:
        """
        return -2*np.imag(self.Local_S_QuantumGeometry(kpoint,spin))
    def Local_S_QuantumMetric(self,kpoint,spin:list):
        """
        Compute the local S quantum metric at a given kpoint and band index.
        """
        return np.real(self.Local_S_QuantumGeometry(kpoint,spin))
    def Local_Zeeman_Berrycurvature(self,kpoint,rs_list:list):
        """
        Compute the local Zeeman Berry curvature at a given kpoint and band index.
        """
        return -2*np.imag(self.Local_Zeeman_QuantumGeometry(kpoint,rs_list))
    def Local_Zeeman_QuantumMetric(self,kpoint,rs_list:list):
        """
        Compute the local Zeeman quantum metric at a given kpoint and band index.
        """
        return np.real(self.Local_Zeeman_QuantumGeometry(kpoint,rs_list))


