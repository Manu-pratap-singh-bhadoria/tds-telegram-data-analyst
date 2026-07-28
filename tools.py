import pandas as pd


class DataTools:

    @staticmethod
    def get_columns(df):
        return {
            "columns": list(df.columns)
        }

    @staticmethod
    def get_rows(df):
        return {
            "rows": len(df)
        }

    @staticmethod
    def get_shape(df):
        return {
            "shape": list(df.shape)
        }

    @staticmethod
    def get_head(df, n=5):
        return {
            "head": df.head(n).to_dict(orient="records")
        }

    @staticmethod
    def get_tail(df, n=5):
        return {
            "tail": df.tail(n).to_dict(orient="records")
        }

    @staticmethod
    def get_dtypes(df):
        return {
            "dtypes": {
                c: str(t)
                for c, t in df.dtypes.items()
            }
        }

    @staticmethod
    def get_missing(df):
        return {
            "missing": df.isnull().sum().to_dict()
        }

    @staticmethod
    def get_summary(df):
        return {
            "summary":
                df.describe(include="all").fillna("").to_dict()
        }

    @staticmethod
    def unique(df, column):
        return {
            "unique":
                df[column].dropna().unique().tolist()
        }

    @staticmethod
    def value_counts(df, column):
        return {
            "counts":
                df[column].value_counts().to_dict()
        }

    @staticmethod
    def mean(df, column):
        return {
            "mean":
                float(df[column].mean())
        }

    @staticmethod
    def median(df, column):
        return {
            "median":
                float(df[column].median())
        }

    @staticmethod
    def mode(df, column):
        return {
            "mode":
                df[column].mode().tolist()
        }

    @staticmethod
    def maximum(df, column):
        return {
            "max":
                df[column].max()
        }

    @staticmethod
    def minimum(df, column):
        return {
            "min":
                df[column].min()
        }

    @staticmethod
    def total(df, column):
        return {
            "sum":
                float(df[column].sum())
        }

    @staticmethod
    def count(df, column):
        return {
            "count":
                int(df[column].count())
        }

    @staticmethod
    def std(df, column):
        return {
            "std":
                float(df[column].std())
        }

    @staticmethod
    def variance(df, column):
        return {
            "variance":
                float(df[column].var())
        }

    @staticmethod
    def minimum_row(df, column):
        row = df.loc[df[column].idxmin()]
        return {
            "row":
                row.to_dict()
        }

    @staticmethod
    def maximum_row(df, column):
        row = df.loc[df[column].idxmax()]
        return {
            "row":
                row.to_dict()
        }

    @staticmethod
    def sort_ascending(df, column):
        return {
            "rows":
                df.sort_values(column).to_dict(orient="records")
        }

    @staticmethod
    def sort_descending(df, column):
        return {
            "rows":
                df.sort_values(column, ascending=False)
                .to_dict(orient="records")
        }

    @staticmethod
    def filter_equals(df, column, value):
        return {
            "rows":
                df[df[column] == value]
                .to_dict(orient="records")
        }

    @staticmethod
    def top_n(df, column, n=5):
        return {
            "rows":
                df.nlargest(n, column)
                .to_dict(orient="records")
        }

    @staticmethod
    def bottom_n(df, column, n=5):
        return {
            "rows":
                df.nsmallest(n, column)
                .to_dict(orient="records")
        }

    @staticmethod
    def correlation(df):
        numeric = df.select_dtypes(include="number")
        return {
            "correlation":
                numeric.corr().fillna("").to_dict()
        }

    @staticmethod
    def groupby_mean(df, group_column, value_column):
        result = (
            df.groupby(group_column)[value_column]
            .mean()
            .to_dict()
        )

        return {
            "groupby_mean": result
        }

    @staticmethod
    def groupby_sum(df, group_column, value_column):
        result = (
            df.groupby(group_column)[value_column]
            .sum()
            .to_dict()
        )

        return {
            "groupby_sum": result
        }

    @staticmethod
    def groupby_count(df, group_column, value_column=None):
        result = df.groupby(group_column).size().to_dict()
        return {
            "groupby_count": result
        }
