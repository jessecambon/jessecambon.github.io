---
layout: post
title:  "How to Create An R Package"
#date:   2019-11-11
tags: draft
---

### Intro

How to create an R package.

### Getting Started
* [Install R-Studio](https://rstudio.com/products/rstudio/)
* We will be generating our documentation with [roxygen2](https://cran.rstudio.com/web/packages/roxygen2/index.html)

### File Layout

Files in root (/) directory:
* DESCRIPTION: Contains important infornation about your package such as dependencies, author info, and your license.
* .Rbuildignore: list files and folders you do not want to include in your R package. Include files and directories such as `data-raw` and `README.md`.
* projectname.Rproj

Main Folders:
* R: 
* data
* man
* tests
* vignettes



### Resources
* General Instructions: http://r-pkgs.had.co.nz/
* More general instructions: https://rstats-pkgs.readthedocs.io
* roxygen2 : https://cran.r-project.org/web/packages/roxygen2/
* Devtools cheat sheet: https://www.rstudio.com/wp-content/uploads/2015/03/devtools-cheatsheet.pdf


