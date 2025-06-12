from pathlib import Path
import sqlite3

PROJECT_DIR = Path(__file__).parents[1]
DATA_DIR = PROJECT_DIR / "data"
SQLITE_PATH = DATA_DIR / "database.sqlite"
SEED_DIR = PROJECT_DIR / "dbt_your_best_bet" / "seeds"


def main():
    """Reads tables from sqlite file, converts to dataframes and writes them out as seed files or parquet files"""
    connection = sqlite3.connect(SQLITE_PATH)
    cursor = connection.cursor()
    tables = list(
        filter(
            lambda c: c != "sqlite_sequence",
            map(
                lambda t: t[0],
                cursor.execute(
                    "SELECT tbl_name FROM sqlite_master WHERE type='table';"
                ).fetchall(),
            ),
        )
    )

    dfs = {table: pd.read_sql(f"select * from {table}", connection) for table in tables}

    # seed files
    dfs["Country"].to_csv(SEED_DIR / "country.csv", index=False)
    dfs["League"].to_csv(SEED_DIR / "league.csv", index=False)

    # parquet files
    dfs["Player_Attributes"].to_parquet(DATA_DIR / "player_attributes.parquet")
    dfs["Match"].to_parquet(DATA_DIR / "match.parquet")
    dfs["Player"].to_parquet(DATA_DIR / "player.parquet")
    dfs["Team"].to_parquet(DATA_DIR / "team.parquet")
    dfs["Team_Attributes"].to_parquet(DATA_DIR / "team_attributes.parquet")

    return


if __name__ == "__main__":
    main()
