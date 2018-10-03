from __future__ import print_function

import matplotlib.pyplot as plt
from Hubbard.plot import GeometryPlot
import sisl
import numpy as np


class Charge(GeometryPlot):

    def __init__(self, HubbardHamiltonian, **keywords):
        # Set default keywords
        if 'realspace' in keywords:
            if 'facecolor' not in keywords:
                keywords['facecolor'] = 'None'
            if 'cmap' not in keywords:
                keywords['cmap'] = 'Greys'
        else:
            if 'cmap' not in keywords:
                keywords['cmap'] = plt.cm.bwr

        GeometryPlot.__init__(self, HubbardHamiltonian, **keywords)

        # Compute total charge on each site
        charge = HubbardHamiltonian.nup + HubbardHamiltonian.ndn

        if 'realspace' in keywords:
            self.__realspace__(charge, HubbardHamiltonian, **keywords)

        else:
            self.__orbitals__(charge, **keywords)

    def __orbitals__(self, charge, **keywords):
        # Set values for the pi-network
        self.ppi.set_array(charge)

        # Set color range
        if 'vmax' in keywords:
            self.ppi.set_clim(0, keywords['vmax'])
        else:
            self.ppi.set_clim(min(charge), max(charge))

        # Colorbars
        if 'colorbar' in keywords:
            if keywords['colorbar'] != False:
                self.add_colorbar(self.ppi, label=r'$Q_\uparrow+Q_\downarrow$ ($e$)')

    def __realspace__(self, charge, HubbardHamiltonian, z=1.1, vmax=0.006, grid_unit=0.05, **keywords):
        # As the radial extension is only 1.6 ang, two times this should
        # be enough for the supercell in the z-direction:
        sc = sisl.SuperCell([self.xmax-self.xmin, self.ymax-self.ymin, 3.2])
        grid = sisl.Grid(grid_unit, sc=sc)

        # The following is a bit of black magic...
        # not sure this gives the density on the grid
        vecs = np.zeros((HubbardHamiltonian.sites, HubbardHamiltonian.sites))
        vecs[0, :] = charge
        H = HubbardHamiltonian.H.move([-self.xmin, -self.ymin, 0])
        H.xyz[np.where(np.abs(H.xyz[:, 2]) < 1e-3), 2] = 0
        H.set_sc(sc)
        es = sisl.EigenstateElectron(vecs, np.zeros(HubbardHamiltonian.sites), H)
        es.sub(0).psi(grid)
        index = grid.index([0, 0, z])

        # Plot only the real part
        ax = self.axes.imshow(grid.grid[:, :, index[2]].T.real, cmap='seismic', origin='lower',
                              vmax=vmax, vmin=-vmax, extent=self.extent)
        # Colorbars
        if 'colorbar' in keywords:
            if keywords['colorbar'] != False:
                # Charge density per unit of length in the z-direction
                plt.colorbar(ax, label=r'$q_\uparrow+q_\downarrow$ ($e/$\AA)')

class ChargeDifference(GeometryPlot):

    def __init__(self, HubbardHamiltonian, **keywords):

        # Set default keywords
        if 'cmap' not in keywords:
            keywords['cmap'] = plt.cm.bwr

        GeometryPlot.__init__(self, HubbardHamiltonian, **keywords)

        # Compute total charge on each site, subtract neutral atom charge
        charge = HubbardHamiltonian.nup + HubbardHamiltonian.ndn
        for ia in HubbardHamiltonian.geom:
            charge[ia] -= HubbardHamiltonian.geom.atoms[ia].Z-5

        if 'realspace' in keywords:
            self.__realspace__(HubbardHamiltonian, charge, **keywords)
        else:
            self.__orbitals__(charge, **keywords)
            
    def __orbitals__(self, charge, **keywords):
        # Set values for the pi-network
        self.ppi.set_array(charge)

        # Set color range
        if 'vmax' in keywords:
            cmax = keywords['vmax']
        else:
            cmax = max(abs(charge))
        self.ppi.set_clim(-cmax, cmax)

        # Colorbars
        if 'colorbar' in keywords:
            if keywords['colorbar'] != False:
                self.add_colorbar(self.ppi, label=r'$Q_\uparrow+Q_\downarrow-Q_\mathrm{NA}$ ($e$)')

    def __realspace__(self, HubbardHamiltonian, charge, z=1.1, vmax=0.006, grid_unit=0.05, **keywords):
        sc = sisl.SuperCell([self.xmax-self.xmin, self.ymax-self.ymin, 3.2])
        grid = sisl.Grid(grid_unit, sc=sc)
        
        vecs = np.zeros((HubbardHamiltonian.sites, HubbardHamiltonian.sites))
        vecs[0, :] = charge
        H = HubbardHamiltonian.H.move([-self.xmin, -self.ymin, 0])
        H.xyz[np.where(np.abs(H.xyz[:, 2]) < 1e-3), 2] = 0
        H.set_sc(sc)
        es = sisl.EigenstateElectron(vecs, np.zeros(HubbardHamiltonian.sites), H)
        es.sub(0).psi(grid)
        index = grid.index([0, 0, z])

        # Plot only the real part
        ax = self.axes.imshow(grid.grid[:, :, index[2]].T.real, cmap='seismic', origin='lower',
                              vmax=vmax, vmin=-vmax, extent=self.extent)
        # Colorbars
        if 'colorbar' in keywords:
            if keywords['colorbar'] != False:
                # Charge density per unit of length in the z-direction
                plt.colorbar(ax, label=r'$q_\uparrow+q_\downarrow-q_\mathrm{NA}$ ($e/$\AA)')
        

class SpinPolarization(GeometryPlot):

    def __init__(self, HubbardHamiltonian, **keywords):

        # Set default keywords
        if 'realspace' in keywords:
            if 'facecolor' not in keywords:
                keywords['facecolor'] = 'None'
            if 'cmap' not in keywords:
                keywords['cmap'] = 'Greys'
        else:
            if 'cmap' not in keywords:
                keywords['cmap'] = plt.cm.bwr

        GeometryPlot.__init__(self, HubbardHamiltonian, **keywords)

        # Compute charge difference between up and down channels
        charge = HubbardHamiltonian.nup - HubbardHamiltonian.ndn

        if 'realspace' in keywords:
            self.__realspace__(charge, HubbardHamiltonian, **keywords)

        else:
            self.__orbitals__(charge, **keywords)

    def __orbitals__(self, charge, **keywords):
        # Set values for the pi-network
        self.ppi.set_array(charge)

        # Set color range
        if 'vmax' in keywords:
            cmax = keywords['vmax']
        else:
            cmax = max(abs(charge))
        self.ppi.set_clim(-cmax, cmax)

        # Colorbars
        if 'colorbar' in keywords:
            if keywords['colorbar'] != False:
                self.add_colorbar(self.ppi, label=r'$Q_\uparrow-Q_\downarrow$ ($e$)')

    def __realspace__(self, charge, HubbardHamiltonian, z=1.1, vmax=0.006, grid_unit=0.05, **keywords):
        # As the radial extension is only 1.6 ang, two times this should
        # be enough for the supercell in the z-direction:
        sc = sisl.SuperCell([self.xmax-self.xmin, self.ymax-self.ymin, 3.2])
        grid = sisl.Grid(grid_unit, sc=sc)

        # The following is a bit of black magic...
        # not sure this gives the density on the grid
        vecs = np.zeros((HubbardHamiltonian.sites, HubbardHamiltonian.sites))
        vecs[0, :] = charge
        H = HubbardHamiltonian.H.move([-self.xmin, -self.ymin, 0])
        H.xyz[np.where(np.abs(H.xyz[:, 2]) < 1e-3), 2] = 0
        H.set_sc(sc)
        es = sisl.EigenstateElectron(vecs, np.zeros(HubbardHamiltonian.sites), H)
        es.sub(0).psi(grid)
        index = grid.index([0, 0, z])

        # Plot only the real part
        ax = self.axes.imshow(grid.grid[:, :, index[2]].T.real, cmap='seismic', origin='lower',
                              vmax=vmax, vmin=-vmax, extent=self.extent)
        # Colorbars
        if 'colorbar' in keywords:
            if keywords['colorbar'] != False:
                # Charge density per unit of length in the z-direction
                plt.colorbar(ax, label=r'$q_\uparrow-q_\downarrow$ ($e/$\AA)')
