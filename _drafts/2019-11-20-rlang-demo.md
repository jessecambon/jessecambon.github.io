---
layout: post
title:  "Quasiquotation Demo"
date:   2019-11-18
tags: test
output: 
  md_document:
    variant: gfm
    preserve_yaml: TRUE
---

Creating a basic function

``` r
library(dplyr)
```

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

``` r
# Get top x rows after sorting by variable var
get_stats <- function(data,group_var,measure_var) {
  measure_name <- quo_name(enquo(measure_var))
  return( 
    data %>% group_by({{group_var}}) %>%
            summarize( !!str_c(measure_name,"_max") := max({{measure_var}}),
                       !!str_c(measure_name,"_min") := min({{measure_var}})) 
    )
}

cyl_hp_stats <- mtcars %>% get_stats(cyl,hp)
```

``` r
kable(cyl_hp_stats)
```

| cyl | hp\_max | hp\_min |
| --: | ------: | ------: |
|   4 |     113 |      52 |
|   6 |     175 |     105 |
|   8 |     335 |     150 |

Creating a function with a list argument. Return mean horsepower with a
list of group by variables.

``` r
hp_calc <- function(data,group_vars,measure_var) {
  group_vars <- rlang::syms(group_vars)
  return(data %>% group_by(!!!group_vars) %>%
           summarize(n=n(),
                     variable=quo_name(enquo(measure_var)),
                     mean=mean({{measure_var}}),
                     min=min({{measure_var}}),
                     max=max({{measure_var}}))
  )
}
 
gear_hp <- mtcars %>% hp_calc(c('gear'),hp) 
vs_am_hp <- mtcars %>% hp_calc(c('vs','am'),cyl) 
```

``` r
kable(gear_hp)
```

| gear |  n | variable |     mean | min | max |
| ---: | -: | :------- | -------: | --: | --: |
|    3 | 15 | hp       | 176.1333 |  97 | 245 |
|    4 | 12 | hp       |  89.5000 |  52 | 123 |
|    5 |  5 | hp       | 195.6000 |  91 | 335 |

``` r
kable(vs_am_hp)
```

| vs | am |  n | variable |     mean | min | max |
| -: | -: | -: | :------- | -------: | --: | --: |
|  0 |  0 | 12 | cyl      | 8.000000 |   8 |   8 |
|  0 |  1 |  6 | cyl      | 6.333333 |   4 |   8 |
|  1 |  0 |  7 | cyl      | 5.142857 |   4 |   6 |
|  1 |  1 |  7 | cyl      | 4.000000 |   4 |   4 |

``` r
library(ggplot2)
ggplot(data=gear_hp) + geom_point(aes(x=gear,y=mean)) + 
  theme_classic() + ylab('Mean HP')
```

![](/rmd_images/2019-11-20-rlang-demo/unnamed-chunk-5-1.png)<!-- -->
