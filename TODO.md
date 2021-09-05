# NOTE
	- Having difficulties plotting large numbers of points with streamlit, moved to uPlot
	- Wrapped all python functionality in an API, using it from HTMl/JS
	- Fast, can plot lot more points, zoom in/zoom out is easier
    - Plot multiple timseries
	- Plot anomalous points in different colours.
    - I looked at the science fair projects, and most of them have a medical application, and publish a paper
	  - Is there any way I can get a medical professional utilize the tool
  

# TODO
- [x] Number of pages should correspond to the level
- [x] Use all numbers in Millions and put the legend on top/bottom (for x axis)
- [X] Show anomalous points
- [X] Switch over to numpy to get fast load times
- [X] Min/Max on same level
- [ ] Zoom into a certain time, and allow move levels with those points

From Christos Faloutsos to Everyone: (4:44 PM) https://www.dropbox.com/sh/13nyfhzr57vnqaa/AACq1eVvq2UWate7N3oJq-uwa?dl=0 gzcat rat_healthy_int.data.gz | wc -l  175,459,328 gzcat rat_seizure_int.data.gz | wc -l  175,705,856

https://www.cs.ucr.edu/~eamonn/time_series_data/ From Me to Everyone: (4:50 PM) https://www.cs.ucr.edu/~eamonn/time_series_data_2018/ From Christos Faloutsos to Everyone: (4:51 PM) open data (usa; brazil) MIMIC datasets tycho https://www.tycho.pitt.edu/ 

Inputs: street\_name
Outputs: has\_sidewalk, traffic\_info{light, heavy, moderate}
