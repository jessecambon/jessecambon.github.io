---
layout: post
title: "Test Jupyter Post"
date: 2021-10-17
author: Jesse Cambon
tags: [python, data]
image: "/images/tidygeocoder_hex_dark2021.png"
---
### References

- [Diabetes Dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html#sklearn.datasets.load_diabetes)
- [Gradient Boosted Regression Example](https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_regression.html#sphx-glr-auto-examples-ensemble-plot-gradient-boosting-regression-py)
- [Bayesian Hyperparameter Search](https://scikit-optimize.github.io/stable/auto_examples/sklearn-gridsearchcv-replacement.html)
- [Gaussian process explanation]( https://scikit-optimize.github.io/stable/auto_examples/bayesian-optimization.html)



```python
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from skopt import BayesSearchCV
from skopt.plots import plot_objective, plot_histogram
import matplotlib.pyplot as plt
from yellowbrick.regressor import residuals_plot, prediction_error

my_seed = 42
```


```python
# Load dataset
X, y = load_diabetes(return_X_y = True, as_frame = True)

combi = pd.concat([X, y], axis = 1)

n_features = X.shape[1]
```


```python
combi
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>sex</th>
      <th>bmi</th>
      <th>bp</th>
      <th>s1</th>
      <th>s2</th>
      <th>s3</th>
      <th>s4</th>
      <th>s5</th>
      <th>s6</th>
      <th>target</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.038076</td>
      <td>0.050680</td>
      <td>0.061696</td>
      <td>0.021872</td>
      <td>-0.044223</td>
      <td>-0.034821</td>
      <td>-0.043401</td>
      <td>-0.002592</td>
      <td>0.019908</td>
      <td>-0.017646</td>
      <td>151.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-0.001882</td>
      <td>-0.044642</td>
      <td>-0.051474</td>
      <td>-0.026328</td>
      <td>-0.008449</td>
      <td>-0.019163</td>
      <td>0.074412</td>
      <td>-0.039493</td>
      <td>-0.068330</td>
      <td>-0.092204</td>
      <td>75.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.085299</td>
      <td>0.050680</td>
      <td>0.044451</td>
      <td>-0.005671</td>
      <td>-0.045599</td>
      <td>-0.034194</td>
      <td>-0.032356</td>
      <td>-0.002592</td>
      <td>0.002864</td>
      <td>-0.025930</td>
      <td>141.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-0.089063</td>
      <td>-0.044642</td>
      <td>-0.011595</td>
      <td>-0.036656</td>
      <td>0.012191</td>
      <td>0.024991</td>
      <td>-0.036038</td>
      <td>0.034309</td>
      <td>0.022692</td>
      <td>-0.009362</td>
      <td>206.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.005383</td>
      <td>-0.044642</td>
      <td>-0.036385</td>
      <td>0.021872</td>
      <td>0.003935</td>
      <td>0.015596</td>
      <td>0.008142</td>
      <td>-0.002592</td>
      <td>-0.031991</td>
      <td>-0.046641</td>
      <td>135.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>437</th>
      <td>0.041708</td>
      <td>0.050680</td>
      <td>0.019662</td>
      <td>0.059744</td>
      <td>-0.005697</td>
      <td>-0.002566</td>
      <td>-0.028674</td>
      <td>-0.002592</td>
      <td>0.031193</td>
      <td>0.007207</td>
      <td>178.0</td>
    </tr>
    <tr>
      <th>438</th>
      <td>-0.005515</td>
      <td>0.050680</td>
      <td>-0.015906</td>
      <td>-0.067642</td>
      <td>0.049341</td>
      <td>0.079165</td>
      <td>-0.028674</td>
      <td>0.034309</td>
      <td>-0.018118</td>
      <td>0.044485</td>
      <td>104.0</td>
    </tr>
    <tr>
      <th>439</th>
      <td>0.041708</td>
      <td>0.050680</td>
      <td>-0.015906</td>
      <td>0.017282</td>
      <td>-0.037344</td>
      <td>-0.013840</td>
      <td>-0.024993</td>
      <td>-0.011080</td>
      <td>-0.046879</td>
      <td>0.015491</td>
      <td>132.0</td>
    </tr>
    <tr>
      <th>440</th>
      <td>-0.045472</td>
      <td>-0.044642</td>
      <td>0.039062</td>
      <td>0.001215</td>
      <td>0.016318</td>
      <td>0.015283</td>
      <td>-0.028674</td>
      <td>0.026560</td>
      <td>0.044528</td>
      <td>-0.025930</td>
      <td>220.0</td>
    </tr>
    <tr>
      <th>441</th>
      <td>-0.045472</td>
      <td>-0.044642</td>
      <td>-0.073030</td>
      <td>-0.081414</td>
      <td>0.083740</td>
      <td>0.027809</td>
      <td>0.173816</td>
      <td>-0.039493</td>
      <td>-0.004220</td>
      <td>0.003064</td>
      <td>57.0</td>
    </tr>
  </tbody>
</table>
<p>442 rows × 11 columns</p>
</div>






<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>sex</th>
      <th>bmi</th>
      <th>bp</th>
      <th>s1</th>
      <th>s2</th>
      <th>s3</th>
      <th>s4</th>
      <th>s5</th>
      <th>s6</th>
      <th>target</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.038076</td>
      <td>0.050680</td>
      <td>0.061696</td>
      <td>0.021872</td>
      <td>-0.044223</td>
      <td>-0.034821</td>
      <td>-0.043401</td>
      <td>-0.002592</td>
      <td>0.019908</td>
      <td>-0.017646</td>
      <td>151.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-0.001882</td>
      <td>-0.044642</td>
      <td>-0.051474</td>
      <td>-0.026328</td>
      <td>-0.008449</td>
      <td>-0.019163</td>
      <td>0.074412</td>
      <td>-0.039493</td>
      <td>-0.068330</td>
      <td>-0.092204</td>
      <td>75.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.085299</td>
      <td>0.050680</td>
      <td>0.044451</td>
      <td>-0.005671</td>
      <td>-0.045599</td>
      <td>-0.034194</td>
      <td>-0.032356</td>
      <td>-0.002592</td>
      <td>0.002864</td>
      <td>-0.025930</td>
      <td>141.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-0.089063</td>
      <td>-0.044642</td>
      <td>-0.011595</td>
      <td>-0.036656</td>
      <td>0.012191</td>
      <td>0.024991</td>
      <td>-0.036038</td>
      <td>0.034309</td>
      <td>0.022692</td>
      <td>-0.009362</td>
      <td>206.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.005383</td>
      <td>-0.044642</td>
      <td>-0.036385</td>
      <td>0.021872</td>
      <td>0.003935</td>
      <td>0.015596</td>
      <td>0.008142</td>
      <td>-0.002592</td>
      <td>-0.031991</td>
      <td>-0.046641</td>
      <td>135.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>437</th>
      <td>0.041708</td>
      <td>0.050680</td>
      <td>0.019662</td>
      <td>0.059744</td>
      <td>-0.005697</td>
      <td>-0.002566</td>
      <td>-0.028674</td>
      <td>-0.002592</td>
      <td>0.031193</td>
      <td>0.007207</td>
      <td>178.0</td>
    </tr>
    <tr>
      <th>438</th>
      <td>-0.005515</td>
      <td>0.050680</td>
      <td>-0.015906</td>
      <td>-0.067642</td>
      <td>0.049341</td>
      <td>0.079165</td>
      <td>-0.028674</td>
      <td>0.034309</td>
      <td>-0.018118</td>
      <td>0.044485</td>
      <td>104.0</td>
    </tr>
    <tr>
      <th>439</th>
      <td>0.041708</td>
      <td>0.050680</td>
      <td>-0.015906</td>
      <td>0.017282</td>
      <td>-0.037344</td>
      <td>-0.013840</td>
      <td>-0.024993</td>
      <td>-0.011080</td>
      <td>-0.046879</td>
      <td>0.015491</td>
      <td>132.0</td>
    </tr>
    <tr>
      <th>440</th>
      <td>-0.045472</td>
      <td>-0.044642</td>
      <td>0.039062</td>
      <td>0.001215</td>
      <td>0.016318</td>
      <td>0.015283</td>
      <td>-0.028674</td>
      <td>0.026560</td>
      <td>0.044528</td>
      <td>-0.025930</td>
      <td>220.0</td>
    </tr>
    <tr>
      <th>441</th>
      <td>-0.045472</td>
      <td>-0.044642</td>
      <td>-0.073030</td>
      <td>-0.081414</td>
      <td>0.083740</td>
      <td>0.027809</td>
      <td>0.173816</td>
      <td>-0.039493</td>
      <td>-0.004220</td>
      <td>0.003064</td>
      <td>57.0</td>
    </tr>
  </tbody>
</table>
<p>442 rows × 11 columns</p>
</div>





```python
# CV split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.1, random_state = my_seed)
```


```python
X.sample(3)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>sex</th>
      <th>bmi</th>
      <th>bp</th>
      <th>s1</th>
      <th>s2</th>
      <th>s3</th>
      <th>s4</th>
      <th>s5</th>
      <th>s6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>160</th>
      <td>-0.009147</td>
      <td>-0.044642</td>
      <td>-0.062252</td>
      <td>-0.074528</td>
      <td>-0.023584</td>
      <td>-0.013214</td>
      <td>0.004460</td>
      <td>-0.039493</td>
      <td>-0.035817</td>
      <td>-0.046641</td>
    </tr>
    <tr>
      <th>80</th>
      <td>0.070769</td>
      <td>-0.044642</td>
      <td>0.012117</td>
      <td>0.042530</td>
      <td>0.071357</td>
      <td>0.053487</td>
      <td>0.052322</td>
      <td>-0.002592</td>
      <td>0.025393</td>
      <td>-0.005220</td>
    </tr>
    <tr>
      <th>334</th>
      <td>-0.060003</td>
      <td>0.050680</td>
      <td>-0.047163</td>
      <td>-0.022885</td>
      <td>-0.071743</td>
      <td>-0.057681</td>
      <td>-0.006584</td>
      <td>-0.039493</td>
      <td>-0.062913</td>
      <td>-0.054925</td>
    </tr>
  </tbody>
</table>
</div>






<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>sex</th>
      <th>bmi</th>
      <th>bp</th>
      <th>s1</th>
      <th>s2</th>
      <th>s3</th>
      <th>s4</th>
      <th>s5</th>
      <th>s6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>160</th>
      <td>-0.009147</td>
      <td>-0.044642</td>
      <td>-0.062252</td>
      <td>-0.074528</td>
      <td>-0.023584</td>
      <td>-0.013214</td>
      <td>0.004460</td>
      <td>-0.039493</td>
      <td>-0.035817</td>
      <td>-0.046641</td>
    </tr>
    <tr>
      <th>80</th>
      <td>0.070769</td>
      <td>-0.044642</td>
      <td>0.012117</td>
      <td>0.042530</td>
      <td>0.071357</td>
      <td>0.053487</td>
      <td>0.052322</td>
      <td>-0.002592</td>
      <td>0.025393</td>
      <td>-0.005220</td>
    </tr>
    <tr>
      <th>334</th>
      <td>-0.060003</td>
      <td>0.050680</td>
      <td>-0.047163</td>
      <td>-0.022885</td>
      <td>-0.071743</td>
      <td>-0.057681</td>
      <td>-0.006584</td>
      <td>-0.039493</td>
      <td>-0.062913</td>
      <td>-0.054925</td>
    </tr>
  </tbody>
</table>
</div>





```python
y.sample(3)
```




    169    152.0
    302    198.0
    162    172.0
    Name: target, dtype: float64







    169    152.0
    302    198.0
    162    172.0
    Name: target, dtype: float64



## EDA



```python
X['sex'].value_counts()
```




    -0.044642    235
     0.050680    207
    Name: sex, dtype: int64







    -0.044642    235
     0.050680    207
    Name: sex, dtype: int64






```python
sns.displot(
    X,
    x = "bmi",
    kind = 'kde'
)
```




    <seaborn.axisgrid.FacetGrid at 0x7f1becbf4c90>




![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)






    <seaborn.axisgrid.FacetGrid at 0x7f1becbf4c90>




![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_10_1.png)




```python
sns.displot(
    X,
    x = "bp",
    kind = 'kde'
)
```




    <seaborn.axisgrid.FacetGrid at 0x7f1c2c05d890>




![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_17_1.png)






    <seaborn.axisgrid.FacetGrid at 0x7f1c2c05d890>




![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_11_1.png)




```python
sns.displot(
    combi,
    x = "bmi",
    y = "target"
)
```




    <seaborn.axisgrid.FacetGrid at 0x7f1be14dab90>




![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_19_1.png)






    <seaborn.axisgrid.FacetGrid at 0x7f1be14dab90>




![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_12_1.png)

## Model



```python
kf = StratifiedKFold(n_splits = 5, shuffle = True, random_state = my_seed) 
```


```python

# model pipelines
pipelines = {
    'linear regression' : make_pipeline(StandardScaler(), LinearRegression()),
    'gradient boosting' : make_pipeline(StandardScaler(), GradientBoostingRegressor()),
    'random forest' : make_pipeline(StandardScaler(), RandomForestRegressor())
}
```

Search gradient boosted model hyperparameter space for optimal parameters using scikit-opt

https://scikit-optimize.github.io/stable/auto_examples/hyperparameter-optimization.html#sphx-glr-auto-examples-hyperparameter-optimization-py



```python
# NOTE: Had to downgrade to scikit-learn 0.23.2 to avoid an error regarding 'iid':
# pip install -Iv scikit-learn==0.23.2

opt = BayesSearchCV(
    pipelines['gradient boosting'],
    {

    "gradientboostingregressor__min_samples_split" : (2, 20),
#    "gradientboostingregressor__min_samples_leaf" : (1, 20),   
    "gradientboostingregressor__n_estimators" : (100, 300),
    "gradientboostingregressor__max_depth" : (1, 5),
    "gradientboostingregressor__max_features": (2, n_features),
    "gradientboostingregressor__learning_rate" : (10**-5, 0.8, 'log-uniform')
    },
    cv = kf, # use k-fold cross validation
    random_state = my_seed,
    n_iter = 30,
    n_jobs = 8
)

opt.fit(X_train, y_train)

print("val. score: %s" % opt.best_score_)
print("test score: %s" % opt.score(X_test, y_test))
print("best params: %s" % str(opt.best_params_))
```

    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)


    val. score: 0.41534121914268674
    test score: 0.5780905566781522
    best params: OrderedDict([('gradientboostingregressor__learning_rate', 0.03200464817593894), ('gradientboostingregressor__max_depth', 1), ('gradientboostingregressor__max_features', 10), ('gradientboostingregressor__min_samples_split', 2), ('gradientboostingregressor__n_estimators', 300)])


    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)
    /home/cambonator/anaconda3/lib/python3.7/site-packages/sklearn/model_selection/_split.py:672: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      % (min_groups, self.n_splits)), UserWarning)


    val. score: 0.41534121914268674
    test score: 0.5780905566781522
    best params: OrderedDict([('gradientboostingregressor__learning_rate', 0.03200464817593894), ('gradientboostingregressor__max_depth', 1), ('gradientboostingregressor__max_features', 10), ('gradientboostingregressor__min_samples_split', 2), ('gradientboostingregressor__n_estimators', 300)])





```python
_ = plot_objective(
    opt.optimizer_results_[0]
)
plt.show()
```


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_27_0.png)


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_18_0.png)




```python
10**0
```




    1







    1






```python
_ = plot_histogram(opt.optimizer_results_[0], 0)
plt.show()
```


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_31_0.png)


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_20_0.png)




```python
#from skopt.plots import plot_convergence
#plot_convergence(opt)
```


```python
_ = prediction_error(opt, X_test, y_test)
```


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_34_0.png)


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_22_0.png)




```python
_ = prediction_error(opt, X_train, y_train)
```


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_36_0.png)


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_23_0.png)




```python
_ = residuals_plot(
    opt, X_test, y_test
)
```


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_38_0.png)


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_24_0.png)




```python
_ = residuals_plot(
    opt, X_train, y_train
)
```


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_40_0.png)


![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_25_0.png)




```python

```
