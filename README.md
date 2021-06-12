# VoronoiAnalyse
## This script is used to calculate the voronoi volume of each sites in a crystal.


The cutoff threhold shoule be modified in some cases. 
If you are working on a high-entropy material which the atomic positions distort signifcantly.
You may have chance to get a unreasonalble atomic volume. In this case, increase the cutoff 
in get_all_neighbors() function.
