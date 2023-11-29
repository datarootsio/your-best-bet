<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- TODO PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- TODO: fix PROJECT LOGO -->
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

In this project, we examine an examplary production ML pipeline. The goal of the project is to showcase how many MLOps concepts can be build within just one dbt project. This can be beneficial for data teams inside organisations to lift ml models faster to production.

The use case is a daily (or weekly) sports betting where you try to beat the bookies. This projects holds the code for a datawarehouse with source data coming from the [European Soccer Database](https://www.kaggle.com/datasets/hugomathien/soccer). Using team and player statistics, performance, fifa stats and bookie odds, we'll find opportunities where at least 1 bookie has a worse probabilistic view on reality than our model. When our probabilistic odds are smaller than the bookies, we have an opportunity to win money 💰.

Within the pipeline, you can:
- **Dataset versioning**: run preprocessing -> (re)generate your ML dataset
- **Experimentation**: run and store experiments
- **Model management**: save and compare models
- **Reproducibility**: run inference pipelines without train / serving skew (run simulations)
- **Feature Store**: store all input features with the KPIs available at the time
- **Prediction Audit**: store all predictions

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

### Prerequisites

* Python
* Access to a Databricks cluster (for example with [Azure free account](https://azure.microsoft.com/en-us/free))
* It's also helpful to have a good background on [dbt](https://docs.getdbt.com/docs/introduction) to perform the examples


### Installation (Azure)

1. install virtual environment
   ```bash
   virtualenv venv
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
   2. Create a [personal access token](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth#--azure-databricks-personal-access-tokens-for-workspace-users), keep this token close and use to connect dbt to your sql warehouse.
   3. Upload data (parquet files) to warehouse, into the `default` schema in the `hive_metastore` catalog. Your catalog should look something like this \
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

For these examples to work -> you need to move to the root dir of the dbt project, i.e. `dbt_your_best_bet`

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

At this point in time, no models are documented, however it's useful to see the lineage.
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



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
