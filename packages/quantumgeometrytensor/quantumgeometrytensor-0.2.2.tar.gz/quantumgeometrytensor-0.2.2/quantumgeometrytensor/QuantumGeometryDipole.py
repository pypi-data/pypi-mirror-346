from .QuantumGeometry import QuantumGeometry
import numpy as np
from .Function import grad_adaptive
class QuantumGeometryDipole(QuantumGeometry):
    """
    Class to compute the dipole moment of a quantum system.
    """

    def __init__(self, hamiltonian):
        """
        Initialize the QuantumGeometryDipole class.

        Parameters:
        - system: The quantum system for which to compute the dipole moment.
        - dipole_moment: The dipole moment of the system.
        """
        super().__init__(hamiltonian)
    
    def spinDipole(self,kpoint,spin):
        """
        Compute the spin matrix dipole at a given kpoint. nabla_c s_nm^a = i ( r^c_nt s^a_tm - s^a_nt r^c_tm)
        """
        _,U = self.get_energy_band(kpoint)
        snm = U.T.conj() @ spin @ U
        rnm = self.inter_band_berry_connection(kpoint)
        return [1j*np.einsum('nt,tm->nm',r,snm) - 1j*np.einsum('nt,tm->nm',snm,r) for r in rnm]

        

    def Local_S_QuantumGeometryDipole(self,kpoint,spin:list):
        """
        Compute the local S quantum geometry dipole at a given kpoint.  nabla_c Sigma_nm^ab 
        """
        # _,U = self.get_energy_band(kpoint)
        # snm_a = U.T.conj() @ spin[0] @ U
        # snm_b = U.T.conj() @ spin[1] @ U
        # snm_a_dipole = self.spinDipole(kpoint,spin[0])
        # snm_b_dipole = self.spinDipole(kpoint,spin[1])
        # return [snm_a_dipole[i]*snm_b.conj() + snm_a*snm_b_dipole[i].conj() for i in range(len(snm_a_dipole)) ]
        S_QGT = lambda kpoint: self.Local_S_QuantumGeometry(kpoint,spin)
        return grad_adaptive(S_QGT, kpoint, h=1e-5)
    
    def Local_S_BerryCurvatureDipole(self,kpoint,spin:list):
        """
        Compute the local S Berry curvature dipole at a given kpoint. 
        """
        return [-2*np.imag(i) for i in self.Local_S_QuantumGeometryDipole(kpoint,spin)]

    def Local_S_QuantumMetricDipole(self, kpoint, spin):
        return [np.real(i) for i in self.Local_S_QuantumGeometryDipole(kpoint,spin)]

    def Local_Zeeman_QuantumGeometryDipole(self, kpoint, rs_list):
        Zeeman_QGT = lambda kpoint: self.Local_Zeeman_QuantumGeometry(kpoint,rs_list)
        return grad_adaptive(Zeeman_QGT, kpoint, h=1e-5)

    def Local_Zeeman_BerryCurvatureDipole(self, kpoint, rs_list):
        return [-2*np.imag(i) for i in self.Local_Zeeman_QuantumGeometryDipole(kpoint,rs_list)]

    def Local_Zeeman_QuantumMetricDipole(self, kpoint, rs_list):
        return [np.real(i) for i in self.Local_Zeeman_QuantumGeometryDipole(kpoint,rs_list)]
    def Local_QuantumGeometryDipole(self, kpoint, direction):
        """
        Compute the local quantum geometry dipole at a given kpoint and band index.
        """
        QGT = lambda kpoint: self.LocalQuantumGeometry(kpoint, direction)
        return grad_adaptive(QGT, kpoint, h=1e-5)
    def Local_BerryCurvatureDipole(self, kpoint, direction):
        return [-2*np.imag(i) for i in self.Local_QuantumGeometryDipole(kpoint, direction)]
    def Local_QuantumMetricDipole(self, kpoint, direction):
        return [np.real(i) for i in self.Local_QuantumGeometryDipole(kpoint, direction)]