from typing import Any
from demo_utils.pipeline import build_pipeline
import joblib
import pandas as pd

_MAP_TO_CLASS = {"a": "away", "d": "draw", "h": "home"}


class RiskRover:
    def __init__(self, pipeline=None, *args, **kwargs):
        if pipeline is not None:
            self.pipeline = pipeline
        else:
            self.pipeline = build_pipeline(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.pipeline, attr)

    def _get_decision_from_row(self, row):
        row.name = "odd"
        best_odds = (
            row[row.filter(regex="^odds").groupby(lambda x: x[-1]).idxmax().values]
            .to_frame()
            .assign(bet=lambda df: df.index.map(lambda x: _MAP_TO_CLASS[x[-1]]))
            .reset_index()
            .rename(columns={"index": "bookie"})
            .set_index("bet")
        )

        model_odds = (
            row.filter(regex="^x")
            .to_frame()
            .assign(bet=lambda df: df.index.map(lambda x: _MAP_TO_CLASS[x[-1]]))
            .set_index("bet")
        )

        decision_info = (
            model_odds.join(best_odds, lsuffix="_model", rsuffix="_bookie")
            .rename(columns={"odd_model": "xOdd"})
            .assign(xProfit=lambda df: df["odd_bookie"] - df["xOdd"])
            .assign(xYieldsProfit=lambda df: df.xProfit > 0)
            .reset_index()
        )

        js = decision_info.to_json()

        decision = decision_info.assign(decision_info=js).loc[
            decision_info.xProfit.idxmax()
        ]
        return decision

    def __call__(self, X, *args: Any, **kwds: Any) -> Any:
        y_proba = self.predict_proba(X)
        y_odds = 1 + (1 - y_proba) / y_proba

        df_odds = X.filter(regex="odds").join(
            pd.DataFrame(y_odds, columns=["xh", "xa", "xd"], index=X.index),
            how="inner",
        )

        # filter out where no odds available => can't beat what doesn't exist, add later
        df_bets = (
            df_odds.dropna(how="all", subset=df_odds.filter(like="odds").columns)
            .apply(self._get_decision_from_row, axis=1)
            .join(df_odds.filter(regex="^x"), how="right")
            .rename(columns={"xh": "xHome", "xd": "xDraw", "xa": "xAway"})
        )

        return df_bets

    @classmethod
    def from_disk(cls, path):
        pipeline = joblib.load(path)
        return RiskRover(pipeline)
