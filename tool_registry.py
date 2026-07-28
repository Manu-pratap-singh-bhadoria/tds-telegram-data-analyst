from tools import DataTools

TOOLS = {

    "get_columns": DataTools.get_columns,
    "get_rows": DataTools.get_rows,
    "get_shape": DataTools.get_shape,

    "get_head": DataTools.get_head,
    "get_tail": DataTools.get_tail,

    "get_dtypes": DataTools.get_dtypes,
    "get_missing": DataTools.get_missing,
    "get_summary": DataTools.get_summary,

    "unique": DataTools.unique,
    "value_counts": DataTools.value_counts,

    "mean": DataTools.mean,
    "median": DataTools.median,
    "mode": DataTools.mode,

    "max": DataTools.maximum,
    "min": DataTools.minimum,
    "sum": DataTools.total,
    "count": DataTools.count,

    "std": DataTools.std,
    "variance": DataTools.variance,

    "max_row": DataTools.maximum_row,
    "min_row": DataTools.minimum_row,

    "sort_ascending": DataTools.sort_ascending,
    "sort_descending": DataTools.sort_descending,

    "filter_equals": DataTools.filter_equals,

    "top_n": DataTools.top_n,
    "bottom_n": DataTools.bottom_n,

    "correlation": DataTools.correlation,

    "groupby_mean": DataTools.groupby_mean,
    "groupby_sum": DataTools.groupby_sum,
    "groupby_count": DataTools.groupby_count,
}