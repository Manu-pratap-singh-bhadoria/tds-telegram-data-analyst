import pandas as pd


class DataTools:

    @staticmethod
    def get_columns(df):
        return {"columns": list(df.columns)}

    @staticmethod
    def get_rows(df):
        return {"rows": len(df)}

    @staticmethod
    def get_shape(df):
        return {"shape": list(df.shape)}

    @staticmethod
    def get_head(df):
        return {"head": df.head().to_dict(orient="records")}

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
            "summary": df.describe(include="all").fillna("").to_dict()
        }

    @staticmethod
    def unique(df, column):
        return {
            "unique": df[column].dropna().unique().tolist()
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
    def max(df, column):
        return {
            "max":
                df[column].max()
        }

    @staticmethod
    def min(df, column):
        return {
            "min":
                df[column].min()
        }