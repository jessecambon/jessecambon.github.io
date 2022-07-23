---
layout: post
title: "Tidygeocoder 1.0.2"
date: 2021-01-18
author: Jesse Cambon
tags: [r, tidygeocoder]
image: "/images/google_map_pin.png"
rmarkdown_link: true
output: 
  md_document:
    pandoc_args: ["--wrap=none"]
    variant: gfm
    preserve_yaml: TRUE 
---

[Tidygeocoder v1.0.2](https://jessecambon.github.io/tidygeocoder/index.html) *“Yodeling Yak”* is now on [CRAN](https://cran.r-project.org/package=tidygeocoder). This release adds support for the popular [Google geocoder service](https://developers.google.com/maps/documentation/javascript/geocoding) (thanks [@chris31415926535](https://github.com/chris31415926535)) and also includes several bugfixes and enhancements. Refer to the [changelog](https://jessecambon.github.io/tidygeocoder/news/index.html) for details on the release and to the [tidygeocoder homepage](https://jessecambon.github.io/tidygeocoder/#geocoder-services) for a comparison of all supported geocoder services.

<img src="/../images/google_map_pin.png" width="25%" style="display: block; margin: auto;" />

You can make use of the Google geocoder service by passing `method = 'google'` to the [`geo()`](https://jessecambon.github.io/tidygeocoder/reference/geo.html) and [`geocode()`](https://jessecambon.github.io/tidygeocoder/reference/geocode.html) functions. Note that the Google geocoder service requires registering for an API key and [charges per query](https://developers.google.com/maps/documentation/geocoding/usage-and-billing). The Google API key needs to be stored in the `GOOGLEGEOCODE_API_KEY` environmental variable for use with tidygeocoder.

Also new in this release, US Census batch geocoding results will now return geographic FIPs codes in character format (instead of numeric) to preserve leading zeros ([\#47](https://github.com/jessecambon/tidygeocoder/issues/47)). The `return_type = 'geographies'` query in the [usage example](https://jessecambon.github.io/tidygeocoder/index.html#usage) shows the new data format.

Additionally, arguments passed to the [`geo()`](https://jessecambon.github.io/tidygeocoder/reference/geo.html) and [`geocode()`](https://jessecambon.github.io/tidygeocoder/reference/geocode.html) functions that aren’t valid for the selected geocoder service (ie. the Census geocoder doesn’t have a `country` argument) will now throw errors:

``` r
library(tidygeocoder)

geo(city = 'Auckland', country = 'New Zealand', method = 'census')
```

    ## Error in geo(city = "Auckland", country = "New Zealand", method = "census"): The following parameter(s) are not supported for the "census" method:
    ## 
    ## country
    ## 
    ## See ?api_parameter_reference for more details.

If you’re interested in contributing to the package and would like to add support for other geocoder services, updated instructions on how to go about this are [located here](https://github.com/jessecambon/tidygeocoder/issues/62#issue-777707424).
