# 🎲 DBT: Your best bet

DBT project for a data pipeline for the [European Soccer Database](https://www.kaggle.com/datasets/hugomathien/soccer)

## 🛠 Installation

See top level [../README.md](README.md).

## 🏁 Quickstart

See top level [../README.md](README.md).

## 📁 File structure

```txt
.
├── README.md
├── analyses
│   ├── compare_model_profit.sql
│   ├── model_profit_per_day.sql
├── dbt_project.yml
├── macros
│   └── macros.sql
├── models
│   ├── aggregated
│   │   ├── season.sql
│   │   └── team_kpi.sql
│   ├── datasets
│   │   └── match_dataset.sql
│   ├── ml
│   │   ├── evaluation.sql
│   │   ├── experiment.py
│   │   ├── models.yml
│   │   ├── predict_input.sql
│   │   └── predict_output.py
│   └── silver
│       ├── match.sql
│       ├── player.sql
│       ├── player_attributes.sql
│       ├── player_match.sql
│       ├── team.sql
│       ├── team_attributes.sql
│       └── team_match.sql
├── packages.yml
├── seeds
│   ├── country.csv
│   └── league.csv
├── selectors.yml
├── snapshots
│   ├── experiment_history.sql
│   └── predict_input_history.sql
├── sources
│   └── european_soccer_db.yml
└── tests
```

More info on the dbt project structure you find [here](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview).

The models are ordered as follows:
- silver -> silver data, as in 'loaded' / 'cleansed'. Basically copies from the original dataset but ensured to only enter when valid according to the `run_date` variable.
- aggregated -> KPIs calculated in SCD2 type fashion
- datasets -> entry points for ML
- ml -> ML code
