import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from bot.performance import liner, multithreaded, multiprocessed, liner_pi, mt_pi, mp_pi

import logging
from telegram import Update
from telegram.ext import ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def creds():
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None

    if os.path.exists('token.json'):
        cerds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not cerds.valid:
        if creds and creds.expired and creds.refresh_token:
            cerds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', "w") as token:
            token.write(creds.to_json())
    return creds


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="talk to me ")


async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        service = build('drive', 'v3', credentials=creds())

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print("files:")
        for item in items:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=item.get("name"))
            print(u'{0} ({1})'.format(item['name'], item['id']))

    except HttpError as error:
        print(f"an erro occurred {error}")


async def upload_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    newFile = await update.message.effective_attachment.get_file()
    await newFile.download(custom_path="downloaded/" + update.message.effective_attachment.file_name)

    try:
        service = build('drive', 'v3', credentials=creds())

        file_metdata = {'name': update.message.document.file_name}
        media = MediaFileUpload("downloaded/"+update.message.document.file_name,
                                mimetype=update.message.document.mime_type, resumable=True)
        file = service.files().create(body=file_metdata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')
    except HttpError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="failure")
        print(f"error occurred {e}")
        file = None

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Successfully uploaded file")

    return file.get("id")

FIRST, SECOND = range(2)


async def cpython(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(u"Search", callback_data=str(FIRST))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(u"first example", reply_markup=reply_markup)
    return FIRST


async def search_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    keyboard = [
        [InlineKeyboardButton(u"Pi", callback_data=(SECOND))]
    ]
    index = ((2**31-1) // 32 - 1)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="lin: " + liner(index))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="mt: " + multithreaded(index))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="mp: " + multiprocessed(index))

    # reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                        text=u"Second module")

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                                reply_markup=reply_markup)

    return SECOND


async def pi_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query


    await context.bot.send_message(chat_id=update.effective_chat.id, text="lin: "+liner_pi(100000000))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="mt: "+mt_pi(100000000))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="mp: "+mp_pi(100000000))


    await context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=u"You can add more CPU bound modules")