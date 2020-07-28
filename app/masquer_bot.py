import os
import json
from io import BytesIO
from re import fullmatch
from hashlib import sha512
from requests import get as requests_get

import telebot
from dotenv import load_dotenv
from stegano.lsb import hide, reveal
from ecies import encrypt, decrypt

from app.utils import decode_hex
from app.models import db, UserAccount, EncryptionCache, DecryptionCache


load_dotenv()

# init Bot
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKKEN")
bot = telebot.TeleBot(telegram_bot_token, threaded=False)


@bot.message_handler(commands=["start", "s"])
def start(message):
    username = message.from_user.username
    account = UserAccount.query.filter_by(
        username_hash=sha512(bytes(username, "utf-8")).hexdigest()
    ).first()
    if account is not None:
        bot.reply_to(
            message,
            "Account is already established.\n/get_key or /gk to get your key.",
        )
    else:
        while True:
            account = UserAccount(username)
            db.session.add(account)
            try:
                db.session.commit()
                bot.send_message(message.chat.id, str(account.public_key))
                break
            except:
                db.session.rollback()
                pass


@bot.message_handler(commands=["get_key", "gk"])
def get_key(message):
    username = message.from_user.username
    account = UserAccount.query.filter_by(
        username_hash=sha512(bytes(username, "utf-8")).hexdigest()
    ).first()
    if account is not None:
        bot.send_message(message.chat.id, account.public_key)
    else:
        bot.reply_to(message, "Unable to fetch userkey.")


@bot.message_handler(commands=["help", "h"])
def help(message):
    bot.send_message(message.chat.id, "Yo! help arrived!")


@bot.message_handler(commands=["encrypt", "e"])
def encryption_init(message):
    cancel(message, True)
    db.session.add(EncryptionCache(message.chat.id))
    try:
        db.session.commit()
        bot.send_message(
            message.chat.id,
            "Encryption process started!\nSend the message to be encrypted.",
        )
    except:
        db.session.rollback()
        bot.reply_to(message, "Operation failed to start due to internal error.")


@bot.message_handler(commands=["decrypt", "d"])
def decryption_init(message):
    cancel(message, True)
    db.session.add(DecryptionCache(message.chat.id))
    try:
        db.session.commit()
        bot.send_message(
            message.chat.id,
            "Decryption process started!\nSend the image to be decrypted.",
        )
    except:
        db.session.rollback()
        bot.reply_to(message, "Operation failed to start due to internal error.")


@bot.message_handler(commands=["cancel", "c"])
def cancel(message, in_call=False):

    e_cache = EncryptionCache.query.filter_by(chat_id=message.chat.id).first()
    d_cache = DecryptionCache.query.filter_by(chat_id=message.chat.id).first()

    if e_cache is not None:
        db.session.delete(e_cache)
        try:
            db.session.commit()
            bot.send_message(message.chat.id, "Former encryption process canceled.")
        except:
            db.session.rollback()
            bot.reply_to(message, "Operation failed to start due to internal error.")

    elif d_cache is not None:
        db.session.delete(d_cache)
        try:
            db.session.commit()
            bot.send_message(message.chat.id, "Former decryption process canceled.")
        except:
            db.session.rollback()
            bot.reply_to(message, "Operation failed to start due to internal error.")

    elif not in_call:
        bot.reply_to(message, "Found no process associated with you.")


@bot.message_handler(commands=["request_new_key", "rnk"])
def request_new_key(message):
    username = message.from_user.username
    account = UserAccount.query.filter_by(
        username_hash=sha512(bytes(username, "utf-8")).hexdigest()
    ).first()

    if account is not None:
        try:
            db.session.delete(account)
            db.session.commit()
            while True:
                account = UserAccount(username)
                db.session.add(account)
                try:
                    db.session.commit()
                    bot.send_message(message.chat.id, "New key created!")
                    bot.send_message(message.chat.id, str(account.public_key))
                    break
                except:
                    db.session.rollback()
        except:
            db.session.rollback()
            bot.reply_to(message, "Operation failed to start due to internal error.")
    else:
        bot.reply_to(message, "Account not found.")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def text_handler(message):

    e_cache = EncryptionCache.query.filter_by(chat_id=message.chat.id).first()
    if e_cache is not None:
        if e_cache.message is None:
            e_cache.message = message.text
            try:
                db.session.commit()
                bot.send_message(
                    message.chat.id,
                    "Message Accepted! Now send the recepient's public key.",
                )
            except:
                db.session.rollback()
                bot.reply_to(
                    message, "Operation failed to start due to internal error."
                )

        elif (fullmatch("[0][xX][0-9a-fA-F]+", message.text) is not None) and (
            len(message.text) == 130
        ):
            e_cache.public_key = message.text
            try:
                db.session.commit()
                bot.send_message(message.chat.id, "Key Accepted! Now send the image.")
            except:
                db.session.rollback()
                bot.reply_to(
                    message, "Operation failed to start due to internal error."
                )
        else:
            bot.send_message(message.chat.id, "Invalid Key! Send Again.")
    else:
        bot.reply_to(message, "Text Discarded! Found no process associated with you.")


@bot.message_handler(func=lambda message: True, content_types=["document"])
def document_handler(message):
    bot.send_message(message.chat.id, "This might take few seconds...")
    file_info = bot.get_file(message.document.file_id)
    response = requests_get(
        "https://api.telegram.org/file/bot%s/%s"
        % (telegram_bot_token, file_info.file_path)
    )
    image_bytes = BytesIO(response.content)
    del response

    e_cache = EncryptionCache.query.filter_by(chat_id=message.chat.id).first()
    d_cache = DecryptionCache.query.filter_by(chat_id=message.chat.id).first()

    if e_cache is not None:
        db.session.delete(e_cache)
        try:
            db.session.commit()
            encrypted_text = encrypt(
                e_cache.public_key, bytes(e_cache.message, "utf-8")
            ).hex()
            secret_img = hide(
                input_image=image_bytes, message=encrypted_text, auto_convert_rgb=True
            )
            return_img = BytesIO()
            secret_img.save(return_img, format="PNG")
            return_img.name = file_info.file_path.split("/")[-1]
            return_img.seek(0)
            bot.send_document(message.chat.id, return_img)
            bot.send_message(message.chat.id, "Image encrypted!")

        except:
            db.session.rollback()
            bot.reply_to(message, "Operation failed to start due to internal error.")

    elif d_cache is not None:
        db.session.delete(d_cache)
        try:
            db.session.commit()
            encrypted_hex = reveal(input_image=image_bytes)
            if encrypted_hex is not None:
                encrypted_text = decode_hex(encrypted_hex)

                username = message.from_user.username
                private_key = (
                    UserAccount.query.filter_by(
                        username_hash=sha512(bytes(username, "utf-8")).hexdigest()
                    )
                    .first()
                    .private_key
                )

                decrypted_text = decrypt(private_key, encrypted_text)

                bot.reply_to(message, decrypted_text)
                bot.send_message(message.chat.id, "Image decrypted!")

            else:
                bot.reply_to(
                    message, "MasquerBot was not able to find any hidden text."
                )
        except:
            db.session.rollback()
            bot.reply_to(message, "Operation failed to start due to internal error.")

    else:
        bot.reply_to(message, "Image Discarded! Found no process associated with you.")


@bot.message_handler(func=lambda message: True, content_types=["photo"])
def photo_handler(message):
    bot.reply_to(message, "Send Image as document.")


@bot.message_handler(
    func=lambda message: message.content_type not in ["text", "photo", "document"]
)
def unsupported_content_type_handler(message):
    bot.reply_to(message, "File Type is not supported.")
