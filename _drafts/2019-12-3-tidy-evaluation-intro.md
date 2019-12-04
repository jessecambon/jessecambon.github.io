---
layout: post
title:  "Introduction to Tidy Evaluation"
date:   2019-11-18
tags: test
output: 
  md_document:
    variant: gfm
    preserve_yaml: TRUE
---

[Tidy evaluation](https://tidyeval.tidyverse.org/) is a framework for
writing more efficient and elegant code with
[tidyverse](https://www.tidyverse.org/) functions. More specifically
this framework provides a set of functions contained in the [rlang
package](https://rlang.r-lib.org/) which allow you to control how
expressions and variables in your code are evaluated by tidyverse
functions.

While tidy evaluation is a powerful tool for R developers, it also might
be difficult to wrap your head around especially if you’re new to R or
the tidyverse. This is an area of R that has undergone [a number of
development phases](https://rlang.r-lib.org/reference/lifecycle.html)
and much of the material I’ve found probably isn’t very accessible to a
newer R user. The goal of this tutorial is to concisely and accessibly
demonstrate how tidy evaluation can be used and to give you intuition on
using this framework in your own code.

To begin, let’s consider a simple motivating example with the [mtcars
dataset](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/mtcars.html).
Below we calculate maximum and minimum horsepower (hp) by the number of
cylinders (cyl) using the “group\_by” and “summarize” functions from
[dplyr](https://dplyr.tidyverse.org/).

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

Now let’s say we wanted to repeat this calculation multiple times while
changing which variable we group by. A brute force way to accomplish
this would be to copy and paste our code as many times as necessary, but
that’s inefficient especially if our code is complicated, requires many
iterations, or needs to be updated frequently. To avoid this inelegant
solution you might think to store the name of a variable inside of a
variable like this `groupby_var <- "vs"`. Then you could attempt to use
your newly created “groupby\_var” variable in your code (ie.
`group_by(groupby_var)`.

However, if you try this you will find it doesn’t work. The “group\_by”
function expects the name of the variable you want to group by as an
input, not a variable containing the name of the variable you want to
group by. This is the type of problem that tidy evaluation is built to
solve. In the example below we use the
[quo](https://rlang.r-lib.org/reference/quotation.html) function and the
[\!\!](https://rlang.r-lib.org/reference/nse-force.html) operator to
pass “vs” as our group by variable to the “group\_by” function.

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

If our code were more complex and referenced our group by variable many
times, we now have a method to set this variable by modifying the input
to “quo”. This has some utility, but if we want to utilize code like
this repeatedly in a script, we might want to turn it into a function.
To do this we will still use the “\!\!” operator but we will now use the
[enquo](https://rlang.r-lib.org/reference/nse-defuse.html) function
instead of “quo”. Below we define this function and call it using “am”
as our group by variable.

``` r
car_stats <- function(groupby_var,measure_var) {
  groupby_var <- enquo(groupby_var)
  measure_var <- enquo(measure_var)
  return(mtcars %>% 
    group_by(!!groupby_var) %>%
    summarize(!!measure_var := mean(!!measure_var),
              max=max(!!measure_var),
              min=min(!!measure_var)) %>%
      mutate(measure_var = as_label(measure_var)))
}
hp_by_am <- car_stats(am,hp)
```

| am |       hp |      max |      min | measure\_var |
| -: | -------: | -------: | -------: | :----------- |
|  0 | 160.2632 | 160.2632 | 160.2632 | hp           |
|  1 | 126.8462 | 126.8462 | 126.8462 | hp           |

Now we have a function we can use to easily change our group\_by
variable with no copy-and-pasting of code. As you might suspect, I am
just using the “group\_by” function as an example, but you could use
very similar code to what we have developed above with other tidyverse
functions. As an example, here is a function that takes a dataset and
two variable names as inputs and builds a scatterplot with
[ggplot2](https://ggplot2.tidyverse.org/). You will notice that the data
argument needs no tidy evaluation, only the x and y variables. We also
use the [as\_label](https://rlang.r-lib.org/reference/as_label.html)
function to extract our variable names as strings to create plot title
using the “ggtitle” function.

``` r
library(ggplot2)
scatter_plot <- function(df,x_var,y_var) {
  x_var <- enquo(x_var)
  y_var <- enquo(y_var)
  
return(ggplot(data=df,aes(x=!!x_var,y=!!y_var)) + 
  geom_point() + 
  theme_bw() +
  geom_smooth() +
  ggtitle(str_c(as_label(y_var), " vs ",as_label(x_var)))
  )
}
scatter_plot(mtcars,disp,hp)
```

    ## `geom_smooth()` using method = 'loess' and formula 'y ~ x'

![](/rmd_images/2019-12-3-tidy-evaluation-intro/unnamed-chunk-7-1.png)<!-- -->

As you can see, we’ve plotted the “hp” (horsepower) variable against
“disp” (displacement) and added a regression line. Instead of copying
and pasting ggplot code to create the same plot with different datasets
and variables, we can just call our function.

Now to wrap things up, one last trick I will demonstrate is how to pass
a list of variables using the syms function. This allows us to make a
similar function to the dplyr code we used above which now allows us to
group by multiple variables. One quirk is that to use the syms function
we will need to pass the variable names in quotes as shown below.

``` r
get_stats <- function(data,groupby_vars,measure_var) {
  groupby_vars <- syms(groupby_vars)
  measure_name <- as_label(enquo(measure_var))
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

## Archive

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
