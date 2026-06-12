import pandas as pd


def load_file(file):

    if file.name.endswith(".csv"):

        return pd.read_csv(file)

    elif (
        file.name.endswith(".xlsx")
        or file.name.endswith(".xls")
    ):

        return pd.read_excel(file)

    return None


def dataframe_summary(df):

    return f"""
Rows: {len(df)}

Columns:
{', '.join(df.columns)}

First 20 Rows:

{df.head(20).to_string(index=False)}

Statistics:

{df.describe(include="all").to_string()}
"""