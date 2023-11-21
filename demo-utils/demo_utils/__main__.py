from demo_utils.pipeline import build_pipeline, preprocess_match_dataset
import pandas as pd
from tempfile import mkdtemp
from shutil import rmtree

def test_pipeline():
    cache_dir = mkdtemp()
    df = pd.read_pickle("./test.pkl")
    X, y = preprocess_match_dataset(df, run_date="2014-12-15")
    clf = build_pipeline(memory=cache_dir)
    clf.fit(X, y)
    return clf


if __name__ == '__main__':
    test_pipeline()
