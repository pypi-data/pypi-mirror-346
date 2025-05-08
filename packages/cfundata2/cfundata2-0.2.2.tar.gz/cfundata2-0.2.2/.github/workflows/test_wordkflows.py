import pandas as pd

from cfundata2 import FREQUENCY2_PATH, FREQUENCY_PATH


def test_frequency():
    # Read the parquet file
    print(FREQUENCY2_PATH)
    print(type(FREQUENCY2_PATH))
    df = pd.read_parquet(FREQUENCY_PATH)
    print(df.head())
    print(df.columns)
    print(df.dtypes)
    print(df.info())

    df2 = pd.read_parquet(FREQUENCY2_PATH)
    print(df2.head())
    print(df2.columns)
    print(df2.dtypes)
    print(df2.info())


if __name__ == "__main__":
    test_frequency()
