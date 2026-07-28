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

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    if not document.file_name.lower().endswith(".csv"):
        await update.message.reply_text(
            json.dumps({"error": "Please upload a CSV file."})
        )
        return

    telegram_file = await document.get_file()

    path = os.path.join(DATASET_DIR, document.file_name)

    await telegram_file.download_to_drive(path)

    df = pd.read_csv(path)

    user_datasets[update.effective_chat.id] = df

    await update.message.reply_text(
        json.dumps({"status": "dataset uploaded"})
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    if chat_id not in user_datasets:
        await update.message.reply_text(
            json.dumps({"error": "Upload a CSV file first."})
        )
        return

    df = user_datasets[chat_id]

    question = update.message.text

    try:

        decision = choose_tool(question)

        tool_name = decision.get("tool")

        arguments = decision.get("arguments", {})

        if tool_name not in TOOLS:
            await update.message.reply_text(
                json.dumps({"error": "Unknown tool"})
            )
            return

        function = TOOLS[tool_name]

        result = function(df, **arguments)
        from logger import write_log
        write_log(question, tool_name, result)

        reply = {
            "answer": result,
            "log_url": "https://example.com/run.jsonl"
        }

        await update.message.reply_text(
            json.dumps(reply, default=str)
        )

    except Exception as e:

        await update.message.reply_text(
            json.dumps(
                {
                    "error": str(e)
                }
            )
        )


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.Document.ALL, handle_document)
)

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

print("Bot Running...")

app.run_polling()