import numpy as np
import sisl


def ssh(d1=1.0, d2=1.5, dy=10):
    """ Generates the ssh-chain geoemtry along the x-axis direction

    Parameters
    ----------
    d1 : float, optional
        intra-atomic distance
    d2 : float, optional
        inter-atomic distance
    dy : float, optional
        size of the supercell in the y-axis direction
    """
    xyz = [[0., 0., 0.], [d1, 0, 0]]
    # Create supercell and geometry
    sc = sisl.SuperCell([d1+d2, dy, 10, 90, 90, 90], nsc=[3, 1, 1])
    uc = sisl.Geometry(xyz, sisl.Atom(Z=6), sc=sc)
    # Iterate over atomic species to set initial charge
    r = np.linspace(0, 1.6, 700)
    func = 5 * np.exp(-r * 5)
    for atom, _ in uc.atoms.iter(True):
        pz = sisl.AtomicOrbital('pz', (r, func), q0=atom.Z-5)
        atom.orbitals[0] = pz
    uc = uc.move(-uc.center(what='xyz'))
    return uc