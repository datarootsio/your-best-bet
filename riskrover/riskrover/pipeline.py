from riskrover import transformers
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn import set_config

from sklearn import (
    pipeline,
    compose,
    feature_selection,
    impute,
    linear_model,
    preprocessing,
    calibration,
)

from pathlib import Path
import json
import importlib.resources

# Ensures that all sklearn transformers output Pandas DataFrames with proper column names, 
# making debugging and understanding intermediate steps much easier.
set_config(transform_output="pandas")

# Categorical type definitions for features
# ordered categorical types enforce specific categories and their inherent order (e.g., "Slow" < "Balanced" < "Fast")
# which is vital for proper ordinal encoding.
amount_type = pd.CategoricalDtype(categories=["Little", "Normal", "Lots"], ordered=True)
speed_type = pd.CategoricalDtype(categories=["Slow", "Balanced", "Fast"], ordered=True)
length_type = pd.CategoricalDtype(categories=["Short", "Mixed", "Long"], ordered=True)
organisation_type = pd.CategoricalDtype(
    categories=["Organised", "Free Form"], ordered=True
)
risk_type = pd.CategoricalDtype(categories=["Safe", "Normal", "Risky"], ordered=True)
line_type = pd.CategoricalDtype(categories=["Deep", "Medium", "High"], ordered=True)
aggression_type = pd.CategoricalDtype(categories=["Contain", "Double", "Press"])
width_type = pd.CategoricalDtype(categories=["Narrow", "Normal", "Wide"], ordered=True)
offside_type = pd.CategoricalDtype(categories=["Cover", "Offside Trap"])
result_type = pd.CategoricalDtype(categories=["away", "draw", "home"])

with importlib.resources.files("riskrover").joinpath("features.json").open() as f:
    FEATURES = json.load(f)

TARGET = "winner"

CATEGORICAL_TYPES = {
    "home_buildupplaydribblingclass": amount_type,
    "away_buildupplaydribblingclass": amount_type,
    "home_buildupplayspeedclass": speed_type,
    "away_buildupplayspeedclass": speed_type,
    "home_buildupplaypassingclass": length_type,
    "away_buildupplaypassingclass": length_type,
    "home_buildupplaypositioningclass": organisation_type,
    "away_buildupplaypositioningclass": organisation_type,
    "home_chancecreationpassingclass": risk_type,
    "away_chancecreationpassingclass": risk_type,
    "home_chancecreationcrossingclass": amount_type,
    "away_chancecreationcrossingclass": amount_type,
    "home_chancecreationshootingclass": amount_type,
    "away_chancecreationshootingclass": amount_type,
    "home_chancecreationpositioningclass": organisation_type,
    "away_chancecreationpositioningclass": organisation_type,
    "home_defencepressureclass": line_type,
    "away_defencepressureclass": line_type,
    "home_defenceaggressionclass": aggression_type,
    "away_defenceaggressionclass": aggression_type,
    "home_defenceteamwidthclass": width_type,
    "away_defenceteamwidthclass": width_type,
    "home_defencedefenderlineclass": offside_type,
    "away_defencedefenderlineclass": offside_type,
    # "winner": result_type,
}

TARGET_MAP = {"home": 0, "draw": 1, "away": 2}


def get_dataset_features(df, subset="all", return_dict=False):
    """
    Get features from the dataset based on the specified subset.

    Args:
    - df (pd.DataFrame): Input DataFrame.
    - subset (str): Subset selection, default is 'all'.
    - return_dict (bool): Return as dictionary or list, default is False.

    Returns:
    - Union[List[str], Dict[str, List[str]]]: Features based on the subset.
    """
    season_info = ["league_name"]
    odds_features = df.filter(like="odds").columns.tolist()
    numeric_stats = df.filter(regex="_(?:avg|median|count|min|max)_").columns.tolist()
    categorical_stats = df.filter(like="class").columns.tolist()
    other_stats = [
        c
        for c in df.filter(
            regex="buildup|chancecreation|defence|form|points_per_match|season_progress"
        ).columns.tolist()
        if c not in numeric_stats + categorical_stats
    ]

    d = dict(
        season_info=season_info,
        odds=odds_features,
        numeric_stats=numeric_stats,
        categorical_stats=categorical_stats,
        other_stats=other_stats,
        all=season_info
        + odds_features
        + numeric_stats
        + categorical_stats
        + other_stats,
    )

    if return_dict:
        return d

    return d[subset]


def preprocess_match_dataset(
    df,
    id_column="id",
    min_date="2009-01-01",
    max_date="2017-01-01",
):
    """
    Preprocess the match dataset.

    Args:
    - df (pd.DataFrame): Input DataFrame.
    - id_column (str): Identifier column name, default is 'id'.
    - min_date (str): Minimum date, default is '2009-01-01'.
    - max_date (str): Maximum date, default is '2017-01-01'.

    Returns:
    - Tuple[pd.DataFrame, pd.Series]: Processed X and y (if present).
    """
    df_pp = (
        df.copy()
        .set_index(id_column)
        .assign(match_date=lambda df: pd.to_datetime(df.match_date))
        .query("(match_date >= @min_date) & (match_date <= @max_date)")
        .assign(
            season=lambda df: df.season.apply(lambda x: int(x[:4]) - 2009),
        )
        .astype(CATEGORICAL_TYPES)
        .sort_values("match_date")
        # .reset_index(drop=True)
    )

    X = df_pp.loc[:, get_dataset_features(df_pp)]
    if TARGET in df_pp.columns:
        y = df_pp[TARGET].map(TARGET_MAP)
        return X, y

    return X, None


def build_pipeline(model=None, *args, **kwargs):
    """
    Build a scikit-learn pipeline.

    Args:
    - model (Any): Model for the pipeline, default is None.
    - *args, **kwargs: Additional arguments.

    Returns:
    - pipeline.Pipeline: Data processing pipeline.
    """
    if model is None:
        model = linear_model.LogisticRegression()

    categorical_pipeline = pipeline.Pipeline(
        steps=[
            (
                "imputer",
                transformers.GroupedImputer(
                    groupby=FEATURES["season_info"], agg_func="mode"
                ),
            ),
            (
                "frequent_imputer",
                impute.SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encode_split",
                compose.ColumnTransformer(
                    transformers=[
                        (
                            "ordinal_encoder",
                            preprocessing.OrdinalEncoder(
                                categories=[
                                    CATEGORICAL_TYPES[c].categories.tolist()
                                    for c in FEATURES["categorical_stats"]
                                ]
                            ),
                            FEATURES["categorical_stats"],
                        ),
                        (
                            "league_encoder",
                            preprocessing.OrdinalEncoder(),
                            ["league_name"],
                        ),
                        # ("season", "passthrough", ["season"]),
                    ],
                    verbose_feature_names_out=False,
                ),
            ),
            ("minmax_scaler", preprocessing.MinMaxScaler(feature_range=(-1, 1))),
        ]
    )

    numerical_stats_pipeline = pipeline.Pipeline(
        steps=[
            ("constant_imputer", impute.SimpleImputer(strategy="median")),
            ("numeric", preprocessing.StandardScaler()),
        ]
    )

    odds_stats_pipeline = pipeline.Pipeline(
        steps=[
            ("numeric", preprocessing.StandardScaler()),
            (
                "imputer",
                impute.IterativeImputer(
                    initial_strategy="mean",
                    n_nearest_features=5,
                    skip_complete=True,
                ),
            ),
        ]
    )

    steps = [
        (
            "type_split",
            compose.ColumnTransformer(
                transformers=[
                    (
                        "categories",
                        categorical_pipeline,
                        FEATURES["season_info"] + FEATURES["categorical_stats"],
                    ),
                    (
                        "stats",
                        numerical_stats_pipeline,
                        FEATURES["numeric_stats"] + FEATURES["other_stats"],
                    ),
                    ("odds", odds_stats_pipeline, FEATURES["odds"]),
                ],
                verbose_feature_names_out=False,
            ),
        ),
        ("selector", feature_selection.SelectKBest(feature_selection.f_classif)),
        ("model", calibration.CalibratedClassifierCV(estimator=model, ensemble=False)),
    ]

    pipe = pipeline.Pipeline(steps=steps, *args, **kwargs)

    return pipe
