---
layout: post
title:  "Deploying RMarkdown Online"
date:   2020-1-12 
author: Jesse Cambon
tags: [ rmarkdown, data-science ]
output: 
  md_document:
    pandoc_args: ["--wrap=none"]
    variant: gfm
    preserve_yaml: TRUE
---

## The Problem

RMarkdown is powerful tool for creating documents with R code and it’s a natural choice for creating blog posts about R, such as this one. However, depending on which blog software you use, you may need to make tweaks to your RMarkdown documents to deploy them successfully.

For example, when I first used RMarkdown to create a post for this [Jekyll](https://jekyllrb.com/) blog, none of my figures (images) showed up. The issue was that my Jekyll creates an HTML file in a different location than my RMarkdown (.Rmd) and Markdown (.md) files to host the content which breaks all the relative figure paths in the Markdown file. [This blog post](http://www.randigriffin.com/2017/04/25/how-to-knit-for-mysite.html) describes the problem in more detail.

This blog post demonstrates a simple solution to this problem that I use for this blog and a GitHub repository. This solution uses a single script file (.R) which contains RMarkdown settings adjustments and is referenced from all RMarkdown (.Rmd) files. It will also allow you to control where RMarkdown saves your figure files.

By default RMarkdown stores figure images two folder levels deep using the RMarkdown file location as its root (ie. `rmdname_files/figure-gfm/image.png`). I find it more conveniant to organize figure images in a separate root directory from my RMarkdown scripts and use folder names that match the name of my RMarkdown file after the RMarkdown file that generated them (ie. `rmd_images/<rmarkdown-filename>/image.png`).

## The Workflow

Note that for the purposes of this post I will be talking about the implementation on a Jekyll blog and some modifications may be required if you are using another blog platform.

For Jekyll there are two steps to building web content with an RMarkdown file. The first is to knit the RMarkdown (.Rmd) file which creates the Markdown (.md) file. The second step is to use the [jekyll build](https://jekyllrb.com/docs/usage/) command to create HTML content which is what will be displayed online.

Steps:

> 1.  **Knit:** Rmarkdown (.Rmd) —-\> Markdown (.md)
> 2.  **Jekyll Build:** Markdown (.md) —-\> HTML (.html)

## The Solution

This solution makes some modifications to the first step (knit) so that figure image files are well organized and the HTML files display the images properly. We will use a central R script (.R) to configure RMarkdown to have customizable figure image locations and to generate figure paths that will work once our content is pushed to a GitHub repository or blog.

The following is the contents of this central R Script which I have named **rmd\_config.R** and placed in the root directory of my GitHub repository:

``` r
library(knitr)
library(stringr)
library(here)
# get name of file during knitting and strip file extension
rmd_filename <- str_remove(knitr::current_input(),"\\.Rmd")

# Figure path on disk = base.dir + fig.path
# Figure URL online = base.url + fig.path
knitr::opts_knit$set(base.dir = str_c(here::here(),'/'),base.url='/') # project root folder
knitr::opts_chunk$set(fig.path = str_c("rmd_images/",rmd_filename,'/'),echo=TRUE)
```

Here is what is going on in the above script:

  - The filename of our RMarkdown script is extracted using `knitr` and `str_remove` and stored in the variable `rmd_filename`.
  - The [here package](https://here.r-lib.org/) is used to establish our ‘base’ directory (the root folder of our GitHub repository). Since this could change based on what local system we are on, the here package allows us to automatically compensate for what root path we are in.
  - The `fig.path`, which is where our figures will be stored, is set to a folder named after the RMarkdown file being run that resides in the ‘rmd\_image’ root directory.

To utilize this above script in an RMarkdown file, we simple insert this chunk which will source the script to apply all the necessary RMarkdown settings:

``` r
library(here)
source(here::here("rmd_config.R"))
```

If you’re using Jekyll for your blog, you’ll also want to include certain YAML header content such as tags or the title of the post. To do this we can use the `preserve_yaml` setting in generating our .md file and then insert whatever yaml content we need into the header. Here is an example YAML header (the first part of your RMarkdown document) which will generate a github-style (“gfm”) .md document:

``` r
---
layout: post
title:  "Deploying RMarkdown Online"
date:   2020-1-12
author: Jesse Cambon
tags: [ rmarkdown, data-science ]
output: 
  md_document:
    pandoc_args: ["--wrap=none"]
    variant: gfm
    preserve_yaml: TRUE
---
```

Note that the ‘pandoc\_args’ setting is to prevent pandoc from inserting extra linebreaks that don’t exist in our RMarkdown file.

One other note about Jekyll is that it uses [liquid markdown](https://jekyllrb.com/docs/liquid/). This normally is not something that causes any issues, but if you want to display characters on your blog that are used by the liquid template such as `{{}}` (R’s “curly-curly” operator) then you will need to wrap these problematic characters like this: `{% raw %}{{}}{% endraw %}`. This prevents Jekyll from attempting to parse these characters as liquid syntax and they will be passed on in raw form to the HTML file for display.

## Conclusion

\<\>
