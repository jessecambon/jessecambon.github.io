---
layout: post
title: "Introducing Tidygeocoder 1.0.0"
date: 2020-7-15
author: Jesse Cambon
tags: [r, data-science, maps]
image: "images/tidygeocoder_hex.png"
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
# reference: https://www.datanovia.com/en/blog/how-to-create-a-map-using-ggplot2/
# EU Countries
some.eu.countries <- c(
  "Portugal", "Spain", "France", "Switzerland", "Germany",
  "Austria", "Belgium", "UK", "Netherlands",
  "Denmark", "Poland", "Italy", 
  "Croatia", "Slovenia", "Hungary", "Slovakia",
  "Czech republic"
)
# Retrieve the map data
some.eu.maps <- map_data("world", region = some.eu.countries)

# Plot
ggplot(stadium_locations, aes(x = long, y = lat)) +
  borders('world', xlim = c(-10, 10), ylim = c(40, 55)) +
  geom_label_repel(aes(label = Club), force = 2, segment.alpha = 0) + 
  geom_point() + theme_void() 
```

<img src="/rmd_images/2020-07-15-tidygeocoder-1-0-0/unnamed-chunk-5-1.png" style="display: block; margin: auto;" />

Another great mapping option is the [leaflet package](https://rstudio.github.io/leaflet/), which was originally what I intended to use for the map above, but getting it to render on a [Jekyll blog](https://jekyllrb.com/) proved to be a bit involved.

If you find any issues with the package or have ideas on how to improve it, feel free to [file an issue on Github](https://github.com/jessecambon/tidygeocoder/issues). For reference, the RMarkdown file that generated this blog post can be found [here](https://github.com/jessecambon/jessecambon.github.io/tree/master/_posts/2020-07-15-tidygeocoder-1-0-0.Rmd).
