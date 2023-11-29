# 🕵️‍♂️ Risk Rover

Python package with all the main modeling code.

The model is a [sklearn pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) with the following components:


This is the architecture of the pipeline:
![](model-pipeline.png)

## 🛠 Installation

```sh
# get poetry inside your env
pip install poetry
poetry build
# check which version we're at
pip install dist/riskrover-x.y.z.tar.gz
```

## 🏁 Quickstart

Locally you would need to have a copy of the [match_dataset](https://github.com/datarootsio/your-best-bet/blob/main/dbt_your_best_bet/models/datasets/match_dataset.sql) in the dbt project, or have access to it from your data platform.

suppose `df` is a copy of your dataset as a pandas dataframe:

### 💺 Training new model

```python
from riskrover import pipeline
from sklearn import linear_model

X_train, y_train = pipeline.preprocess_match_dataset(df, max_date=train_end_date)

# you can pick any model really
clf = pipeline.build_pipeline(model=linear_model.LinearRegression())

clf.fit(X_train, y_train)
```


## 🤝 Contributing

```sh
# installs environment + dependencies
poetry install
```
