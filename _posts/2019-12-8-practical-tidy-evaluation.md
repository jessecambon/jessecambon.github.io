---
layout: post
title:  "Practical Tidy Evaluation"
date:   2019-12-8
author: Jesse Cambon
tags: [r, tidyverse, data-science]
output: 
  md_document:
    variant: gfm
    preserve_yaml: TRUE
---

Tidy evaluation is a framework for controlling how expressions and
variables in your code are evaluated by
[tidyverse](https://www.tidyverse.org/) functions. This framework,
housed in the [rlang package](https://rlang.r-lib.org), is a powerful
tool for writing more efficient and elegant code. In particular, you’ll
find it useful for passing variable names as inputs to functions that
use tidyverse packages like [dplyr](https://dplyr.tidyverse.org/) and
[ggplot2](https://ggplot2.tidyverse.org/).

The goal of this post is to offer accessible examples and intuition for
putting tidy evaluation to work in your own code. Because of this I will
keep conceptual explanations brief, but for more comprehensive
documentation you can refer to [dplyr’s
website](https://dplyr.tidyverse.org/reference/tidyeval.html), [rlang’s
website](https://rlang.r-lib.org/), the [‘Tidy Evaluation’
book](https://tidyeval.tidyverse.org/) by Lionel Henry and Hadley
Wickham, and the [Metaprogramming Section of the ‘Advanced R’
book](https://adv-r.hadley.nz/metaprogramming.html) by Hadley Wickham.

### Motivating Example

To begin, let’s consider a simple example of calculating summary
statistics with the [mtcars
dataset](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/mtcars.html).
Below we calculate maximum and minimum horsepower (hp) by the number of
cylinders (cyl) using the
[group\_by](https://dplyr.tidyverse.org/reference/group_by.html) and
[summarize](https://dplyr.tidyverse.org/reference/summarise.html)
functions from [dplyr](https://dplyr.tidyverse.org/).

``` r
library(dplyr)
hp_by_cyl <- mtcars %>% 
  group_by(cyl) %>%
  summarize(min_hp=min(hp),
            max_hp=max(hp))
```

| cyl | min\_hp | max\_hp |
| --: | ------: | ------: |
|   4 |      52 |     113 |
|   6 |     105 |     175 |
|   8 |     150 |     335 |

Now let’s say we wanted to repeat this calculation multiple times *while
changing which variable we group by*. A brute force method to accomplish
this would be to copy and paste our code as many times as necessary and
modify the group by variable in each iteration. However, this is
inefficient especially if our code gets more complicated, requires many
iterations, or requires further development.

To avoid this inelegant solution you might think to store the name of a
variable inside of another variable like this `groupby_var <- "vs"`.
Then you could attempt to use your newly created “groupby\_var” variable
in your code: `group_by(groupby_var)`. However, if you try this you will
find it doesn’t work. The “group\_by” function expects the name of the
variable you want to group by as an input, not the name of a variable
that *contains* the name of the variable you want to group by.

This is the kind of headache that tidy evaluation can help you solve. In
the example below we use the
[quo](https://rlang.r-lib.org/reference/quotation.html) function and the
“bang-bang” [\!\!](https://rlang.r-lib.org/reference/nse-force.html)
operator to set “vs” (engine type, 0 = automatic, 1 = manual) as our
group by variable. The “quo” function allows us to store the variable
name in our “groupby\_var” variable and “\!\!” extracts the stored
variable name.

``` r
groupby_var <- quo(vs)

hp_by_vs <- mtcars %>% 
  group_by(!!groupby_var) %>%
  summarize(min_hp=min(hp),
            max_hp=max(hp))
```

| vs | min\_hp | max\_hp |
| -: | ------: | ------: |
|  0 |      91 |     335 |
|  1 |      52 |     123 |

The code above provides a method for setting the group by variable by
modifying the input to the “quo” function when we define “groupby\_var”.
This can be useful, particularly if we intend to reference the group by
variable multiple times. However, if we want to use code like this
repeatedly in a script then we should consider packaging it into a
function. This is what we will do next.

### Making Functions with Tidy Evaluation

To use tidy evaluation in a function, we will still use the “\!\!”
operator as we did above, but instead of “quo” we will use the
[enquo](https://rlang.r-lib.org/reference/nse-defuse.html) function. Our
new function below takes the group by variable and the measurement
variable as inputs so that we can now calculate maximum and minimum
values of any variable we want. Also note two new features I have
introduced in this function:

  - The [as\_label](https://rlang.r-lib.org/reference/as_label.html)
    function extracts the string value of the “measure\_var” variable
    (“hp” in this case). We use this to set the value of the
    “measure\_var” column.
  - The “walrus operator”
    [:=](https://rlang.r-lib.org/reference/quasiquotation.html#forcing-names)
    is used to create a column named after the variable name stored in
    the “measure\_var” argument (“hp” in the example). The walrus
    operator allows you to use strings and evaluated variables (such as
    “measure\_var” in our example) on the left hand side of an
    assignment operation (where there would normally be a “=” operator)
    in functions such as “mutate” and “summarize”.

Below we define our function and use it to group by “am” (transmission
type, 0 = automatic, 1 = manual) and calculate summary statistics with
the “hp” (horsepower) variable.

``` r
car_stats <- function(groupby_var,measure_var) {
  groupby_var <- enquo(groupby_var)
  measure_var <- enquo(measure_var)
  return(mtcars %>% 
    group_by(!!groupby_var) %>%
    summarize(min=min(!!measure_var),
              max=max(!!measure_var)) %>%
          mutate(measure_var = as_label(measure_var),
            !!measure_var := NA)
    )
}
hp_by_am <- car_stats(am,hp)
```

| am | min | max | measure\_var | hp |
| -: | --: | --: | :----------- | :- |
|  0 |  62 | 245 | hp           | NA |
|  1 |  52 | 335 | hp           | NA |

We now have a flexible function that contains a dplyr workflow. You can
experiment with modifying this function for your own purposes.
Additionally, as you might suspect, you could use the same tidy
evaluation functions we just used with tidyverse packages other than
dplyr.

As an example, below I’ve defined a function that builds a scatter plot
with [ggplot2](https://ggplot2.tidyverse.org/). The function takes a
dataset and two variable names as inputs. You will notice that the
dataset argument “df” needs no tidy evaluation. The
[as\_label](https://rlang.r-lib.org/reference/as_label.html) function is
used to extract our variable names as strings to create a plot title
with the “ggtitle” function.

``` r
library(ggplot2)
scatter_plot <- function(df,x_var,y_var) {
  x_var <- enquo(x_var)
  y_var <- enquo(y_var)
  
  return(ggplot(data=df,aes(x=!!x_var,y=!!y_var)) + 
  geom_point() + theme_bw() + 
  theme(plot.title = element_text(lineheight=1, face="bold",hjust = 0.5)) +
  geom_smooth() +
  ggtitle(str_c(as_label(y_var), " vs. ",as_label(x_var)))
  )
}
scatter_plot(mtcars,disp,hp)
```

![](/rmd_images/2019-12-8-practical-tidy-evaluation/unnamed-chunk-7-1.png)<!-- -->

As you can see, we’ve plotted the “hp” (horsepower) variable against
“disp” (displacement) and added a regression line. Now, instead of
copying and pasting ggplot code to create the same plot with different
datasets and variables, we can just call our function.

### The “Curly-Curly” Shortcut and Passing Multiple Variables

To wrap things up, I’ll cover a few additional tricks and shortcuts for
your tidy evaluation toolbox.

  - The “curly-curly” {% raw %}[{{
    }}](https://www.tidyverse.org/blog/2019/06/rlang-0-4-0/){% endraw %}
    operator directly extracts a stored variable name from
    “measure\_var” in the example below. In the prior example we
    needed both “enquo” and “\!\!” to evaluate a variable like this so
    the “curly-curly” operator is a convenient shortcut. However, note
    that if you want to extract the string variable name with the
    “as\_label” function, you will still need to use “enquo” and
    “\!\!” as we have done below with “measure\_name”.
  - The [syms](https://rlang.r-lib.org/reference/sym.html) function and
    the “\!\!\!” operator are used for passing a list of variables as a
    function argument. In prior examples “\!\!” was used to evaluate a
    single group by variable; we now use “\!\!\!” to evaluate a list of
    group by variables. One quirk is that to use the “syms” function we
    will need to pass the variable names in quotes.
  - The walrus operator “:=” is again used to create new columns, but
    now the column names are defined with a combination of a variable
    name stored in a function argument and another string ("\_min" and
    "\_max" below). We use the “enquo” and “as\_label” functions to
    extract the string variable name from “measure\_var” and store it in
    “measure\_name” and then use the “str\_c” function from
    [stringr](https://stringr.tidyverse.org/) to combine strings. You
    can use similar code to build your own column names from variable
    name inputs and strings.

Our new function is defined below and is first called to group by the
“cyl” variable and then called to group by the “am” and “vs”
variables. Note that the “\!\!\!” operator and “syms” function can be
used with either a list of strings or a single string. {% raw %}

``` r
get_stats <- function(data,groupby_vars,measure_var) {
  groupby_vars <- syms(groupby_vars)
  measure_name <- as_label(enquo(measure_var))
  return( 
    data %>% group_by(!!!groupby_vars) %>%
            summarize( !!str_c(measure_name,"_min") := min({{measure_var}}),
                       !!str_c(measure_name,"_max") := max({{measure_var}}))
    )}
cyl_hp_stats <- mtcars %>% get_stats("cyl",mpg)
gear_stats <- mtcars %>% get_stats(c("am","vs"),gear)
```

{% endraw %}

| cyl | mpg\_min | mpg\_max |
| --: | -------: | -------: |
|   4 |     21.4 |     33.9 |
|   6 |     17.8 |     21.4 |
|   8 |     10.4 |     19.2 |

| am | vs | gear\_min | gear\_max |
| -: | -: | --------: | --------: |
|  0 |  0 |         3 |         3 |
|  0 |  1 |         3 |         4 |
|  1 |  0 |         4 |         5 |
|  1 |  1 |         4 |         5 |

This concludes my introduction to tidy evaluation. Hopefully this serves
as a useful starting point for using these concepts in your own code.
