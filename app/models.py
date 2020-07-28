'''
./app/models.py
'''
from datetime import datetime, timedelta
from hashlib import sha512

from flask_sqlalchemy import SQLAlchemy
from ecies.utils import generate_eth_key

db = SQLAlchemy()


class UserAccount(db.Model):
    __tablename__ = "user_accounts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_hash = db.Column(db.Text(), unique=True, nullable=False)
    private_key = db.Column(db.Text(), unique=True, nullable=False)
    public_key = db.Column(db.Text(), unique=True, nullable=False)

    def __init__(self, username):
        self.username_hash = sha512(bytes(username, "utf-8")).hexdigest()
        eth_k = generate_eth_key()
        self.private_key = eth_k.to_hex()
        self.public_key = eth_k.public_key.to_hex()
        del eth_k


'''
One might argue Cache Tables are not required and these values can be stored in variables, but
since there are workers and we dont know which worker will hit when, so there is a need for
constant Database.
'''


class EncryptionCache(db.Model):
    __tablename__ = "encryption_cache"
    chat_id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.Text(), nullable=True)
    message = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime())
    # A Photo is excluded due to size limit and thefore is asked at last in encryption process.

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.created_at = datetime.now()
        self.message = None
        self.public_key = None


class DecryptionCache(db.Model):
    __tablename__ = "decryption_cache"
    chat_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime())
    # A Photo is excluded due to size limit and thefore is asked at last in encryption process.

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.created_at = datetime.now()


'''
These triggers are for saving memory,
One might suggest of adding scheduler for that, we have added schedular at start
before starting flask app. so DB could not have been accesible there.
'''


@db.event.listens_for(UserAccount, "before_insert")
def delete_trigger_cache(mapper, connection, target):
    delete_function()


@db.event.listens_for(EncryptionCache, "before_insert")
def delete_trigger_cache(mapper, connection, target):
    delete_function()


@db.event.listens_for(DecryptionCache, "before_insert")
def delete_trigger_cache(mapper, connection, target):
    delete_function()


def delete_function():
    try:
        db.session.query(EncryptionCache).filter(
            (EncryptionCache.created_at + timedelta(seconds=600)) < datetime.now()
        ).delete()
    except:
        db.seesion.rollback()
        pass

    try:
        db.session.query(DecryptionCache).filter(
            (DecryptionCache.created_at + timedelta(seconds=600)) < datetime.now()
        ).delete()
    except:
        db.seesion.rollback()
        pass
