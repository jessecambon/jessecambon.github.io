---
layout: post
title:  "Essential Data Science Workflows"
date:   2019-12-8
author: Jesse Cambon
tags: [ tidyverse, data-science]
output: 
  md_document:
    pandoc_args: ["--wrap=none"]
    variant: gfm
    preserve_yaml: TRUE
---

The workflows that data scientists use can vary widely depending on the objectives of the work and data being used. However, there are some common operations that you are likely to use repeatedly in a wide variety of contexts. This post will illustrate these “essential” data science workflows with inbuilt datasets. If you’re new to R, data science, or the [tidyverse](https://www.tidyverse.org/) and you want to quickly learn some useful data science workflows then this post is written for you.

I will mainly rely on the [dplyr](https://dplyr.tidyverse.org/), [tidyr](https://tidyr.tidyverse.org/), and [stringr](https://stringr.tidyverse.org/) packages which all have excellent documentation that you can refer to for further details. Because this post uses inbuilt datasets, I will *not* cover importing data from files. If you need to import your data, refer to the [readr](https://readr.tidyverse.org/) (for CSV and text files) or [readxl](https://readxl.tidyverse.org/) (for excel spreadsheets) packages.

## Basic Data Manipulation

``` r
library(tidyverse)
library(ggplot2)
```

To begin, let’s take a look at the ‘mpg’ dataset from ggplot2:

| manufacturer | model | displ | year | cyl | trans      | drv | cty | hwy | fl | class   |
| :----------- | :---- | ----: | ---: | --: | :--------- | :-- | --: | --: | :- | :------ |
| audi         | a4    |   1.8 | 1999 |   4 | auto(l5)   | f   |  18 |  29 | p  | compact |
| audi         | a4    |   1.8 | 1999 |   4 | manual(m5) | f   |  21 |  29 | p  | compact |
| audi         | a4    |   2.0 | 2008 |   4 | manual(m6) | f   |  20 |  31 | p  | compact |

First we’ll perform a few of the most commonly used data manipulations on this dataset.

  - [filter](https://dplyr.tidyverse.org/reference/filter.html) controls which rows we want to keep from the input dataset. In this example three conditions are applied using the “&” (AND) operator.
  - [mutate](https://dplyr.tidyverse.org/reference/mutate.html) is used to create new columns.
  - [str\_c](https://stringr.tidyverse.org/reference/str_c.html) combines multiple strings. In this case we are combining the manufacturer and model string fields into a single field with a single space in between.
  - [select](https://dplyr.tidyverse.org/reference/select.html) is used to pick which columns we want to keep. A ‘-’ before a column indicates that we want to drop that column. The everything() function is shorthand for selecting all remaining columns and is an examle of a [select helper](https://www.rdocumentation.org/packages/dplyr/versions/0.7.3/topics/select_helpers). As you can see, this select statement sets the order of the first four columns and then includes the remaining columns while removing the manfacturer and model columns.
  - [rename](https://dplyr.tidyverse.org/reference/select.html) is used to rename the ‘fl’ column to ‘fuel\_type’

The end result of this dplyr workflow is that we have selected the two rows pertaining to 2005 Nissan vehicles with 4 cylinders, created two new columns, ordered our columns, removed two columns, and renamed a column.

``` r
mpg_subset <- mpg %>%
  filter(cyl == 4 & year >= 2005  & manufacturer == "nissan") %>%
  mutate(ratio = hwy/cty,
         make_model = str_c(manufacturer,' ',model)) %>%
  select(make_model,year,cyl,hwy,everything(),-manufacturer,-model) %>%
  rename(fuel_type = fl)
```

| make\_model   | year | cyl | hwy | displ | trans      | drv | cty | fuel\_type | class   |    ratio |
| :------------ | ---: | --: | --: | ----: | :--------- | :-- | --: | :--------- | :------ | -------: |
| nissan altima | 2008 |   4 |  31 |   2.5 | auto(av)   | f   |  23 | r          | midsize | 1.347826 |
| nissan altima | 2008 |   4 |  32 |   2.5 | manual(m6) | f   |  23 | r          | midsize | 1.391304 |

## Summary Statistics

A data scientist will often want to calculate summary statistics and metrics for a dataset. One of the simplest metrics is to count observations by a particular categorical variable. Here we find the number of rows for each value of the ‘cyl’ (cylinders) column:

``` r
count_cyl <- mpg %>%
  count(cyl)
```

| cyl |  n |
| --: | -: |
|   4 | 81 |
|   5 |  4 |
|   6 | 79 |
|   8 | 70 |

A broader variety of statistics can be calculated using the [group\_by](https://dplyr.tidyverse.org/reference/group_by.html) and [summarize](https://dplyr.tidyverse.org/reference/summarise.html) functions. In this example, we create a new categorical column “class\_c” (which combines 2 seaters and subcompact vehicles into a single category) and then calculate a variety of basic summary statistics by this column. The arrange function is used to order the rows in the dataset in descending order of the created ‘count’ variable. Note that the ungroup() function is not strictly necessary, but it is a good practice if we plan to manipulate our dataset in the future without using groups.

``` r
mpg_stats <- mpg %>% select(class,hwy) %>%
  mutate(class_c = case_when(class %in% c("2seater","subcompact") ~ "subcompact",
                               TRUE ~ class)) %>%
  group_by(class_c) %>%
  summarize(count = n(),
            max_hwy = max(hwy),
            min_hwy = min(hwy),
            median_hwy = median(hwy),
            mean_hwy = mean(hwy)) %>%
  ungroup() %>%
  arrange(desc(count)) # sort dataset
```

Note that ‘2seater’ is reclassified as ‘subcompact’

| class\_c   | count | max\_hwy | min\_hwy | median\_hwy | mean\_hwy |
| :--------- | ----: | -------: | -------: | ----------: | --------: |
| suv        |    62 |       27 |       12 |        17.5 |  18.12903 |
| compact    |    47 |       44 |       23 |        27.0 |  28.29787 |
| midsize    |    41 |       32 |       23 |        27.0 |  27.29268 |
| subcompact |    40 |       44 |       20 |        26.0 |  27.72500 |
| pickup     |    33 |       22 |       12 |        17.0 |  16.87879 |
| minivan    |    11 |       24 |       17 |        23.0 |  22.36364 |

### Stacking Data

If you have datasets whose columns or rows align, you can combine them by stacking them vertically or horizontally. In this example, we will first use the [slice](https://dplyr.tidyverse.org/reference/slice.html) function to obtain subsets of the ‘mpg’ dataset by row numbers and then stack these slices vertically and horizontally.

Initial ‘mpg’ Dataset:

| manufacturer | model | displ | year | cyl | trans      | drv | cty | hwy | fl | class   |
| :----------- | :---- | ----: | ---: | --: | :--------- | :-- | --: | --: | :- | :------ |
| audi         | a4    |   1.8 | 1999 |   4 | auto(l5)   | f   |  18 |  29 | p  | compact |
| audi         | a4    |   1.8 | 1999 |   4 | manual(m5) | f   |  21 |  29 | p  | compact |
| audi         | a4    |   2.0 | 2008 |   4 | manual(m6) | f   |  20 |  31 | p  | compact |

``` r
mpg1 <- mpg %>% slice(1:2) %>% 
  select(manufacturer,model,hwy,cty) %>%
  mutate(dataset = 1)
```

| manufacturer | model | hwy | cty | dataset |
| :----------- | :---- | --: | --: | ------: |
| audi         | a4    |  29 |  18 |       1 |
| audi         | a4    |  29 |  21 |       1 |

``` r
mpg2 <- mpg %>% slice(44:45) %>%
  select(manufacturer,model,hwy,cty) %>%
  mutate(dataset = 2)
```

| manufacturer | model       | hwy | cty | dataset |
| :----------- | :---------- | --: | --: | ------: |
| dodge        | caravan 2wd |  17 |  11 |       2 |
| dodge        | caravan 2wd |  22 |  15 |       2 |

Since these two datsets we just created, mpg1 and mpg2, have the same columns we can stack them vertically using [bind\_rows](https://dplyr.tidyverse.org/reference/bind.html):

``` r
mpg_stack_vert <- mpg1 %>% 
  bind_rows(mpg2)
```

| manufacturer | model       | hwy | cty | dataset |
| :----------- | :---------- | --: | --: | ------: |
| audi         | a4          |  29 |  18 |       1 |
| audi         | a4          |  29 |  21 |       1 |
| dodge        | caravan 2wd |  17 |  11 |       2 |
| dodge        | caravan 2wd |  22 |  15 |       2 |

Now let’s create third subsection of the ‘mpg’ dataset and call it ‘mpg3’:

``` r
mpg3 <- mpg %>% slice(1:2,5:6) %>%
  select(displ,year)
```

| displ | year |
| ----: | ---: |
|   1.8 | 1999 |
|   1.8 | 1999 |
|   2.8 | 1999 |
|   2.8 | 1999 |

We can stack the ‘mpg\_stack\_vert’ and ‘mpg3’ datasets horizontally since their rows align. We use the the [bind\_cols](https://dplyr.tidyverse.org/reference/bind.html) function to do this.

``` r
mpg_stack_horz <- mpg_stack_vert %>%
  bind_cols(mpg3)
```

| manufacturer | model       | hwy | cty | dataset | displ | year |
| :----------- | :---------- | --: | --: | ------: | ----: | ---: |
| audi         | a4          |  29 |  18 |       1 |   1.8 | 1999 |
| audi         | a4          |  29 |  21 |       1 |   1.8 | 1999 |
| dodge        | caravan 2wd |  17 |  11 |       2 |   2.8 | 1999 |
| dodge        | caravan 2wd |  22 |  15 |       2 |   2.8 | 1999 |

### Joining

If you have datasets that contain a common “key” column (or a set of key columns) then you can use one of the [join functions from dplyr](https://dplyr.tidyverse.org/reference/join.html) to combine these datasets.

``` r
car_type <- mpg %>% select(manufacturer,model,class) %>%
  distinct() # distinct rows only

joined <- mpg_stack_horz %>%
  left_join(car_type,by = c('manufacturer','model')) %>% 
  select(-dataset,everything())
```

### Converting Long Data to Wide

Let’s take a look at the ‘us\_rent\_income’ dataset from the tidyr package:

| GEOID | NAME    | variable | estimate | moe |
| :---- | :------ | :------- | -------: | --: |
| 01    | Alabama | income   |    24476 | 136 |
| 01    | Alabama | rent     |      747 |   3 |
| 02    | Alaska  | income   |    32940 | 508 |
| 02    | Alaska  | rent     |     1200 |  13 |

Each row of this dataset pertains to either income or rent as we can see by looking at the value of the ‘variable’ column. This is an example of a ‘long’ data format. The ‘long’ format is versatile, but sometimes we may want to convert to the ‘wide’ data format for presentation purposes. To do this, we can use the [pivot\_wider](https://tidyr.tidyverse.org/reference/pivot_wider.html) function from tidyr to put rent and income into separate columns. This function has two arguments you will need to set:

  - **names\_from**: column containing values that we will use for our new column names
  - **values\_from**: column containing the values that will populate our new columns

Additionally we use the select to drop two columns, drop\_na to remove rows with missing values, and mutate to createa income to rent ratio.

``` r
col_ratio <- us_rent_income %>%
  select(-GEOID,-moe) %>%
  pivot_wider(names_from = variable, values_from = estimate) %>% 
  drop_na() %>%   # drop missing values
  mutate(income_rent_ratio = income / (12*rent))
```

| NAME     | income | rent | income\_rent\_ratio |
| :------- | -----: | ---: | ------------------: |
| Alabama  |  24476 |  747 |            2.730478 |
| Alaska   |  32940 | 1200 |            2.287500 |
| Arizona  |  27517 |  972 |            2.359139 |
| Arkansas |  23789 |  709 |            2.796074 |

### Converting Wide Data to Long

Now let’s take a look at the ‘world\_bank\_pop’ dataset from tidyr (first 6 columns only):

| country | indicator   |         2000 |         2001 |         2002 |        2003 |
| :------ | :---------- | -----------: | -----------: | -----------: | ----------: |
| ABW     | SP.URB.TOTL | 42444.000000 | 43048.000000 | 43670.000000 | 44246.00000 |
| ABW     | SP.URB.GROW |     1.182632 |     1.413021 |     1.434559 |     1.31036 |
| ABW     | SP.POP.TOTL | 90853.000000 | 92898.000000 | 94992.000000 | 97017.00000 |

This dataset is in “wide” format since a categorical variable, in this case the year, is stored in the column names. To convert this dataset to the “long” format", which is often more versatile for data manipulations, we can use the pivot\_longer function from tidyr. This function takes three inputs:

  - **cols** (1st argument): what columns do we want to pivot? (ie. subtract ones we don’t want to)
  - **names\_to** : the name of new column which has the column names as values
  - **values\_to** : name of new column which will contain values

We also use the mutate and as.numeric() functions to convert our new ‘year’ variable to numeric and then filter so that our output dataset only includes certain years using the seq function. The format for ‘seq’ is seq(start, stop, increment).

``` r
wb_pop <- world_bank_pop %>%
  pivot_longer(c(-country,-indicator), names_to = "year", values_to = "value") %>%
  mutate(year = as.numeric(year)) %>% # convert to numeric
  filter(year %in% seq(2000,2016,2))
```

| country | indicator   | year | value |
| :------ | :---------- | ---: | ----: |
| ABW     | SP.URB.TOTL | 2000 | 42444 |
| ABW     | SP.URB.TOTL | 2002 | 43670 |
| ABW     | SP.URB.TOTL | 2004 | 44669 |

## Visualizations

### Bar Chart

  - use fill argument in ggplot() to set bar color based on a variable
  - reorder() orders the bars

<!-- end list -->

``` r
# A simple bar chart - average heights of the species
# the reorder command orders our bars in order of descending height
ggplot(data = mpg_stats,
    aes(x = reorder(class_c,-mean_hwy), y = mean_hwy)) +
geom_bar(stat = 'identity',position = 'dodge',color = 'black') +
scale_y_continuous(expand = expand_scale(mult = c(0, .1))) +    # plot margins
geom_text(aes(label = round(mean_hwy)), vjust = -0.5) +  # labelling
theme_bw() +
theme(legend.position = "none", # no legend (in case we want to use fill)
      panel.grid = element_blank()) + # turn off grid
labs(title = '') +
xlab('') +
ylab('')
```

![](/rmd_images/Essential-DataScience-R/unnamed-chunk-27-1.png)<!-- -->

``` r
# Histogram with autobinning based on gender
ggplot(mpg,aes(hwy)) +
geom_histogram(aes(fill = cyl),binwidth = 1) +
theme_bw() +
scale_y_continuous(expand = expand_scale(mult = c(0, .05))) +
xlab('Highway mpg') + ylab('Count')
```

![](/rmd_images/Essential-DataScience-R/histogram-1.png)<!-- -->

## Line

We divide the `value` field by 100 since to convert it to a decimal percentage value.

SP.POP.GROW is the % population growth

``` r
ggplot(wb_pop %>% filter(country %in% c("USA","CAN","MEX") & indicator == "SP.POP.GROW"),
          aes(x = year,y = value/100,color = country)) +
  theme_classic() +
geom_line() + geom_point() + # lines and points
scale_x_continuous(expand = expand_scale(mult = c(.05, .05))) +
scale_y_continuous(labels = scales::percent) + 
labs(title = '',
     caption = '') +
theme(legend.title = element_blank(),
      panel.grid.minor.x = element_blank(),
      legend.text = element_text(size = 10),
      legend.position = 'right') +
xlab('Year') +
ylab('Population Growth') +
# make legend items bigger
guides(colour = guide_legend(override.aes = list(size = 2))) 
```

![](/rmd_images/Essential-DataScience-R/line-1.png)<!-- -->

## Lollipop

Lollipop charts can be an attractive alternative to bar charts.

``` r
  ggplot(data = col_ratio %>% arrange(desc(rent)) %>% head(15), aes(x = NAME, y = rent) ) +
    geom_segment( aes(x = reorder(NAME,rent) ,xend = NAME, y = 0, yend = rent), color = "grey") +
    geom_point(size = 3) +
   theme_minimal() +
  theme(plot.subtitle = element_text(face = "bold",hjust = 0.5),
      plot.title = element_text(lineheight = 1, face = "bold",hjust = 0.5),
      panel.grid.minor.y = element_blank(),
      panel.grid.major.y = element_blank(),
      panel.grid.minor.x = element_blank()
    ) +
  coord_flip() +
    scale_y_continuous(labels = scales::dollar,expand = expand_scale(mult = c(0, .1))) + 
    labs(title = 'States With Highest Rent',
        caption = 'Source: 2017 American Community Survey (Census)') +
    xlab('') + ylab('Median Monthly Rent')
```

![](/rmd_images/Essential-DataScience-R/lollipop-1.png)<!-- -->
