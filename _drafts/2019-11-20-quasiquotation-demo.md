---
layout: post
title:  "Quasiquotation Demystified"
date:   2019-11-18
tags: test
output: 
  md_document:
    variant: gfm
    preserve_yaml: TRUE
---

[Quasiquotation](https://rlang.r-lib.org/reference/quasiquotation.html)
is a somewhat intimidating term for useful concept that will allow you
to write more elegant and customizable dplyr-based code and functions.
The purpose of this post is to demystify quasiquotation and show you how
you can put it to use in your code.

To begin, let’s consider a simple example in dplyr with the mtcars
dataset. Here we calculate the maximum and minimum horsepower (hp) by
the number of cylinders (cyl) using the “group\_by” and “summarize”
functions.

``` r
library(dplyr)
hp_by_cyl <- mtcars %>% 
  group_by(cyl) %>%
  summarize(max_hp=max(hp),
            min_hp=min(hp))
```

| cyl | max\_hp | min\_hp |
| --: | ------: | ------: |
|   4 |     113 |      52 |
|   6 |     175 |     105 |
|   8 |     335 |     150 |

This code works well enough, but let’s say we wanted to change the group
by variable so that we could, for example, calculate maximum and minimum
hp by the `vs` (engine type) or `am` (transmission) variables. One way
to accomplish this would be to copy and paste the above code and then
manually change the group by variable. However, this isn’t a particular
elegant or efficient solution particularly with more complicated code or
in situations where we’d like to iterate through several different
variables.

Another approach might be to store that name of a new group by variable
in a variable like this `groupby_var <- "vs"` and then use `groupby_var`
in our code (ie. `group_by(groupby_var)`. However, if you were to try
this you would find it doesn’t work because of the way dplyr works. The
group\_by function expects the variable (or variables) you want to
aggregate by as inputs. It does not expect the variable names to be in
quotes and it doesn’t expect you to give it a variable that contains the
name of the variable you want to aggregate by.

Essentially, we need a way to tell the group\_by function to look at the
value stored in `groupby_var` and use that value as a variable name.
This is the type of operation that quasiquotation is built for. In the
example below we use the
[quo](https://rlang.r-lib.org/reference/quotation.html) function and the
`!!` operator from rlang to accomplish this objective.

``` r
groupby_var <- quo(vs)

hp_by_vs <- mtcars %>% 
  group_by(!!groupby_var) %>%
  summarize(max_hp=max(hp),
            min_hp=min(hp))
```

| vs | max\_hp | min\_hp |
| -: | ------: | ------: |
|  0 |     335 |      91 |
|  1 |     123 |      52 |

Using this code, we can now modify our groupby\_var as needed to
aggregate by whatever variables we like without copy and pasting code.
If we writing this code for experimental purposes then this might be
good enough. However, if we wanted to call this code multiple times in
the same script then we should turn it into a function. To do this, the
main modification we have to make is to use the enquo function instead
of the quo function.

``` r
max_min_hp <- function(groupby_var) {
  groupby_var <- enquo(groupby_var)
  return(mtcars %>% 
    group_by(!!groupby_var) %>%
    summarize(max_hp=max(hp),
              min_hp=min(hp)))
}
hp_by_am <- max_min_hp(am)
```

| am | max\_hp | min\_hp |
| -: | ------: | ------: |
|  0 |     245 |      62 |
|  1 |     335 |      52 |

Now let’s say we wanted to customize this function even further. Let’s
make it so that our function can use one or multiple variables for
group\_by and let’s make the measurement variable (hp in the above
examples) an input to the function.

``` r
get_stats <- function(data,groupby_vars,measure_var) {
  groupby_vars <- rlang::syms(groupby_vars)
  measure_name <- quo_name(enquo(measure_var))
  return( 
    data %>% group_by(!!!groupby_vars) %>%
            summarize( !!str_c(measure_name,"_max") := max({{measure_var}}),
                       !!str_c(measure_name,"_min") := min({{measure_var}})) 
    )}
cyl_hp_stats <- mtcars %>% get_stats("cyl",mpg)
gear_stats <- mtcars %>% get_stats(c("am","vs"),gear)
```

| cyl | mpg\_max | mpg\_min |
| --: | -------: | -------: |
|   4 |     33.9 |     21.4 |
|   6 |     21.4 |     17.8 |
|   8 |     19.2 |     10.4 |

| am | vs | gear\_max | gear\_min |
| -: | -: | --------: | --------: |
|  0 |  0 |         3 |         3 |
|  0 |  1 |         4 |         3 |
|  1 |  0 |         5 |         4 |
|  1 |  1 |         5 |         4 |

Creating a function with a list argument. Return mean horsepower with a
list of group by variables.

``` r
metric_calc <- function(data,group_vars,measure_var) {
  group_vars <- rlang::syms(group_vars)
  return(data %>% group_by(!!!group_vars) %>%
           summarize(n=n(),
                     variable=quo_name(enquo(measure_var)),
                     mean=mean({{measure_var}}),
                     min=min({{measure_var}}),
                     max=max({{measure_var}}))
  )
}
 
gear_hp <- mtcars %>% metric_calc(c('gear'),hp) 
vs_am_hp <- mtcars %>% metric_calc(c('vs','am'),cyl) 
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

![](/rmd_images/2019-11-20-quasiquotation-demo/unnamed-chunk-11-1.png)<!-- -->

Experimental:

``` r
get_stats <- function(data,groupby_vars,measure_var) {
  
  measure_name <- quo_name(enquo(measure_var))
  return( 
    data %>% group_by_at(groupby_vars) %>%
            summarize( !!str_c(measure_name,"_max") := max({{measure_var}}),
                       !!str_c(measure_name,"_min") := min({{measure_var}})) 
    )
}

#test1 <- mtcars %>% get_stats(cyl,mpg)
test2 <- mtcars %>% get_stats(vars(cyl,am),gear)
```

| cyl | am | gear\_max | gear\_min |
| --: | -: | --------: | --------: |
|   4 |  0 |         4 |         3 |
|   4 |  1 |         5 |         4 |
|   6 |  0 |         4 |         3 |
|   6 |  1 |         5 |         4 |
|   8 |  0 |         3 |         3 |
|   8 |  1 |         5 |         5 |
