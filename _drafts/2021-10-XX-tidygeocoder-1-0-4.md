---
layout: post
title: "Tidygeocoder 1.0.4"
date: 2021-10-12
author: Jesse Cambon
tags: [r, tidygeocoder]
image: "/images/tidygeocoder_hex_dark2021.png"
output: 
  md_document:
    pandoc_args: ["--wrap=none"]
    variant: gfm
    preserve_yaml: TRUE
---

[Tidygeocoder v1.0.4](https://jessecambon.github.io/tidygeocoder/) is now released on [CRAN](https://cran.r-project.org/package=tidygeocoder)! This release adds support for the [Geoapify geocoding service](https://www.geoapify.com/geocoding-api) (thanks [Daniel Possenriede](https://github.com/dpprdan)!), a progress bar, and new functions for combining multiple geocoding queries. A more detailed overview is available in the [changelog](https://jessecambon.github.io/tidygeocoder/news/index.html).

Progress bars are now shown for single input geocoding (ie. not batch geocoding):

<img src="/../images/tidygeocoder_progress_bar_v104.gif" width="70%" style="display: block; margin: auto;" />

### Combining Multiple Queries

In past releases of the package, `method = "cascade"` could be used in the `geo()` and `geocode()` functions to combine the results of geocoding queries from two different services. The “cascade” method is now deprecated in favor of two new and more flexible functions: `geocode_combine()` and `geo_combine()`. These functions allow for executing and combing the results of more than two queries and they allow the queries to be customized as needed.

To demonstrate the utility of these new functions, below I’ve assembled a dataset of addresses to be geocoded. The first 5 entries are street level addresses in the United States that can be geocoded with the US Census geocoding service. However, three of these addresses will not return results with the US Census batch service (see [issue \#87 for details](https://github.com/jessecambon/tidygeocoder/issues/87)) and must instead be geocoded with the US Census single address geocoder. Additionally, the last three addresses are cities outside the United States and require a different geocoding service entirely (the US Census service is limited to the United States).

``` r
library(tidyverse)
library(tidygeocoder)

mixed_addresses <- tribble(
  ~street_address, ~city, ~state_cd, ~zip_cd,
  "624 W DAVIS ST #1D",   "BURLINGTON", "NC",  27215,
  "201 E CENTER ST #268", "MEBANE",     "NC",  27302,
  "7833  WOLFE LN",       "SNOW CAMP",  "NC",  27349,
  "202 C St",             "San Diego",  "CA",  92101,
  "121 N Rouse Ave",      "Bozeman",    "MT",  59715
) %>%
  bind_rows(
    tibble(city = c('Taipei', 'Moscow', 'Buenos Aires'))
  )
```

If we wanted to geocode a large dataset with these types of addresses, we might first try to find as many as possible via the US Census batch service, then attempt the remaining addresses with the US Census single address geocoder, and then finally send any remaining unfound addresses to another service.

While you could manually execute these queries and combine the results, the `geocode_combine()` streamlines the process. The function accepts a dataframe input and a list of queries provided as lists (ie. a list of lists). Each list in the `queries` argument contains parameters that are passed to the `geocode()` function. Optionally, the `query_names` argument can be used to label the results of the queries.

``` r
results <- mixed_addresses %>%
  geocode_combine(
    queries = list(
      list(method = 'census', mode = 'batch', 
        street = 'street_address', city = 'city', state = 'state_cd', postalcode = 'zip_cd'),
      list(method = 'census', mode = 'single',
           street = 'street_address', city = 'city', state = 'state_cd', postalcode = 'zip_cd'),
      list(method = 'arcgis', address = 'city')
    ),
    query_names = c('census - batch', 'census - single', 'arcgis')
  )
```

    ## 

    ## Passing 8 addresses to the US Census batch geocoder

    ## Query completed in: 2 seconds

    ## Passing 6 addresses to the US Census single address geocoder

    ## Query completed in: 7.6 seconds

    ## Passing 3 addresses to the ArcGIS single address geocoder

    ## Query completed in: 0.6 seconds

| street\_address       | city         | state\_cd | zip\_cd |       lat |       long | query           |
|:----------------------|:-------------|:----------|--------:|----------:|-----------:|:----------------|
| 624 W DAVIS ST \#1D   | BURLINGTON   | NC        |   27215 |  36.09598 |  -79.44453 | census - single |
| 201 E CENTER ST \#268 | MEBANE       | NC        |   27302 |  36.09683 |  -79.26977 | census - single |
| 7833 WOLFE LN         | SNOW CAMP    | NC        |   27349 |  35.89866 |  -79.43713 | census - single |
| 202 C St              | San Diego    | CA        |   92101 |  32.71676 | -117.16283 | census - batch  |
| 121 N Rouse Ave       | Bozeman      | MT        |   59715 |  45.68066 | -111.03203 | census - batch  |
| NA                    | Taipei       | NA        |      NA |  25.03737 |  121.56355 | arcgis          |
| NA                    | Moscow       | NA        |      NA |  55.75696 |   37.61502 | arcgis          |
| NA                    | Buenos Aires | NA        |      NA | -34.60849 |  -58.37344 | arcgis          |

By default the results of the queries are combined into a single dataframe as shown above. However, the results of each query can be returned as separate list items by setting `return_list = TRUE`. Additionally, only addresses that yield no results are passed to the subsequent query specified in the `queries` parameter, but setting `cascade = FALSE` will send all addresses to all queries.

The R Markdown file that generated this post is available [here](https://github.com/jessecambon/jessecambon.github.io/blob/main/_posts/2021-04-19-tidygeocoder-1-0-3.Rmd).
