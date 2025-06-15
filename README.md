
<a name="readme-top"></a>


<br />
<div align="center">
  <a href="https://github.com/devdnhee">
    <img src="images/logo.png" alt="Logo" width="600" height="120">
  </a>

<h1 align="center">🎲 Your Best Bet</h1>

  <p align="center">
    MLOps demo with Python models in dbt on the <a href="https://www.kaggle.com/datasets/hugomathien/soccer">European Soccer Database</a>

  </p>
</div>




<!-- ABOUT THE PROJECT -->
## About The Project
Welcome to the high-octane world of production ML pipelines! We're thrilled to present an epic demonstration showcasing numerous MLOps concepts packed into a single dbt project. Strap in as we unveil this treasure trove of tools, tailored to empower data teams within organizations, speeding up the journey of ML models to production!

Imagine a scenario of daily (or weekly) sports betting where you're on a quest to outsmart the bookies. This project houses the code for a data warehouse powered by the [European Soccer Database](https://www.kaggle.com/datasets/hugomathien/soccer). Utilizing team and player statistics, performance metrics, FIFA stats, and bookie odds, we'll hunt down opportunities where our model paints a more accurate picture than at least one bookie. When our odds stack up better against theirs, it's our chance to strike gold! 💰

Within our pipeline, you can:

- **Version Your Dataset**: run preprocessing to (re)generate your ML dataset
- **Experiment & Store**: run and save experiments
- **Model Management**: save and compare models
- **Reproducibility**: ensure inference pipelines run without train/serving skew (run simulations)
- **Feature Store**: house all input features with the available KPIs at that time
- **Prediction Audit**: maintain a log of all predictions

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

### Prerequisites
This thrilling adventure requires:

* Python
* Access to a Databricks cluster (e.g., [Azure free account](https://azure.microsoft.com/en-us/free))
* A firm grasp on [dbt](https://docs.getdbt.com/docs/introduction) for seamless execution of these examples



### Installation (Databricks)

1. install virtual environment
   ```bash
   virtualenv .venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Download data from [here]("https://www.kaggle.com/datasets/hugomathien/soccer/download?datasetVersionNumber=10") -> you need a Kaggle account. Drop the resulting `database.sqlite` file in the data folder.
3. Convert data to parquet and csv files
   ```bash
   python scripts/convert_data.py
   ```
4. Databricks
   1. Create a SQL warehouse -> check the connection details for your profile in the next step
   2. Create a personal access token
   3. Upload data (parquet files) to warehouse
   ![](images/catalog.png)
   4. Create a compute cluster
   5. check the cluster id (you can find in the SparkUI), and set as env var: `COMPUTE_CLUSTER_ID=...` \
   ![](images/sparkui.png)
5. dbt
   1. initialise and install dependencies.
   ```sh
   cd dbt_your_latest_bet
   dbt deps
   ```
   2. setup your [dbt profile](https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles), should look something like this:
   ```yaml
   databricks:
    outputs:
        dev:
            catalog: hive_metastore
            host: xxx.cloud.databricks.com
            http_path: /sql/1.0/warehouses/$SQL_WAREHOUSE_ID
            schema: football
            threads: 4 # max number of parallel processes
            token: $PERSONAL_ACCESS_TOKEN
            type: databricks
    target: dev
   ```
6. `riskrover` python package, managed with poetry
   1. build and install the package in your local environment
   ```sh
   cd riskrover
   poetry build
   pip install dist/riskrover-x.y.z.tar.gz
   ```
   2. Install the resulting `riskrover` whl file on your databricks compute cluster


You should now be able to run the entire pipeline without any trained models (i.e. the preprocessing):

```sh
dbt build --selector gold
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Explore and command the powers of our pipeline.

For these examples to work -> you need to move to the root dir of the dbt project, i.e. `dbt_your_best_bet`.

### MWE for a simulation

The default variables are stored in `dbt_project.yaml`. We find ourselves on 2016-01-01 in our simulation, with the option to run until 2016-05-25.

```sh
cd dbt_your_best_bet

# Preprocessing
dbt build --selector gold

# Experimentation (by default -> training set to 2015-07-31, and trains a simple logistic regression with cross validation)
dbt build --selector ml_experiment

# Inference on test set (2015-08-01 -> 2015-12-31)
dbt build --selector ml_predict_run

# moving forward in time, for example with a weekly run
dbt build --vars '{"run_date": "2016-01-08"}'
dbt build --vars '{"run_date": "2016-01-15"}'
dbt build --vars '{"run_date": "2016-01-22"}'
...
```

### Checking the data catalog

```sh
cd dbt_your_best_bet

dbt docs generate
dbt docs serve
```

It's like a grand lineage tale with no models documented yet—stay tuned!
We can already check the lineage:
![](images/lineage.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

Mostly maintenance, no plans on new features unless requested.

- [ ] Documentation
- [ ] Tests
- [ ] Extra sql analysis models

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

All contributions are welcome!

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License.



<!-- CONTACT -->
## Contact
- devdnhee@gmail.com / dorian@dataroots.io



<p align="right">(<a href="#readme-top">back to top</a>)</p>




## TO ADD TO README

- how to clean simulation
- updated setup guide -> env vars!!!!
- how to install package on databricks cluster
- more examples on how to follow along the simulation
- evaluation notebook
- ...

## Cleanup

```sql
drop table if exists snapshots.predict_input_history;
drop table if exists snapshots.experiment_history;
```

then build with `--full-refresh`


## Simulation

The default variables are stored in `dbt_project.yaml`. We find ourselves on 2016-01-01 in our simulation, with the option to run until 2016-05-25.

```sh
# Preprocessing
dbt build --selector gold --full-refresh

# Experimentation (by default -> training set to 2015-07-31, and trains a simple logistic regression with cross validation) => best model is stored
dbt build --selector ml_experiment --vars '{"ml_experiment_model": "logistic_regression", "ml_experiment_cv_n_iter": 10, "ml_experiment_n_splits": 2}'

# cross validation with xgboost
dbt build --selector ml_experiment --vars '{"ml_experiment_model": "xgboost", "ml_experiment_cv_n_iter": 10, "ml_experiment_n_splits": 2}'

# random forest
dbt build --selector ml_experiment --vars '{"ml_experiment_model": "random_forest", "ml_experiment_cv_n_iter": 10, "ml_experiment_n_splits": 2}'

# Inference on test set (2015-08-01 -> 2015-12-31)
# You Let's perform on all models
RUN_DATE='2016-01-01' dbt build --selector ml_predict_run --vars '{"ml_predict_model": "logistic_regression"}'
RUN_DATE='2016-01-01' dbt build --selector ml_predict_run --vars '{"ml_predict_model": "random_forest"}'
RUN_DATE='2016-01-01' dbt build --selector ml_predict_run --vars '{"ml_predict_model": "xgboost"}'

# Good time to take stock of the different models:
dbt compile -s analyses/compare_model_profit.sql

# moving forward in time, for example with a weekly run
dbt build --vars '{"run_date": "2016-01-08"}'
dbt build --vars '{"run_date": "2016-01-15"}'
dbt build --vars '{"run_date": "2016-01-22"}'
```
