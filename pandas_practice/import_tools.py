import pandas as pd


def ensure_list(ambiguous_item):
    """If input is not a list, return list of input"""
    return ambiguous_item if isinstance(ambiguous_item, list) else [ambiguous_item]


def import_csv(
    csv_fp: str = "data/survey_results_public.csv",
    dtypes: dict = None,
    index_col: str = None,
    header: int = 0,
    na_values: list = None,
):
    df = pd.read_csv(
        csv_fp,
        header=header,
        index_col=index_col,
        na_values=ensure_list(na_values),
        dtype=dtypes,
    )

    df["YearsCode"] = df["YearsCode"].replace(
        {"Less than 1 year": "0", "More than 50 years": "51"}
    )
    df["YearsCode"] = pd.to_numeric(df["YearsCode"])

    return df


def fiter_by_x(df: pd.DataFrame, column: str, values: list):
    filtered = df[column] in ensure_list(values)
    return df.loc[filtered]


# df.agg({'col1':'mean','col2':sum})
# df.groupby('Country').apply(lambda x: x.sort_values('YearsCode'))

if __name__ == "__main__":
    import_csv()
