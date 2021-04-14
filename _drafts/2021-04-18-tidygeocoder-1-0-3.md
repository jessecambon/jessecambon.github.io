---
layout: post
title: "Tidygeocoder 1.0.3"
date: 2021-04-14
author: Jesse Cambon
tags: [tidygeocoder]
image: ""
output: 
  md_document:
    pandoc_args: ["--wrap=none"]
    variant: gfm
    preserve_yaml: TRUE 
---

[Tidygeocoder v1.0.3](https://jessecambon.github.io/tidygeocoder/) is released on [CRAN](https://cran.r-project.org/package=tidygeocoder)! This release adds **reverse geocoding** (getting address data from latitude and longitude) and **6 new geocoder services**. Big thanks go to [Diego Hernangómez](https://github.com/dieghernan) and [Daniel Possenriede](https://github.com/dpprdan) for their work on this release. You can refer to the [changelog](https://jessecambon.github.io/tidygeocoder/news/index.html) for further details on the release.

``` r
library(tidyverse, warn.conflicts = FALSE)
```

    ## ── Attaching packages ─────────────────────────────────────── tidyverse 1.3.0 ──

    ## ✓ ggplot2 3.3.3     ✓ purrr   0.3.4
    ## ✓ tibble  3.0.6     ✓ dplyr   1.0.4
    ## ✓ tidyr   1.1.2     ✓ stringr 1.4.0
    ## ✓ readr   1.4.0     ✓ forcats 0.5.1

    ## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
    ## x dplyr::filter() masks stats::filter()
    ## x dplyr::lag()    masks stats::lag()

``` r
library(tidygeocoder)

num_coords <- 10 # number of locations
set.seed(103) # for reproducibility

# latitude and longitude bounds
lat_limits <- c(40.40857, 40.42585)
long_limits <- c(-3.72472, -3.66983)

# randomly sample latitudes and longitude values
random_lats <- runif(
  num_coords, 
  min = lat_limits[1], 
  max = lat_limits[2]
  )

random_longs <- runif(
  num_coords, 
  min = long_limits[1], 
  max = long_limits[2]
  )

# reverse geocode coordinates
madrid <- reverse_geo(lat = random_lats, random_longs, 
                      method = 'osm', full_results = TRUE,
                      custom_query = list(extratags = 1, addressdetails = 1, namedetails = 1))
```

``` r
# https://leaflet-extras.github.io/leaflet-providers/preview/
library(leaflet)

madrid %>% # Our dataset
  leaflet(width = "100%", options = leafletOptions(attributionControl = FALSE)) %>%
  setView(lng = mean(madrid$long), lat = mean(madrid$lat), zoom = 14) %>%
  # Map Backgrounds
  addProviderTiles(providers$Stamen.Terrain, group = "Terrain") %>%
  addProviderTiles(providers$OpenRailwayMap, group = "Rail") %>%
  addProviderTiles(providers$Esri.WorldImagery, group = "Satellite") %>%
  addTiles(group = "OSM") %>%
  # Add Markers
  addMarkers(
    labelOptions = labelOptions(noHide = F), lng = ~long, lat = ~lat,
#    clusterOptions = markerClusterOptions(maxClusterRadius = 10), 
    label = ~name,
    group = "Random Locations"
  ) %>%
  # Map Control Options
  addLayersControl(
    baseGroups = c("OSM", "Terrain", "Satellite", "Rail"),
    overlayGroups = c("Random Locations"),
    options = layersControlOptions(collapsed = TRUE)
  )
```

<img src="/rmd_images/2021-04-18-tidygeocoder-1-0-3/unnamed-chunk-2-1.png" style="display: block; margin: auto;" />
