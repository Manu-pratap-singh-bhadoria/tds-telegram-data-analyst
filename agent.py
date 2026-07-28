import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com",
)

SYSTEM_PROMPT = """
You are an intelligent routing agent.

Your ONLY job is to choose the correct tool and arguments.

DO NOT answer the user's question.
DO NOT explain anything.
DO NOT generate text.

Return ONLY a JSON object.

Available tools:

Dataset Information
- get_columns
- get_rows
- get_shape
- get_head
- get_tail
- get_dtypes
- get_missing
- get_summary

Statistics
- mean
- median
- mode
- max
- min
- sum
- count
- std
- variance

Values
- unique
- value_counts

Sorting
- sort_ascending
- sort_descending

Filtering
- filter_equals

Ranking
- top_n
- bottom_n

Group By
- groupby_mean
- groupby_sum
- groupby_count

Relationships
- correlation

Rules

1. Return ONLY JSON.

2. Use this format:

{
  "tool":"tool_name",
  "arguments":{}
}

3. If a column is needed, include:

{
  "tool":"mean",
  "arguments":{
      "column":"salary"
  }
}

4. For top or bottom rows:

{
  "tool":"top_n",
  "arguments":{
      "column":"salary",
      "n":5
  }
}

5. For filtering:

{
  "tool":"filter_equals",
  "arguments":{
      "column":"class",
      "value":"A"
  }
}

6. For groupby mean:

{
  "tool":"groupby_mean",
  "arguments":{
      "group_column":"department",
      "value_column":"salary"
  }
}

7. If no tool matches, return

{
   "tool":"unknown",
   "arguments":{}
}
"""


def choose_tool(question):

    response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    try:
        return json.loads(
            response.choices[0].message.content
        )
    except Exception:
        return {
            "tool": "unknown",
            "arguments": {}
        }