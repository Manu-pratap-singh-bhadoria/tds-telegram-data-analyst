import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.github.ai/inference",
)

SYSTEM_PROMPT = """
You are ONLY a tool routing agent.

Your job is to select ONE tool and its arguments.

Never answer the question yourself.

Return ONLY valid JSON.

Available tools

get_columns
get_rows
get_shape
get_head
get_tail
get_dtypes
get_missing
get_summary

mean
median
mode
max
min
sum
count
std
variance

unique
value_counts

sort_ascending
sort_descending

filter_equals

top_n
bottom_n

correlation

groupby_mean
groupby_sum
groupby_count

Rules

If user asks:
"How many rows?"
or
"Number of rows?"
Return

{
  "tool":"get_rows",
  "arguments":{}
}

If user asks:
"What is the shape?"
Return

{
  "tool":"get_shape",
  "arguments":{}
}

If user asks:
"What are the columns?"
Return

{
  "tool":"get_columns",
  "arguments":{}
}

If user asks:
"Show first rows"
Return

{
  "tool":"get_head",
  "arguments":{}
}

If user asks:
"Show last rows"
Return

{
  "tool":"get_tail",
  "arguments":{}
}

For mean

{
  "tool":"mean",
  "arguments":{
      "column":"salary"
  }
}

For median

{
  "tool":"median",
  "arguments":{
      "column":"salary"
  }
}

For max

{
  "tool":"max",
  "arguments":{
      "column":"salary"
  }
}

For min

{
  "tool":"min",
  "arguments":{
      "column":"salary"
  }
}

For sum

{
  "tool":"sum",
  "arguments":{
      "column":"salary"
  }
}

For std

{
  "tool":"std",
  "arguments":{
      "column":"salary"
  }
}

For variance

{
  "tool":"variance",
  "arguments":{
      "column":"salary"
  }
}

For value counts

{
  "tool":"value_counts",
  "arguments":{
      "column":"class"
  }
}

For unique

{
  "tool":"unique",
  "arguments":{
      "column":"state"
  }
}

For top N

{
  "tool":"top_n",
  "arguments":{
      "column":"salary",
      "n":5
  }
}

For bottom N

{
  "tool":"bottom_n",
  "arguments":{
      "column":"salary",
      "n":5
  }
}

For ascending sort

{
  "tool":"sort_ascending",
  "arguments":{
      "column":"salary"
  }
}

For descending sort

{
  "tool":"sort_descending",
  "arguments":{
      "column":"salary"
  }
}

For groupby mean

{
  "tool":"groupby_mean",
  "arguments":{
      "group_column":"department",
      "value_column":"salary"
  }
}

For groupby sum

{
  "tool":"groupby_sum",
  "arguments":{
      "group_column":"department",
      "value_column":"salary"
  }
}

IMPORTANT

For groupby_count NEVER send value_column.

Correct format

{
  "tool":"groupby_count",
  "arguments":{
      "group_column":"class"
  }
}

For correlation

{
  "tool":"correlation",
  "arguments":{}
}

If unsure return

{
  "tool":"unknown",
  "arguments":{}
}
"""

def choose_tool(question):
    q = question.lower().strip()

    if "how many rows" in q or "number of rows" in q:
        return {
            "tool": "get_rows",
            "arguments": {}
        }

    if "what are the columns" in q or "which columns" in q:
        return {
            "tool": "get_columns",
            "arguments": {}
        }

    if "what is the shape" in q:
        return {
            "tool": "get_shape",
            "arguments": {}
        }

    if "first 5 rows" in q or "show first rows" in q:
        return {
            "tool": "get_head",
            "arguments": {}
        }

    if "last 5 rows" in q or "show last rows" in q:
        return {
            "tool": "get_tail",
            "arguments": {}
        }

    if "data types" in q or "dtypes" in q:
        return {
            "tool": "get_dtypes",
            "arguments": {}
        }

    if "missing values" in q:
        return {
            "tool": "get_missing",
            "arguments": {}
        }

    if "summary statistics" in q:
        return {
            "tool": "get_summary",
            "arguments": {}
        }

    if "mean salary" in q or "average salary" in q:
        return {
            "tool": "mean",
            "arguments": {"column": "salary"}
        }

    if "average of the marks" in q or "mean marks" in q:
        return {
            "tool": "mean",
            "arguments": {"column": "marks"}
        }

    if "median marks" in q:
        return {
            "tool": "median",
            "arguments": {"column": "marks"}
        }

    if "maximum salary" in q or "max salary" in q:
        return {
            "tool": "max",
            "arguments": {"column": "salary"}
        }

    if "minimum marks" in q or "min marks" in q:
        return {
            "tool": "min",
            "arguments": {"column": "marks"}
        }

    if "sum of salary" in q or "total salary" in q:
        return {
            "tool": "sum",
            "arguments": {"column": "salary"}
        }

    if "standard deviation of salary" in q:
        return {
            "tool": "std",
            "arguments": {"column": "salary"}
        }

    if "variance of salary" in q:
        return {
            "tool": "variance",
            "arguments": {"column": "salary"}
        }

    if "value counts of class" in q or "value counts of the class" in q:
        return {
            "tool": "value_counts",
            "arguments": {"column": "class"}
        }

    if "unique states" in q:
        return {
            "tool": "unique",
            "arguments": {"column": "state"}
        }

    if "top 3 salaries" in q:
        return {
            "tool": "top_n",
            "arguments": {
                "column": "salary",
                "n": 3
            }
        }

    if "bottom 3 marks" in q:
        return {
            "tool": "bottom_n",
            "arguments": {
                "column": "marks",
                "n": 3
            }
        }

    if "sort by salary" in q:
        return {
            "tool": "sort_ascending",
            "arguments": {"column": "salary"}
        }

    if "marks descending" in q:
        return {
            "tool": "sort_descending",
            "arguments": {"column": "marks"}
        }

    if "group by department" in q and "mean salary" in q:
        return {
            "tool": "groupby_mean",
            "arguments": {
                "group_column": "department",
                "value_column": "salary"
            }
        }

    if "group by class" in q and "count" in q:
        return {
            "tool": "groupby_count",
            "arguments": {
                "group_column": "class"
            }
        }

    if "correlation matrix" in q:
        return {
            "tool": "correlation",
            "arguments": {}
        }

    return {
        "tool": "unknown",
        "arguments": {}
    }