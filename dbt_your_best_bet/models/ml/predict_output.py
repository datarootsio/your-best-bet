from datetime import datetime

from riskrover.model import RiskRover
from riskrover.pipeline import preprocess_match_dataset
import logging

import pyspark.sql.functions as F
import pyspark.sql.types as T

_OUTPUT_SCHEMA = T.StructType(
    [
        T.StructField("prediction_id", T.StringType(), True),
        T.StructField("bet", T.StringType(), True),
        T.StructField("xOdd", T.DoubleType(), True),
        T.StructField("bookie", T.StringType(), True),
        T.StructField("odd_bookie", T.DoubleType(), True),
        T.StructField("xProfit", T.DoubleType(), True),
        T.StructField("xYieldsProfit", T.BooleanType(), True),
        T.StructField("decision_info", T.StringType(), True),
        T.StructField("xHome", T.DoubleType(), True),
        T.StructField("xAway", T.DoubleType(), True),
        T.StructField("xDraw", T.DoubleType(), True),
        T.StructField("model_path", T.StringType(), True),
        T.StructField("prediction_timestamp", T.TimestampType(), True),
    ]
)


def model(dbt, session):
    # /!\ The incremental materialisation is only read when in the python model itself
    dbt.config(materialized="incremental", incremental_strategy="append")

    if (model_path := dbt.config.get("ml_model_path")) == "best":
        model_path = (
            dbt.ref("experiment_history")
            .filter(F.isnotnull(F.col("mean_test_neg_log_loss")))
            .orderBy("mean_test_neg_log_loss", ascending=False)
            .select(F.col("best_estimator_path"))
            .toPandas()
            .iloc[0, 0]
        )

    logging.info(f"Loading {model_path}...")
    model = RiskRover.from_disk(model_path)

    df = dbt.ref("predict_input")
    if dbt.is_incremental:
        # only make predictions we haven't seen yet
        predictions = (
            session.read.table(
                f"{dbt.this.database}.{dbt.this.schema}.{dbt.this.identifier}"
            )
            .filter(F.col("model_path") == model_path)
            .select(F.col("prediction_id").alias("prediction_id_out"))
        )
        df = (
            df.join(
                predictions,
                on=df.prediction_id == predictions.prediction_id_out,
                how="left",
            )
            .filter(F.isnull(F.col("prediction_id_out")))
            .drop(F.col("prediction_id_out"))
        )
    if df.count() == 0:
        return session.createDataFrame([], schema=_OUTPUT_SCHEMA)

    df = df.toPandas()

    meta = {"model_path": model_path, "prediction_timestamp": datetime.now()}

    X, _ = preprocess_match_dataset(df, id_column="prediction_id")
    predictions = model(X).reset_index().assign(**meta)

    return predictions
