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

[Tidygeocoder v1.0.3](https://jessecambon.github.io/tidygeocoder/) is released on [CRAN](https://cran.r-project.org/package=tidygeocoder)! This release adds support for reverse geocoding (geocoding geographic coordinates) and 7 new geocoder services: [OpenCage](https://opencagedata.com/), [HERE](https://developer.here.com/products/geocoding-and-search), [Mapbox](https://docs.mapbox.com/api/search/), [MapQuest](https://developer.mapquest.com/documentation/geocoding-api/), [TomTom](https://developer.tomtom.com/search-api/search-api-documentation/geocoding), [Bing](https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/), and [ArcGIS](https://developers.arcgis.com/rest/geocode/api-reference/overview-world-geocoding-service.htm). Refer to the [geocoder services page](https://jessecambon.github.io/tidygeocoder/articles/geocoder_services.html) for information on all the supported geocoder services.

Big thanks go to [Diego Hernangómez](https://github.com/dieghernan) and [Daniel Possenriede](https://github.com/dpprdan) for their work on this release. You can refer to the [changelog](https://jessecambon.github.io/tidygeocoder/news/index.html) for further details on all the changes.

## Reverse Geocoding

To demonstrate the new reverse geocoding capabilities, in this example we’ll randomly sample coordinates in Madrid and label them on a map. The coordinates are placed in a dataframe and reverse geocoded with the `reverse_geocode()` function. The Nominatim (“osm”) geocoder service is used and several API parameters are passed via the `custom_query` argument to return additional data from Nominatim. Refer to [Nominatim’s API documentation](https://nominatim.org/release-docs/latest/api/Reverse/) for details.

``` r
library(tidyverse, warn.conflicts = FALSE)
library(tidygeocoder)
library(knitr)
library(leaflet)
library(glue)
library(htmltools)

num_coords <- 30 # number of locations
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

# reverse geocode the coordinates
madrid <- reverse_geo(
              lat = random_lats, random_longs, 
              method = 'osm', full_results = TRUE,
              custom_query = list(extratags = 1, addressdetails = 1, namedetails = 1)
          )
```

After geocoding our coordinates, we can construct HTML labels with the data returned from Nominatim and display these locations on a leaflet map.

``` r
# Create html labels
# https://rstudio.github.io/leaflet/popups.html
madrid_labelled <- madrid %>%
  transmute(
    lat, 
    long, 
    label = str_c(
        ifelse(is.na(name), "", glue("<b>{name}</b></br>")),
        ifelse(is.na(suburb), "", glue("<b>Suburb</b>: {suburb}</br>")),
        ifelse(is.na(quarter), "", glue("<b>Quarter</b>: {quarter}")),
        sep = ''
    ) %>% lapply(htmltools::HTML)
  )

# Make the leaflet map
madrid_labelled %>% 
  leaflet(width = "100%", options = leafletOptions(attributionControl = FALSE)) %>%
  setView(lng = mean(madrid$long), lat = mean(madrid$lat), zoom = 14) %>%
  # Map Backgrounds
  # https://leaflet-extras.github.io/leaflet-providers/preview/
  addProviderTiles(providers$Stamen.Terrain, group = "Terrain") %>%
  addProviderTiles(providers$OpenRailwayMap, group = "Rail") %>%
  addProviderTiles(providers$Esri.WorldImagery, group = "Satellite") %>%
  addTiles(group = "OSM") %>%
  # Add Markers
  addMarkers(
    labelOptions = labelOptions(noHide = F), lng = ~long, lat = ~lat,
    label = ~label,
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

## Limits

This release also adds improve support for returning multiple results per input with the `limit` argument. Consider this batch query with the US census geocoder:

``` r
tie_addresses <- tibble::tribble(
  ~res_street_address, ~res_city_desc, ~state_cd, ~zip_code,
  "624 W DAVIS ST   #1D",   "BURLINGTON", "NC",  27215,
  "201 E CENTER ST   #268", "MEBANE",     "NC",  27302,
  "7833  WOLFE LN",         "SNOW CAMP",  "NC",  27349,
)

tg_batch <- tie_addresses %>%
  geocode(
    street = res_street_address,
    city = res_city_desc,
    state = state_cd,
    postalcode = zip_code,
    method = 'census', 
    full_results = TRUE
  )
```

| res\_street\_address  | res\_city\_desc | state\_cd | zip\_code | lat | long |  id | input\_address                             | match\_indicator | match\_type | matched\_address | tiger\_line\_id | tiger\_side |
|:----------------------|:----------------|:----------|----------:|----:|-----:|----:|:-------------------------------------------|:-----------------|:------------|:-----------------|:----------------|:------------|
| 624 W DAVIS ST \#1D   | BURLINGTON      | NC        |     27215 |  NA |   NA |   1 | 624 W DAVIS ST \#1D, BURLINGTON, NC, 27215 | Tie              | NA          | NA               | NA              | NA          |
| 201 E CENTER ST \#268 | MEBANE          | NC        |     27302 |  NA |   NA |   2 | 201 E CENTER ST \#268, MEBANE, NC, 27302   | Tie              | NA          | NA               | NA              | NA          |
| 7833 WOLFE LN         | SNOW CAMP       | NC        |     27349 |  NA |   NA |   3 | 7833 WOLFE LN, SNOW CAMP, NC, 27349        | Tie              | NA          | NA               | NA              | NA          |

You can see NA results are returned and the `match_indicator` column indicates a “Tie”. This is what the US Census batch geocoder returns when multiple results are available for each input address (see [issue \#87](https://github.com/jessecambon/tidygeocoder/issues/87) for more details).

In order to see the available results for these addresses, you will need to use single address geocoding. Below we specify to use the single address geocoder instead of batch geocoding with the `mode` argument. The `limit` argument is specified to allow multiple results to be returned per address. The `return_input` argument (new in this release) has to be set to `FALSE` to allow `limit` to be set to a value other than 1 (see the [geocode()](https://jessecambon.github.io/tidygeocoder/reference/geocode.html) function documentation for details).

``` r
tg_single <- tie_addresses %>%
  geocode(
    street = res_street_address,
    city = res_city_desc,
    state = state_cd,
    postalcode = zip_code,
    limit = 100,
    return_input = FALSE,
    method = 'census', 
    mode = 'single',
    full_results = TRUE
  )
```

| street                | city       | state | postalcode |      lat |      long | matchedAddress                        | tigerLine.tigerLineId | tigerLine.side | addressComponents.fromAddress | addressComponents.toAddress | addressComponents.preQualifier | addressComponents.preDirection | addressComponents.preType | addressComponents.streetName | addressComponents.suffixType | addressComponents.suffixDirection | addressComponents.suffixQualifier | addressComponents.city | addressComponents.state | addressComponents.zip |
|:----------------------|:-----------|:------|:-----------|---------:|----------:|:--------------------------------------|:----------------------|:---------------|:------------------------------|:----------------------------|:-------------------------------|:-------------------------------|:--------------------------|:-----------------------------|:-----------------------------|:----------------------------------|:----------------------------------|:-----------------------|:------------------------|:----------------------|
| 624 W DAVIS ST \#1D   | BURLINGTON | NC    | 27215      | 36.09598 | -79.44453 | 624 W DAVIS ST, BURLINGTON, NC, 27215 | 71662708              | L              | 618                           | 628                         |                                | W                              |                           | DAVIS                        | ST                           |                                   |                                   | BURLINGTON             | NC                      | 27215                 |
| 624 W DAVIS ST \#1D   | BURLINGTON | NC    | 27215      | 36.08821 | -79.43201 | 624 E DAVIS ST, BURLINGTON, NC, 27215 | 71664000              | L              | 600                           | 698                         |                                | E                              |                           | DAVIS                        | ST                           |                                   |                                   | BURLINGTON             | NC                      | 27215                 |
| 201 E CENTER ST \#268 | MEBANE     | NC    | 27302      | 36.09683 | -79.26977 | 201 W CENTER ST, MEBANE, NC, 27302    | 71655977              | R              | 201                           | 299                         |                                | W                              |                           | CENTER                       | ST                           |                                   |                                   | MEBANE                 | NC                      | 27302                 |
| 201 E CENTER ST \#268 | MEBANE     | NC    | 27302      | 36.09582 | -79.26624 | 201 E CENTER ST, MEBANE, NC, 27302    | 71656021              | R              | 299                           | 201                         |                                | E                              |                           | CENTER                       | ST                           |                                   |                                   | MEBANE                 | NC                      | 27302                 |
| 7833 WOLFE LN         | SNOW CAMP  | NC    | 27349      | 35.89866 | -79.43713 | 7833 WOLFE LN, SNOW CAMP, NC, 27349   | 71682243              | L              | 7999                          | 7801                        |                                |                                |                           | WOLFE                        | LN                           |                                   |                                   | SNOW CAMP              | NC                      | 27349                 |
| 7833 WOLFE LN         | SNOW CAMP  | NC    | 27349      | 35.89693 | -79.43707 | 7833 WOLF LN, SNOW CAMP, NC, 27349    | 71685327              | L              | 7801                          | 7911                        |                                |                                |                           | WOLF                         | LN                           |                                   |                                   | SNOW CAMP              | NC                      | 27349                 |

We can now see there are two available results for each address. Note that the US Census service API does not have a `limit` argument in its API, but we can still use the `limit` parameter in `geocode()` or `geo()`. Refer to the [api\_parameter\_reference](https://jessecambon.github.io/tidygeocoder/reference/api_parameter_reference.html) documentation for more details.
