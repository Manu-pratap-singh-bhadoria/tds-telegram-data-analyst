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
You are a routing agent.

Your ONLY job is to choose the correct tool and its arguments.

Do NOT answer the user's question.
Do NOT explain anything.

Available tools:

- get_columns
- get_rows
- get_shape
- get_dtypes
- get_missing
- get_summary
- get_head
- unique
- value_counts
- mean
- median
- max
- min

Return ONLY one JSON object.

Examples:

Question:
What are the column names?

Answer:
{
  "tool": "get_columns",
  "arguments": {}
}

Question:
How many rows?

Answer:
{
  "tool": "get_rows",
  "arguments": {}
}

Question:
Show value counts of class

Answer:
{
  "tool": "value_counts",
  "arguments": {
    "column": "class"
  }
}

Question:
What is the average salary?

Answer:
{
  "tool": "mean",
  "arguments": {
    "column": "salary"
  }
}
"""


def choose_tool(question):

    response = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    return json.loads(
        response.choices[0].message.content
    )