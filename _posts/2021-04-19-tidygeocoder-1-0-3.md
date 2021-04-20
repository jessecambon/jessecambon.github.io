---
layout: post
title: "Tidygeocoder 1.0.3"
date: 2021-04-19
author: Jesse Cambon
tags: [r, tidygeocoder]
image: "/images/tidygeocoder_hex.png"
leafletmap: true
always_allow_html: yes
output: 
  md_document:
    pandoc_args: ["--wrap=none"]
    variant: gfm
    preserve_yaml: TRUE
---

[Tidygeocoder v1.0.3](https://jessecambon.github.io/tidygeocoder/) is released on [CRAN](https://cran.r-project.org/package=tidygeocoder)! This release adds support for reverse geocoding (geocoding geographic coordinates) and 7 new geocoder services: [OpenCage](https://opencagedata.com/), [HERE](https://developer.here.com/products/geocoding-and-search), [Mapbox](https://docs.mapbox.com/api/search/), [MapQuest](https://developer.mapquest.com/documentation/geocoding-api/), [TomTom](https://developer.tomtom.com/search-api/search-api-documentation/geocoding), [Bing](https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/), and [ArcGIS](https://developers.arcgis.com/rest/geocode/api-reference/overview-world-geocoding-service.htm). Refer to the [geocoder services page](https://jessecambon.github.io/tidygeocoder/articles/geocoder_services.html) for information on all the supported geocoder services.

Big thanks go to [Diego Hernangómez](https://github.com/dieghernan) and [Daniel Possenriede](https://github.com/dpprdan) for their work on this release. You can refer to the [changelog](https://jessecambon.github.io/tidygeocoder/news/index.html) for the details on the changes in the release.

## Reverse Geocoding

In this example we’ll randomly sample coordinates in Madrid and label them on a map. The coordinates are placed in a dataframe and reverse geocoded with the `reverse_geocode()` function. The Nominatim (“osm”) geocoder service is used and several API parameters are passed via the `custom_query` argument to request additional columns of data from Nominatim. Refer to [Nominatim’s API documentation](https://nominatim.org/release-docs/latest/api/Reverse/) for more information on these parameters.

``` r
library(tidyverse, warn.conflicts = FALSE)
library(tidygeocoder)
library(knitr)
library(leaflet)
library(glue)
library(htmltools)

num_coords <- 25 # number of coordinates
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

# Reverse geocode the coordinates
# the speed of the query is limited to 1 coordinate per second to comply
# with Nominatim's usage policies
madrid <- reverse_geo(
              lat = random_lats, random_longs, 
              method = 'osm', full_results = TRUE,
              custom_query = list(extratags = 1, addressdetails = 1, namedetails = 1)
          )
```

After geocoding our coordinates, we can construct HTML labels with the data returned from Nominatim and display these locations on a [leaflet](http://rstudio.github.io/leaflet/) map.

``` r
# Create html labels
# https://rstudio.github.io/leaflet/popups.html
madrid_labelled <- madrid %>%
  transmute(
    lat, 
    long, 
    label = str_c(
        ifelse(is.na(name), "", glue("<b>Name</b>: {name}</br>")),
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

<div id="htmlwidget-562547e6d92361b7b630" style="width:100%;height:480px;" class="leaflet html-widget"></div>
<script type="application/json" data-for="htmlwidget-562547e6d92361b7b630">{"x":{"options":{"crs":{"crsClass":"L.CRS.EPSG3857","code":null,"proj4def":null,"projectedBounds":null,"options":{}},"attributionControl":false},"setView":[[40.415021103152,-3.69357282582785],14,[]],"calls":[{"method":"addProviderTiles","args":["Stamen.Terrain",null,"Terrain",{"errorTileUrl":"","noWrap":false,"detectRetina":false}]},{"method":"addProviderTiles","args":["OpenRailwayMap",null,"Rail",{"errorTileUrl":"","noWrap":false,"detectRetina":false}]},{"method":"addProviderTiles","args":["Esri.WorldImagery",null,"Satellite",{"errorTileUrl":"","noWrap":false,"detectRetina":false}]},{"method":"addTiles","args":["//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",null,"OSM",{"minZoom":0,"maxZoom":18,"tileSize":256,"subdomains":"abc","errorTileUrl":"","tms":false,"noWrap":false,"zoomOffset":0,"zoomReverse":false,"opacity":1,"zIndex":1,"detectRetina":false,"attribution":"&copy; <a href=\"http://openstreetmap.org\">OpenStreetMap<\/a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA<\/a>"}]},{"method":"addMarkers","args":[[40.4123014709814,40.4096615445682,40.4175871664274,40.417272506227,40.4106519994937,40.4100781149822,40.4160619508378,40.411906436556,40.4091072090676,40.413993361209,40.4163817212981,40.4135176730348,40.4223178283641,40.4228223820305,40.423828380907,40.410822169486,40.4109466401929,40.4134973449898,40.4146834641808,40.4143576724255,40.4116045660791,40.4180861643726,40.4174389485912,40.4185510909274,40.4180497715706],[-3.67578744418699,-3.67010136934424,-3.67335474251329,-3.70310583343772,-3.67488869123186,-3.71444517586805,-3.67663930623259,-3.68756156697234,-3.72200196854039,-3.69475406050333,-3.67205522449481,-3.70229658222932,-3.6763332644197,-3.68158102478245,-3.72233264530065,-3.6795209595742,-3.68922342991826,-3.69160540612346,-3.6707955976882,-3.70259709061521,-3.7173106429264,-3.72088573588971,-3.69363431777976,-3.71829686008829,-3.70821170503502],null,null,"Random Locations",{"interactive":true,"draggable":false,"keyboard":true,"title":"","alt":"","zIndexOffset":0,"opacity":1,"riseOnHover":false,"riseOffset":250},null,null,null,null,["<b>Name<\/b>: Torre del Retiro<\/br><b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Niño Jesús","<b>Name<\/b>: Alimentación Bazar<\/br><b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Niño Jesús","<b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Ibiza","<b>Name<\/b>: Casa de Empeño<\/br><b>Suburb<\/b>: Sol<\/br><b>Quarter<\/b>: Sol","<b>Name<\/b>: Real Escuela Superior de Arte Dramático (RESAD)<\/br><b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Niño Jesús","<b>Name<\/b>: Dalieda de San Francisco<\/br><b>Suburb<\/b>: Palacio<\/br>","<b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Ibiza","<b>Name<\/b>: Bosque del Recuerdo<\/br><b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Jerónimos","<b>Suburb<\/b>: Latina<\/br>","<b>Suburb<\/b>: Cortes<\/br><b>Quarter<\/b>: Cortes","<b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Ibiza","<b>Suburb<\/b>: Embajadores<\/br>","<b>Suburb<\/b>: Salamanca<\/br><b>Quarter<\/b>: Goya","<b>Suburb<\/b>: Salamanca<\/br><b>Quarter<\/b>: Recoletos","<b>Suburb<\/b>: Moncloa-Aravaca<\/br>","<b>Name<\/b>: La Rosaleda<\/br><b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Jerónimos","<b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Jerónimos","<b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Jerónimos","<b>Name<\/b>: Citröen España<\/br><b>Suburb<\/b>: Retiro<\/br><b>Quarter<\/b>: Niño Jesús","<b>Name<\/b>: España Cañi<\/br><b>Suburb<\/b>: Cortes<\/br>","<b>Suburb<\/b>: Palacio<\/br><b>Quarter<\/b>: Palacio","<b>Name<\/b>: Paseo de la Virgen del Puerto<\/br><b>Suburb<\/b>: Palacio<\/br><b>Quarter<\/b>: Palacio","<b>Suburb<\/b>: Cortes<\/br><b>Quarter<\/b>: Cortes","<b>Suburb<\/b>: Moncloa-Aravaca<\/br><b>Quarter<\/b>: Argüelles","<b>Name<\/b>: Oratorio Santo Niño del Remedio<\/br><b>Suburb<\/b>: Centro<\/br>"],{"interactive":false,"permanent":false,"direction":"auto","opacity":1,"offset":[0,0],"textsize":"10px","textOnly":false,"className":"","sticky":true},null]},{"method":"addLayersControl","args":[["OSM","Terrain","Satellite","Rail"],"Random Locations",{"collapsed":true,"autoZIndex":true,"position":"topright"}]}],"limits":{"lat":[40.4091072090676,40.423828380907],"lng":[-3.72233264530065,-3.67010136934424]}},"evals":[],"jsHooks":[]}</script>

## Limits

This release also improves support for returning multiple results per input with the `limit` argument. Consider this batch query with the US Census geocoder:

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

To see all available results for these addresses, you will need to use `mode` to force single address (not batch) geocoding and `limit > 1`. The `return_input` argument (new in this release) has to be set to `FALSE` to allow `limit` to be set to a value other than 1. See the [geocode() function documentation](https://jessecambon.github.io/tidygeocoder/reference/geocode.html) for details.

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

We can now see there are two available results for each address. Note that this particular issue with “Tie” batch results is specific to the US Census geocoder service. Refer to the [api\_parameter\_reference](https://jessecambon.github.io/tidygeocoder/reference/api_parameter_reference.html) documentation for more details on the `limit` parameter.

The `limit` parameter can also be used to return all matches for a more general query:

``` r
paris <- geo('Paris', method = 'opencage', full_results = TRUE, limit = 10)
```

| address |      lat |       long | formatted                                 | annotations.currency.name |
|:--------|---------:|-----------:|:------------------------------------------|:--------------------------|
| Paris   | 48.85670 |   2.351462 | Paris, France                             | Euro                      |
| Paris   | 33.66180 | -95.555513 | Paris, TX 75460, United States of America | United States Dollar      |
| Paris   | 38.20980 | -84.252987 | Paris, Kentucky, United States of America | United States Dollar      |
| Paris   | 36.30195 | -88.325858 | Paris, TN 38242, United States of America | United States Dollar      |
| Paris   | 39.61115 | -87.696137 | Paris, IL 61944, United States of America | United States Dollar      |
| Paris   | 44.25995 | -70.500641 | Paris, Maine, United States of America    | United States Dollar      |
| Paris   | 35.29203 | -93.729917 | Paris, AR 72855, United States of America | United States Dollar      |
| Paris   | 39.48087 | -92.001281 | Paris, MO 65275, United States of America | United States Dollar      |

The RMarkdown file that generated this post is available [here](https://github.com/jessecambon/jessecambon.github.io/blob/main/_posts/2021-04-19-tidygeocoder-1-0-3.Rmd).
