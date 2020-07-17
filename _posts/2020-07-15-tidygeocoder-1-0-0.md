---
layout: post
title: "Introducing Tidygeocoder 1.0.0"
date: 2020-7-15
author: Jesse Cambon
tags: [r, data-science, maps]
image: "images/tidygeocoder_hex.png"
linktormd: true
leafletmap: true
always_allow_html: yes
output: 
  md_document:
    pandoc_args: ["--wrap=none"]
    variant: gfm
    preserve_yaml: TRUE 
---

[Tidygeocoder v1.0.0](https://jessecambon.github.io/tidygeocoder/index.html) is now live on CRAN. There are numerous new features and improvements such as batch geocoding (submitting multiple addresses per query), returning full results from geocoder services (not just latitude and longitude), address component arguments (city, country, etc.), query customization, and reduced package dependencies.

For a full list of new features and improvements refer to the [release page on Github](https://github.com/jessecambon/tidygeocoder/releases/tag/v1.0.0). For usage examples you can reference the [Getting Started vignette](https://jessecambon.github.io/tidygeocoder/articles/tidygeocoder.html).

<img src="/../images/tidygeocoder_hex.png" width="200" style="display: block; margin: auto;" />

To demonstrate a few of the new capabilities of this package, I decided to make a map of the stadiums for the [UEFA Champions League Round of 16 clubs](https://www.uefa.com/uefachampionsleague/draws/2020/2001141/). To start, I looked up the addresses for the stadiums and put them in a dataframe.

``` r
library(dplyr)
library(tidygeocoder)
library(ggplot2)
require(maps)
library(ggrepel)

# https://www.uefa.com/uefachampionsleague/clubs/
stadiums <- tibble::tribble(
~Club,                ~Street,   ~City,   ~Country,
"Barcelona",          "Camp Nou", "Barcelona", "Spain",
"Bayern Munich",      "Allianz Arena", "Munich", "Germany",
"Chelsea",            "Stamford Bridge", "London", "UK",
"Borussia Dortmund",  "Signal Iduna Park", "Dortmund", "Germany",
"Juventus",           "Allianz Stadium", "Turin", "Italy",
"Liverpool",          "Anfield", "Liverpool", "UK",
"Olympique Lyonnais", "Groupama Stadium", "Lyon", "France",
"Man. City",          "Etihad Stadium", "Manchester", "UK",
"Napoli",             "San Paolo Stadium", "Naples", "Italy",
"Real Madrid",        "Santiago Bernabéu Stadium", "Madrid", "Spain",
"Tottenham",          "Tottenham Hotspur Stadium", "London", "UK",
"Valencia",           "Av. de Suècia, s/n, 46010", "Valencia", "Spain",
"Atalanta",           "Gewiss Stadium", "Bergamo", "Italy",
"Atlético Madrid",    "Estadio Metropolitano", "Madrid", "Spain",
"RB Leipzig",         "Red Bull Arena", "Leipzig", "Germany",
"PSG",                "Le Parc des Princes", "Paris", "France"
  )
```

To geocode these addresses, you can use the [geocode](https://jessecambon.github.io/tidygeocoder/reference/geocode.html) function as shown below. New in v1.0.0, the `street`, `city`, and `country` arguments specify the address. The Nominatim (OSM) geocoder is selected with the `method` argument. Additionally, the `full_results` and `custom_query` arguments (also new in v1.0.0) are used to return the full geocoder results and set [Nominatim’s “extratags” parameter](https://nominatim.org/release-docs/develop/api/Search/#parameters) which returns extra columns.

``` r
stadium_locations <- stadiums %>%
  geocode(street = Street, city = City, country = Country, method = 'osm', 
          full_results = TRUE, custom_query= list(extratags = 1))
```

This returns 40 columns including the longitude and latitude. A few of the columns returned due to the `extratags` argument are shown below.

``` r
stadium_locations %>%
  select(Club, City, Country, extratags.sport, extratags.capacity, extratags.operator, extratags.wikipedia) %>%
  rename_with(~gsub('extratags.', '', .)) %>%
  knitr::kable()
```

| Club               | City       | Country | sport                     | capacity | operator                      | wikipedia                         |
| :----------------- | :--------- | :------ | :------------------------ | :------- | :---------------------------- | :-------------------------------- |
| Barcelona          | Barcelona  | Spain   | soccer                    | NA       | NA                            | en:Camp Nou                       |
| Bayern Munich      | Munich     | Germany | soccer                    | 75021    | NA                            | de:Allianz Arena                  |
| Chelsea            | London     | UK      | soccer                    | 41837    | Chelsea Football Club         | en:Stamford Bridge (stadium)      |
| Borussia Dortmund  | Dortmund   | Germany | soccer                    | NA       | NA                            | de:Signal Iduna Park              |
| Juventus           | Turin      | Italy   | soccer                    | NA       | NA                            | it:Allianz Stadium (Torino)       |
| Liverpool          | Liverpool  | UK      | soccer                    | 54074    | Liverpool Football Club       | en:Anfield                        |
| Olympique Lyonnais | Lyon       | France  | soccer                    | 58000    | Olympique Lyonnais            | fr:Parc Olympique lyonnais        |
| Man. City          | Manchester | UK      | soccer                    | NA       | Manchester City Football Club | en:City of Manchester Stadium     |
| Napoli             | Naples     | Italy   | soccer                    | NA       | NA                            | en:Stadio San Paolo               |
| Real Madrid        | Madrid     | Spain   | soccer                    | 85454    | NA                            | es:Estadio Santiago Bernabéu      |
| Tottenham          | London     | UK      | soccer;american\_football | 62062    | Tottenham Hotspur             | en:Tottenham Hotspur Stadium      |
| Valencia           | Valencia   | Spain   | NA                        | NA       | NA                            | NA                                |
| Atalanta           | Bergamo    | Italy   | soccer                    | NA       | NA                            | NA                                |
| Atlético Madrid    | Madrid     | Spain   | soccer                    | NA       | NA                            | es:Estadio Metropolitano (Madrid) |
| RB Leipzig         | Leipzig    | Germany | NA                        | NA       | NA                            | de:Red Bull Arena (Leipzig)       |
| PSG                | Paris      | France  | soccer                    | 48527    | Paris Saint-Germain           | fr:Parc des Princes               |

Below, the stadium locations are plotted on a map of Europe using the longitude and latitude coordinates and ggplot.

``` r
ggplot(stadium_locations, aes(x = long, y = lat)) +
  borders('world', xlim = c(-10, 10), ylim = c(40, 55)) +
  geom_label_repel(aes(label = Club), force = 2, segment.alpha = 0) + 
  geom_point() + theme_void() 
```

<img src="/rmd_images/2020-07-15-tidygeocoder-1-0-0/unnamed-chunk-5-1.png" style="display: block; margin: auto;" />

Alternatively you can create an interactive map with the leaflet library:

``` r
library(leaflet)

stadium_locations %>% # Our dataset
  leaflet(width="100%", options = leafletOptions(attributionControl = FALSE)) %>%
  setView(lng = mean(stadium_locations$long), lat = mean(stadium_locations$lat), zoom = 5) %>%
  # Map Backgrounds
  addProviderTiles(providers$Esri.NatGeoWorldMap, group='ESRI') %>% 
  addProviderTiles(providers$Stamen.Terrain, group='Terrain') %>%
  addProviderTiles(providers$NASAGIBS.ViirsEarthAtNight2012, group='Night') %>%
  addProviderTiles(providers$Stamen.Toner, group='Stamen') %>%
  addTiles(group = "OSM") %>%
  addProviderTiles(providers$Esri.WorldTopoMap, group="Topo") %>%
  # Add Markers
  addMarkers(labelOptions = labelOptions(noHide = F), lng = ~long, lat = ~lat,
       clusterOptions = markerClusterOptions(maxClusterRadius = 10), label= ~Club,
       group="Stadiums") %>%
  # Map Control Options
  addLayersControl(baseGroups = c("ESRI", "OSM", "Stamen", "Terrain", "Topo", "Night"),
       overlayGroups=c('Stadiums'),
       options = layersControlOptions(collapsed = TRUE))
```

<div id="htmlwidget-f568007e7418b35b1d10" style="width:100%;height:480px;" class="leaflet html-widget"></div>
<script type="application/json" data-for="htmlwidget-f568007e7418b35b1d10">{"x":{"options":{"crs":{"crsClass":"L.CRS.EPSG3857","code":null,"proj4def":null,"projectedBounds":null,"options":{}},"attributionControl":false},"setView":[[46.816030234375,3.70195179384455],5,[]],"calls":[{"method":"addProviderTiles","args":["Esri.NatGeoWorldMap",null,"ESRI",{"errorTileUrl":"","noWrap":false,"detectRetina":false}]},{"method":"addProviderTiles","args":["Stamen.Terrain",null,"Terrain",{"errorTileUrl":"","noWrap":false,"detectRetina":false}]},{"method":"addProviderTiles","args":["NASAGIBS.ViirsEarthAtNight2012",null,"Night",{"errorTileUrl":"","noWrap":false,"detectRetina":false}]},{"method":"addProviderTiles","args":["Stamen.Toner",null,"Stamen",{"errorTileUrl":"","noWrap":false,"detectRetina":false}]},{"method":"addTiles","args":["//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",null,"OSM",{"minZoom":0,"maxZoom":18,"tileSize":256,"subdomains":"abc","errorTileUrl":"","tms":false,"noWrap":false,"zoomOffset":0,"zoomReverse":false,"opacity":1,"zIndex":1,"detectRetina":false,"attribution":"&copy; <a href=\"http://openstreetmap.org\">OpenStreetMap<\/a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA<\/a>"}]},{"method":"addProviderTiles","args":["Esri.WorldTopoMap",null,"Topo",{"errorTileUrl":"","noWrap":false,"detectRetina":false}]},{"method":"addMarkers","args":[[41.38089905,48.21880845,51.4816865,51.4928359,45.10965935,53.4308358,45.7653624,53.48309105,40.82797725,40.4530512,51.6041916,39.4756558,45.709222,40.43605295,51.34579105,48.8413634],[2.12292250075175,11.6246641517999,-0.191963664421104,7.45074465483453,7.64122132434347,-2.96090954141653,4.98205431107367,-2.20025200234333,14.1928889639353,-3.68754628942801,-0.0662349052591809,-0.3587826,9.68081336849461,-3.59971580972644,12.3482549226364,2.25306931623782],null,null,"Stadiums",{"interactive":true,"draggable":false,"keyboard":true,"title":"","alt":"","zIndexOffset":0,"opacity":1,"riseOnHover":false,"riseOffset":250},null,null,{"showCoverageOnHover":true,"zoomToBoundsOnClick":true,"spiderfyOnMaxZoom":true,"removeOutsideVisibleBounds":true,"spiderLegPolylineOptions":{"weight":1.5,"color":"#222","opacity":0.5},"freezeAtZoom":false,"maxClusterRadius":10},null,["Barcelona","Bayern Munich","Chelsea","Borussia Dortmund","Juventus","Liverpool","Olympique Lyonnais","Man. City","Napoli","Real Madrid","Tottenham","Valencia","Atalanta","Atlético Madrid","RB Leipzig","PSG"],{"interactive":false,"permanent":false,"direction":"auto","opacity":1,"offset":[0,0],"textsize":"10px","textOnly":false,"className":"","sticky":true},null]},{"method":"addLayersControl","args":[["ESRI","OSM","Stamen","Terrain","Topo","Night"],"Stadiums",{"collapsed":true,"autoZIndex":true,"position":"topright"}]}],"limits":{"lat":[39.4756558,53.48309105],"lng":[-3.68754628942801,14.1928889639353]}},"evals":[],"jsHooks":[]}</script>

<br>

If you find any issues with the package or have ideas on how to improve it, feel free to [file an issue on Github](https://github.com/jessecambon/tidygeocoder/issues). For reference, the RMarkdown file that generated this blog post can be found [here](https://github.com/jessecambon/jessecambon.github.io/tree/master/_posts/2020-07-15-tidygeocoder-1-0-0.Rmd).
