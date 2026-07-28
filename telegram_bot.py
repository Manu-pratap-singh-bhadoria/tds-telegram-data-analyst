import os
import json
import pandas as pd

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

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATASET_DIR = "datasets"
os.makedirs(DATASET_DIR, exist_ok=True)

user_datasets = {}


def make_reply(answer):
    return {
        "answer": answer,
        "log_url": "https://raw.githubusercontent.com/Manu-pratap-singh-bhadoria/tds-telegram-data-analyst/refs/heads/main/logs/run.jsonl"
    }


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

        await update.message.reply_text(
            json.dumps(
                make_reply(
                    {
                        "status": "dataset uploaded",
                        "rows": len(df),
                        "columns": list(df.columns)
                    }
                ),
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

    question = update.message.text

    if chat_id not in user_datasets:

        await update.message.reply_text(
            json.dumps(
                make_reply(
                    {
                        "error": "Upload a CSV file first."
                    }
                )
            )
        )
        return

    df = user_datasets[chat_id]

    try:

        decision = choose_tool(question)

        tool_name = decision.get("tool")

        arguments = decision.get(
            "arguments",
            {}
        )

        if tool_name not in TOOLS:

            await update.message.reply_text(
                json.dumps(
                    make_reply(
                        {
                            "error": "Unknown tool"
                        }
                    )
                )
            )
            return

        function = TOOLS[tool_name]

        result = function(
            df,
            **arguments
        )

        await update.message.reply_text(
            json.dumps(
                make_reply(result),
                default=str
            )
        )

    except KeyError as e:

        await update.message.reply_text(
            json.dumps(
                make_reply(
                    {
                        "error": f"Column not found: {str(e)}"
                    }
                )
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


app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)

app.add_handler(
    MessageHandler(
        filters.Document.ALL,
        handle_document
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

print("Bot Running...")

app.run_polling()