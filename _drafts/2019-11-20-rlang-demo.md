---
layout: post
title:  "Testing a Draft"
date:   2019-11-18
tags: test
output: 
  md_document:
    preserve_yaml: TRUE
---

Creating a basic function

    # Get top x rows after sorting by variable var
    get_stats <- function(data,group_var,measure_var) {
      #deparse(substitute(measure_var))
      
      label <- str_c(deparse(substitute(measure_var)),"_max")
      
      return( data %>% group_by({{group_var}}) %>%
                summarize( {{label}} := max({{measure_var}}) ))
    }

    cyl_hp_stats <- mtcars %>% get_stats(cyl,hp)

    kable(cyl_hp_stats)

<table>
<thead>
<tr class="header">
<th style="text-align: right;">cyl</th>
<th style="text-align: right;">hp_max</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: right;">4</td>
<td style="text-align: right;">113</td>
</tr>
<tr class="even">
<td style="text-align: right;">6</td>
<td style="text-align: right;">175</td>
</tr>
<tr class="odd">
<td style="text-align: right;">8</td>
<td style="text-align: right;">335</td>
</tr>
</tbody>
</table>

Creating a function with a list argument

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

    kable(gear_hp)

<table>
<thead>
<tr class="header">
<th style="text-align: right;">gear</th>
<th style="text-align: right;">n</th>
<th style="text-align: right;">mean_hp</th>
<th style="text-align: right;">min_hp</th>
<th style="text-align: right;">max_hp</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: right;">3</td>
<td style="text-align: right;">15</td>
<td style="text-align: right;">176.1333</td>
<td style="text-align: right;">97</td>
<td style="text-align: right;">245</td>
</tr>
<tr class="even">
<td style="text-align: right;">4</td>
<td style="text-align: right;">12</td>
<td style="text-align: right;">89.5000</td>
<td style="text-align: right;">52</td>
<td style="text-align: right;">123</td>
</tr>
<tr class="odd">
<td style="text-align: right;">5</td>
<td style="text-align: right;">5</td>
<td style="text-align: right;">195.6000</td>
<td style="text-align: right;">91</td>
<td style="text-align: right;">335</td>
</tr>
</tbody>
</table>

    kable(vs_am_hp)

<table>
<thead>
<tr class="header">
<th style="text-align: right;">vs</th>
<th style="text-align: right;">am</th>
<th style="text-align: right;">n</th>
<th style="text-align: right;">mean_hp</th>
<th style="text-align: right;">min_hp</th>
<th style="text-align: right;">max_hp</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: right;">0</td>
<td style="text-align: right;">0</td>
<td style="text-align: right;">12</td>
<td style="text-align: right;">194.16667</td>
<td style="text-align: right;">150</td>
<td style="text-align: right;">245</td>
</tr>
<tr class="even">
<td style="text-align: right;">0</td>
<td style="text-align: right;">1</td>
<td style="text-align: right;">6</td>
<td style="text-align: right;">180.83333</td>
<td style="text-align: right;">91</td>
<td style="text-align: right;">335</td>
</tr>
<tr class="odd">
<td style="text-align: right;">1</td>
<td style="text-align: right;">0</td>
<td style="text-align: right;">7</td>
<td style="text-align: right;">102.14286</td>
<td style="text-align: right;">62</td>
<td style="text-align: right;">123</td>
</tr>
<tr class="even">
<td style="text-align: right;">1</td>
<td style="text-align: right;">1</td>
<td style="text-align: right;">7</td>
<td style="text-align: right;">80.57143</td>
<td style="text-align: right;">52</td>
<td style="text-align: right;">113</td>
</tr>
</tbody>
</table>

    library(ggplot2)
    ggplot(data=gear_hp) + geom_point(aes(x=gear,y=mean_hp))

![](/rmd_images/2019-11-20-rlang-demo/unnamed-chunk-5-1.png)
