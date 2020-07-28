'''
./app/masquer_bot.py

Brain of the Bot.
'''
import os
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
            '''
            Infiteloop as key pairs are genrated randomly, there is absolutely no way of
            knowing that same value is reapted or not. so db.seesion.commit() will return error if
            a exact same key is returned, due to unique contraint in UserAccount model.
            '''
            account = UserAccount(username)
            db.session.add(account)
            try:
                db.session.commit()
                help(message)
                get_key(message)
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
        bot.send_message(message.chat.id, "Here is your public key.")
        bot.send_message(message.chat.id, account.public_key)
    else:
        bot.reply_to(message, "Unable to fetch userkey.")


@bot.message_handler(commands=["help", "h"])
def help(message):
    bot.send_message(
        message.chat.id,
        "Hi I'm MasquerBot. I can masque any given <text> within any given <image>.\nHow this works is, everyone is given a public key, that public key is used to lock information, we call it public key as it can be publicly disctributed. So to masque a message, both sender and reciever must initiate MasquerBot's Service. Each message is masqued only for receiver, if receiver changes xer key then decryption would be impossible.",
    )
    bot.send_message(
        message.chat.id,
        "Here is the list of commands\n• /help: Get these same messages again.\n• /get_key: Get your public key.\n• /encrypt: Initate encryption process.\n• /decrypt: Initate decryption process.\n• /cancel: Cancel the ongoing process.\n• /request_new_key: Create new public key.",
    )


@bot.message_handler(commands=["encrypt", "e"])
def encryption_init(message):
    cancel(message, True)
    db.session.add(EncryptionCache(message.chat.id))
    try:
        db.session.commit()
        bot.send_message(
            message.chat.id,
            "Encryption process started!\nSend the *message* to be encrypted.",
            parse_mode="Markdown",
        )
    except:
        db.session.rollback()
        bot.reply_to(message, "Operation failed to start due to internal error.")


@bot.message_handler(commands=["decrypt", "d"])
def decryption_init(message):
    '''
    Once added to Database, handling is done by document_handler 
    '''
    cancel(message, True)
    db.session.add(DecryptionCache(message.chat.id))
    try:
        db.session.commit()
        bot.send_message(
            message.chat.id,
            "Decryption process started!\nSend the *image* _(as document)_ to be decrypted.",
            parse_mode="Markdown",
        )
    except:
        db.session.rollback()
        bot.reply_to(message, "Operation failed to start due to internal error.")


@bot.message_handler(commands=["cancel", "c"])
def cancel(message, in_call=False):
    '''
    in_call refers to function if called with anyother function rather than command handling
    Since we called cancel function within discryption and encrytion, so there
    is no way both will run in parallel. 
    '''
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
    # simple delete account and create new.
    username = message.from_user.username
    account = UserAccount.query.filter_by(
        username_hash=sha512(bytes(username, "utf-8")).hexdigest()
    ).first()

    if account is not None:
        try:
            db.session.delete(account)
            db.session.commit()
            while True:
                # Check start function for infinit loop informaton.
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


######## Some one liners.
@bot.message_handler(commands=["github"])
def github(message):
    bot.send_message(
        message.chat.id, "https://github.com/ra101/MasquerBot",
    )


@bot.message_handler(commands=["dev"])
def dev(message):
    bot.send_message(
        message.chat.id, "https://t.me/ra_101",
    )


@bot.message_handler(commands=["home"])
def home(message):
    bot.send_message(
        message.chat.id, "https://masquerbot.herokuapp.com/home.html",
    )


@bot.message_handler(commands=["icon"])
def icon(message):
    bot.send_message(
        message.chat.id,
        "The icon of the `MasquerBot` consists of 4 components.\n\n• *Masque*: It is the war-masque wore by `Tobi`. Whom every mistakes for `Uchiha Madara`, but he was actually `Uchiha Obito`. These multiple layers of facade fits the theme of the bot.\n\n• *Left Eye*: The `Rinne-Sharingan` is a dōjutsu kekkei mōra. It can be used to cast an illusionary technique that traps the whole world. It symbolizes the state-of-the-art encryption algorithm used in the bot.\n\n• *Right Eye*: The `Jōgan` is a unique dōjutsu. It can clearly see the key point in the chakra system. It represents the pixel-manipulation power of bot.",
        parse_mode="Markdown",
    )


########


@bot.message_handler(func=lambda message: True, content_types=["text"])
def text_handler(message):
    '''
    This function, handles message_for_encrytion, public_key and any random text.
    it checks in with EncryptionCache and decide on basis of result what to send back.
    '''
    e_cache = EncryptionCache.query.filter_by(chat_id=message.chat.id).first()
    if e_cache is not None:
        if e_cache.message is None:
            e_cache.message = message.text
            try:
                db.session.commit()
                bot.send_message(
                    message.chat.id,
                    "Message Accepted! Now send the *recepient's public key*.",
                    parse_mode="Markdown",
                )
            except:
                db.session.rollback()
                bot.reply_to(
                    message, "Operation failed to start due to internal error."
                )

        # RegEx match for public key.
        elif (fullmatch("[0][xX][0-9a-fA-F]+", message.text) is not None) and (
            len(message.text) == 130
        ):
            e_cache.public_key = message.text
            try:
                db.session.commit()
                bot.send_message(
                    message.chat.id,
                    "Key Accepted! Now send the *image* _(as document)_.",
                    parse_mode="Markdown",
                )
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
    '''
    This function downloads images, and see what to do with it,
    encrypt it, decrypt it or discard it.
    it check in with EncryptionCache and DecryptionCache and based on result decides what to do.
    '''

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

            # Encryption
            encrypted_text = encrypt(
                e_cache.public_key, bytes(e_cache.message, "utf-8")
            ).hex()

            # Steganography
            secret_img = hide(
                input_image=image_bytes, message=encrypted_text, auto_convert_rgb=True
            )

            # File Creation
            return_img = BytesIO()
            secret_img.save(return_img, format="PNG")  # only PNG works.
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

            # Reverse Steganography
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

                # Decryption
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
    func=lambda message: True,
    content_types=[
        "audio",
        "sticker",
        "video",
        "video_note",
        "voice",
        "location",
        "contact",
    ],
)
def unsupported_content_type_handler(message):
    bot.reply_to(message, "File Type is not supported.")
