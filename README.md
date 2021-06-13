# VoronoiAnalyse
This script is used to calculate the voronoi volume of each sites in a crystal.


The cutoff threhold shoule be modified in some cases. 

## How to use this code?
```markdown
python get_voronoi_volume.py
```

## Note:
1. If you are working on a high-entropy material which the atomic positions distort signifcantly. You may have chance to get a unreasonalble atomic volume. In this case, increase the cutoff in [get_all_neighbors()](https://github.com/jzhang-github/VoronoiAnalyse/blob/eb4f1e93202cb1d164efc493a4c8fb37fb3b4442/get_voronoi_volume.py#L80-L81) function.

2. If your structure is not a cubic system, you need to change the fraction volume of atoms by changing [this](https://github.com/jzhang-github/VoronoiAnalyse/blob/eb4f1e93202cb1d164efc493a4c8fb37fb3b4442/get_voronoi_volume.py#L78).
