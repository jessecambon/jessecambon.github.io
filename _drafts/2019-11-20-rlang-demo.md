---
layout: post
title:  "Testing a Draft"
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
#deparse(substitute(measure_var))
#print(quo_name(enquo(measure_var)))
  measure_name <- quo_name(enquo(measure_var))
  #label <- str_c(deparse(substitute(measure_var)),"_max")
  
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

Creating a function with a list argument

``` r
hp_calc <- function(data,variables) {
  variables <- rlang::syms(variables)
  
  return(data %>% group_by(!!!variables) %>%
           summarize(n=n(),
                     mean_hp=mean(hp),
                     min_hp=min(hp),
                     max_hp=max(hp))
         )
}
 
gear_hp <- mtcars %>% hp_calc(c('gear')) 
vs_am_hp <- mtcars %>% hp_calc(c('vs','am')) 
```

``` r
kable(gear_hp)
```

| gear |  n | mean\_hp | min\_hp | max\_hp |
| ---: | -: | -------: | ------: | ------: |
|    3 | 15 | 176.1333 |      97 |     245 |
|    4 | 12 |  89.5000 |      52 |     123 |
|    5 |  5 | 195.6000 |      91 |     335 |

``` r
kable(vs_am_hp)
```

| vs | am |  n |  mean\_hp | min\_hp | max\_hp |
| -: | -: | -: | --------: | ------: | ------: |
|  0 |  0 | 12 | 194.16667 |     150 |     245 |
|  0 |  1 |  6 | 180.83333 |      91 |     335 |
|  1 |  0 |  7 | 102.14286 |      62 |     123 |
|  1 |  1 |  7 |  80.57143 |      52 |     113 |

``` r
library(ggplot2)
ggplot(data=gear_hp) + geom_point(aes(x=gear,y=mean_hp))
```

![](//home/cambonator/Programming/jessecambon.github.io/rmd_images/2019-11-20-rlang-demo/unnamed-chunk-5-1.png)<!-- -->
