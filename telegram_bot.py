import os
import json
import re
import io
import pandas as pd
import requests

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

from agent import choose_tool
from tool_registry import TOOLS
from logger import write_log


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATASET_DIR = "datasets"
os.makedirs(DATASET_DIR, exist_ok=True)

user_datasets = {}


LOG_URL = (
    "https://raw.githubusercontent.com/"
    "Manu-pratap-singh-bhadoria/"
    "tds-telegram-data-analyst/"
    "refs/heads/main/logs/run.jsonl"
)


def make_reply(answer):
    return {
        "answer": answer,
        "log_url": LOG_URL
    }


def load_csv_from_url(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return pd.read_csv(io.BytesIO(response.content))


def find_csv_url(text):
    if "https://" in text:
        url = text.rsplit("https://", 1)[1]
        url = "https://" + url
        url = url.split(")", 1)[0]
        url = url.split(" ", 1)[0]
        return url.strip("[]<>.,;'\"")

    if "http://" in text:
        url = text.rsplit("http://", 1)[1]
        url = "http://" + url
        url = url.split(")", 1)[0]
        url = url.split(" ", 1)[0]
        return url.strip("[]<>.,;'\"")

    return None



async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    if document is None:
        return

    if not document.file_name.lower().endswith(".csv"):
        await update.message.reply_text(
            json.dumps(
                make_reply(
                    {"error": "Please upload a CSV file."}
                )
            )
        )
        return

    telegram_file = await document.get_file()

    path = os.path.join(
        DATASET_DIR,
        document.file_name
    )

    await telegram_file.download_to_drive(path)

    try:

        df = pd.read_csv(path)

        user_datasets[
            update.effective_chat.id
        ] = df

        result = {
            "status": "dataset uploaded",
            "rows": len(df),
            "columns": list(df.columns)
        }

        await update.message.reply_text(
            json.dumps(
                make_reply(result),
                default=str
            )
        )

    except Exception as e:

        await update.message.reply_text(
            json.dumps(
                make_reply(
                    {
                        "error": str(e)
                    }
                )
            )
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    question = update.message.text or ""

    try:

        # ---------------------------------------------------------
        # 1. Check whether the message contains a public CSV URL
        # ---------------------------------------------------------

        csv_url = find_csv_url(question)

        print("QUESTION:", repr(question))
        print("EXTRACTED CSV URL:", repr(csv_url))

        if csv_url:
            df = load_csv_from_url(csv_url)

            user_datasets[chat_id] = df

        # ---------------------------------------------------------
        # 2. Otherwise use the dataset already stored for this chat
        # ---------------------------------------------------------

        elif chat_id in user_datasets:

            df = user_datasets[chat_id]

        # ---------------------------------------------------------
        # 3. No dataset available
        # ---------------------------------------------------------

        else:

            result = {
                "error": (
                    "No dataset found. "
                    "Please provide a public CSV URL in the message."
                )
            }

            write_log(
                question,
                "dataset_error",
                result
            )

            await update.message.reply_text(
                json.dumps(
                    make_reply(result),
                    default=str
                )
            )

            return

        # ---------------------------------------------------------
        # 4. Ask the LLM which analysis tool to use
        # ---------------------------------------------------------

        decision = choose_tool(question)

        tool_name = decision.get("tool")

        arguments = decision.get(
            "arguments",
            {}
        )

        # ---------------------------------------------------------
        # 5. Validate tool
        # ---------------------------------------------------------

        if tool_name not in TOOLS:

            result = {
                "error": "Unknown tool"
            }

            write_log(
                question,
                tool_name,
                result
            )

            await update.message.reply_text(
                json.dumps(
                    make_reply(result),
                    default=str
                )
            )

            return

        # ---------------------------------------------------------
        # 6. Execute analysis
        # ---------------------------------------------------------

        function = TOOLS[tool_name]

        result = function(
            df,
            **arguments
        )

        # ---------------------------------------------------------
        # 7. Write log
        # ---------------------------------------------------------

        write_log(
            question,
            tool_name,
            result
        )

        # ---------------------------------------------------------
        # 8. Return exactly one JSON object
        # ---------------------------------------------------------

        await update.message.reply_text(
            json.dumps(
                make_reply(result),
                default=str
            )
        )

    except KeyError as e:

        result = {
            "error": f"Column not found: {str(e)}"
        }

        write_log(
            question,
            "error",
            result
        )

        await update.message.reply_text(
            json.dumps(
                make_reply(result),
                default=str
            )
        )

    except Exception as e:

        result = {
            "error": str(e)
        }

        write_log(
            question,
            "error",
            result
        )

        await update.message.reply_text(
            json.dumps(
                make_reply(result),
                default=str
            )
        )


app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)


# CSV attachment handler
app.add_handler(
    MessageHandler(
        filters.Document.ALL,
        handle_document
    )
)


# Normal text message handler
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)


if __name__ == "__main__":
    print("Bot Running...")
    app.run_polling()
