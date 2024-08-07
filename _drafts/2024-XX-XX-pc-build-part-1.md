---
layout: post
title: "Planning a PC Build"
date: 2024-8-6
author: Jesse Cambon
tags: [pc]
image: ""
---
## Intro

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

![Alt text goes here](/../images/godzilla-tech-interview.jpg)

Source: [Reddit](https://www.reddit.com/r/recruitinghell/comments/l6bp24/interview_level_godzilla_job_pays_10_hr/)


```python
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt

X, y = load_diabetes(return_X_y = True, as_frame = True)

sns.displot(
    X,
    x = "bmi",
    kind = 'kde'
)
```




    <seaborn.axisgrid.FacetGrid at 0x7fd82f16d7f0>




    
![png](/jupyter_files/2022-XX-XX-job-market_files/2022-XX-XX-job-market_4_1.png)
    

