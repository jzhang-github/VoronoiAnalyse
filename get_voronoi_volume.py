# -*- coding: utf-8 -*-
"""
Created on Fri May 14 10:15:55 2021

@author: ZHANG Jun

Emain: j.zhang@my.cityu.edu.hk

This script is used to calculate the voronoi volume of each sites in a crystal.

20210619. update.
"""

from pymatgen.core.structure import Structure
import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial import Voronoi
import os
from sys import argv

# =============================================================================
if len(argv) < 4 or '-h' in argv:
    print("\n"+"Usage: Command + FileName + Start_index + End_index")
    os._exit(0)
# =============================================================================

class VoronoiAnalyse(object):
    """
    Description
    ----------
        This script is used to calculate the voronoi volume of a BCC crystal.
        For another crystal types, you need to modify the value of
        "volume_fraction_for_cubic" in "__call__()" function.

    Parameters
    ----------
    file_name : str
        User defined file name.
    start_index : int
        In many cases, we don't need all the Voronoi volumes of every atom.
        Therefore, this is the start. For python, the index starts from zero.
    end_index : int
        This is the end of index. If you want include the 100th atom, the end
        index should be 100.
    """
    def __init__(self,
                 file_name,
                 start_index,
                 end_index):
        self.file_name = file_name
        self.start_index = start_index
        self.end_index = end_index

    def voronoi_volumes(self, points): # Refer to: https://stackoverflow.com/questions/19634993/volume-of-voronoi-cell-python
        """
        Parameters
        ----------
        points : np.array
            Cartesian coordinates of the crystal.
        Return
        ----------
        vol: list
            Voronoi volumes of each site.
        """
        v = Voronoi(points)
        vol = np.zeros(v.npoints)
        for i, reg_num in enumerate(v.point_region):
            indices = v.regions[reg_num]
            if -1 in indices: # some regions can be opened
                vol[i] = np.inf
            else:
                vol[i] = ConvexHull(v.vertices[indices]).volume
        return vol

    def __call__(self):
        """
        Return
        ----------
        vor_vol: list
            Voronoi volumes of specified sites.
        error: float
            Compare the total Voronoi volume and the cell volume.
            Positive value indicates overestimating.
        """
        crystal = Structure.from_file(self.file_name)
        self.cell_volume = crystal.volume
        self.number_of_atoms = crystal.num_sites
        volume_fraction_for_cubic = 0.5235987755982988
        self.atomic_diameter = (self.cell_volume * volume_fraction_for_cubic / self.number_of_atoms * 3 / 4 / np.pi) ** (1 / 3) * 2
        all_NN = crystal.get_all_neighbors(r=self.atomic_diameter*1.2071067811865475,
                                           include_index=True)
        vor_vol = []
        for i in range(self.number_of_atoms):
            number_of_neighbors = len(all_NN[i])
            coords = []
            coords.append(crystal[i].coords)
            for j in range(number_of_neighbors):
                coords.append(all_NN[i][j].coords)
            coords = np.array(coords)
            vor_vol.append(self.voronoi_volumes(coords)[0])

        error = np.sum(vor_vol) / self.cell_volume - 1.0
        vor_vol = vor_vol[self.start_index: self.end_index]
        return vor_vol, error

if __name__ == '__main__':
    fname_argv,start_argv, end_argv= argv[1:4]
    vor_crystal = VoronoiAnalyse(fname_argv, int(start_argv), int(end_argv))
    vor_vol, error = vor_crystal()
    for i in range(len(vor_vol)):
        print(vor_vol[i], flush=True)
    print('Error:', error)

