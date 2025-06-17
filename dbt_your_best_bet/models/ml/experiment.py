from tempfile import mkdtemp
from shutil import rmtree
from datetime import datetime
import hashlib

import scipy.stats
from sklearn import model_selection
from sklearn import ensemble, linear_model
import xgboost
import pandas as pd
import joblib
import os

import json

from riskrover import pipeline

import pyspark.sql.types as T

# Grid search parameters for different models
_MODEL_GRIDS = {
    "random_forest": {
        "n_estimators": scipy.stats.randint(50, 1000),
        "max_depth": scipy.stats.randint(5, 25),
        "criterion": ["gini", "entropy", "log_loss"],
        "min_samples_split": scipy.stats.randint(2, 10),
    },
    "logistic_regression": {
        "C": scipy.stats.loguniform(0.1, 1000),
    },
    "xgboost": {
        "booster": ["gbtree", "gblinear", "dart"],
        "gamma": scipy.stats.uniform(1, 9),
        "max_depth": scipy.stats.randint(3, 18),
        "reg_alpha": scipy.stats.randint(40, 160),
        "reg_lambda": scipy.stats.uniform(0, 1),
        "colsample_bytree": scipy.stats.uniform(0.5, 1),
        "min_child_weight": scipy.stats.randint(0, 10),
        "n_estimators": scipy.stats.randint(20, 500),
    },
}

# Parameters for the pipeline
_PIPELINE_PARAMS = {
    "selector__k": scipy.stats.randint(20, 100),
}

# Scoring metrics for cross-validation
_CV_SCORING = [
    "neg_log_loss",
    "accuracy",
    "f1_macro",
    "precision_macro",
    "recall_macro",
    "roc_auc_ovr",
]

# Path for storing trained models
_DBFS_MODELS_PATH = "/dbfs/FileStore/models"

# Output schema structure using PySpark SQL types
_OUTPUT_SCHEMA = T.StructType(
    [
        T.StructField("mean_fit_time", T.DoubleType(), True),
        T.StructField("mean_score_time", T.DoubleType(), True),
        T.StructField("params", T.StringType(), True),
        T.StructField("mean_test_neg_log_loss", T.DoubleType(), True),
        T.StructField("rank_test_neg_log_loss", T.IntegerType(), True),
        T.StructField("mean_train_neg_log_loss", T.DoubleType(), True),
        T.StructField("mean_test_accuracy", T.DoubleType(), True),
        T.StructField("rank_test_accuracy", T.IntegerType(), True),
        T.StructField("mean_train_accuracy", T.DoubleType(), True),
        T.StructField("mean_test_f1_macro", T.DoubleType(), True),
        T.StructField("rank_test_f1_macro", T.IntegerType(), True),
        T.StructField("mean_train_f1_macro", T.DoubleType(), True),
        T.StructField("mean_test_precision_macro", T.DoubleType(), True),
        T.StructField("rank_test_precision_macro", T.IntegerType(), True),
        T.StructField("mean_train_precision_macro", T.DoubleType(), True),
        T.StructField("mean_test_recall_macro", T.DoubleType(), True),
        T.StructField("rank_test_recall_macro", T.IntegerType(), True),
        T.StructField("mean_train_recall_macro", T.DoubleType(), True),
        T.StructField("mean_test_roc_auc_ovr", T.DoubleType(), True),
        T.StructField("rank_test_roc_auc_ovr", T.IntegerType(), True),
        T.StructField("mean_train_roc_auc_ovr", T.DoubleType(), True),
        T.StructField("best_estimator_path", T.StringType(), True),
        T.StructField("experiment_name", T.StringType(), True),
        T.StructField("run_date", T.StringType(), True),
        T.StructField("train_start_date", T.StringType(), True),
        T.StructField("train_end_date", T.StringType(), True),
        T.StructField("execution_timestamp", T.TimestampType(), True),
        T.StructField("algorithm", T.StringType(), True),
        T.StructField("class", T.StringType(), True),
        T.StructField("dbt_vars", T.StringType(), True),
        T.StructField("experiment_id", T.StringType(), True),
    ]
)


def build_param_grid(model_name):
    """
    Build parameter grid for grid search based on the selected model.

    Args:
    - model_name (str): Name of the machine learning model.

    Returns:
    - dict: Parameter grid for grid search.
    """
    model_params = {
        f"model__estimator__{k}": v for k, v in _MODEL_GRIDS[model_name].items()
    }
    return {**model_params, **_PIPELINE_PARAMS}


def get_model(model_name):
    """
    Get the instance of the selected machine learning model.

    Args:
    - model_name (str): Name of the machine learning model.

    Returns:
    - object: Instance of the specified machine learning model.
    """
    match model_name:
        case "random_forest":
            return ensemble.RandomForestClassifier()
        case "logistic_regression":
            return linear_model.LogisticRegression()
        case "xgboost":
            return xgboost.XGBClassifier(objective="multi:softprob")


def generate_experiment_id(r):
    """
    Generate an experiment ID using experiment details.

    Args:
    - r (dict / pd.Series): Dictionary containing experiment details.

    Returns:
    - str: Experiment ID generated using hash digest.
    """
    s_enc = f"{r['experiment_name']}_{r['rank_test_neg_log_loss']}".encode()
    return hashlib.md5(s_enc).hexdigest()


def model(dbt, session):
    """
    Train machine learning models using the provided data and configurations.

    Args:
    - dbt (object at run time): Object containing configuration and data references.
    - session: SparkSession object for executing operations.

    Returns:
    - pd.DataFrame: DataFrame containing experiment results and metadata.
    """
    if not dbt.config.get("experiment_enabled"):
        return session.createDataFrame([], _OUTPUT_SCHEMA)

    # fetch variables
    train_end_date = dbt.config.get("train_end_date")
    model = dbt.config.get("model")

    # fetch data
    sparkDF = dbt.ref("match_dataset")
    df = sparkDF.toPandas()

    cache_dir = mkdtemp()

    X_train, y_train = pipeline.preprocess_match_dataset(df, max_date=train_end_date)
    algorithm = get_model(model)
    clf = pipeline.build_pipeline(model=algorithm, memory=cache_dir)
    cv = model_selection.RandomizedSearchCV(
        estimator=clf,
        param_distributions=build_param_grid(model),
        n_iter=int(dbt.config.get("n_iter")),
        scoring=_CV_SCORING,
        n_jobs=-1,
        refit="neg_log_loss",
        # gap asserts the test split is starting on a different date
        cv=model_selection.TimeSeriesSplit(
            n_splits=int(dbt.config.get("n_splits")), gap=50
        ).split(X_train),
        return_train_score=True,
        verbose=3,
    )
    cv.fit(X_train, y_train)

    meta = {
        "best_estimator_path": os.path.join(
            _DBFS_MODELS_PATH, f"model_{datetime.now().strftime('%Y%m%d%H%M%S')}.joblib"
        ),
        "experiment_name": f"experiment_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "run_date": dbt.config.get("run_date"),
        "train_start_date": dbt.config.get("train_start_date"),
        "train_end_date": train_end_date,
        "execution_timestamp": datetime.now(),
        "algorithm": model,
        "class": str(algorithm.__class__)[8:-2],
        "dbt_vars": json.dumps(
            {
                "start_date": dbt.config.get("train_start_date"),
                "train_end_date": dbt.config.get("train_end_date"),
                "run_date": dbt.config.get("run_date"),
                "ml_experiment_model": dbt.config.get("model"),
                "ml_experiment_cv_n_iter": dbt.config.get("n_iter"),
                "ml_experiment_n_splits": dbt.config.get("n_splits"),
            }
        ),
    }

    os.makedirs(_DBFS_MODELS_PATH, exist_ok=True)
    joblib.dump(cv.best_estimator_, meta["best_estimator_path"])

    df_experiment = (
        pd.DataFrame(cv.cv_results_)
        # parameters are different depending on the model -> exclude from the schema
        # std + split scores are TMI
        .filter(regex="^(?!param_|split\d+|std)")
        .assign(**meta)
        .assign(
            experiment_id=lambda df: df.apply(generate_experiment_id, axis=1),
            # important to convert to string, or we'll struggle with schema issues
            params=lambda df: df.params.apply(json.dumps),
        )
    )

    # clean up
    rmtree(cache_dir)

    return df_experiment
