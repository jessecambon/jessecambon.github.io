---
layout: post
title:  "Geocoding with Tidygeocoder"
date:   2019-11-08 22:47:40 -0500
categories: geocoding r 
---

The tidygeocoder package is a newly published tidyverse-style interface for geocoding. It returns latitude and longitude coordinates in tibble format from addresses using  the US Census or Nominatim (OSM) geocoder services. In this post I will demonstrate how to use it for plotting a few Washington, DC landmarks in honor of the recent Washington Nationals World Series win.


```r
library(dplyr)
library(tidygeocoder)

dc_addresses <- tribble( ~name,~addr,
"White House", "1600 Pennsylvania Ave Washington, DC",
"National Academy of Sciences", "2101 Constitution Ave NW, Washington, DC 20418",
"Department of Justice", "950 Pennsylvania Ave NW, Washington, DC 20530",
"Supreme Court", "1 1st St NE, Washington, DC 20543",
"Washington Monument", "2 15th St NW, Washington, DC 20024")

coordinates <- dc_addresses %>%
  geocode(addr)
```

The geocode function adds longitude and latitude to our dataframe of addresses as columns. The default geocoder service used is the US Census, but Nominatim or a hybrid approach can be chosen with the "method" argument (see the documentation for details)

| name                         | addr                                           |      lat |       long |
| :--------------------------- | :--------------------------------------------- | -------: | ---------: |
| White House                  | 1600 Pennsylvania Ave Washington, DC           | 38.89875 | \-77.03535 |
| National Academy of Sciences | 2101 Constitution Ave NW, Washington, DC 20418 | 38.89211 | \-77.04678 |
| Department of Justice        | 950 Pennsylvania Ave NW, Washington, DC 20530  | 38.89416 | \-77.02501 |
| Supreme Court                | 1 1st St NE, Washington, DC 20543              | 38.88990 | \-77.00591 |
| Washington Monument          | 2 15th St NW, Washington, DC 20024             | 38.88979 | \-77.03291 |

```r
library(OpenStreetMap)
dc_map <- openmap( c(38.905,-77.05),c(38.885,-77.00))
dc_map.latlng <- openproj(dc_map)
```

Note that the coordinates supplied to the "openmap" function above were obtained using openstreetmap.org (use the export button to extract coordinates). The "openmap" function obtains the map and the "openproj" function projects it onto a latitude and longitude coordinate system so we can overlay our coordinates on a map, which is what we do next:

```r
library(ggplot2)
library(ggrepel)
autoplot(dc_map.latlng) +
  theme_minimal() +
  theme(      axis.text.y=element_blank(),
              axis.title=element_blank(),
              axis.text.x=element_blank(),
              plot.margin = unit(c(0, 0, 0, 0), "cm")
              ) +
  geom_point(data=coordinates, aes(x=long, y=lat), color="navy", size=4, alpha=1) +
  geom_label_repel(data=coordinates,
        aes(label=name,x=long, y=lat),show.legend=F,box.padding=.5,size = 5)
```

And that's our map. Alternatively, the leaflet package provides an excellent interface to plot coordinates on an interactive map. For more information on tidygeocoder, visit its home on GitHub or CRAN.