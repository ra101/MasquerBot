
<div align="center">
<p align="center">
  <img src="./assets/logo_circle.png" width="250px" height="250px">
</p>

 <a href="https://t.me/MasquerBot" alt="https://t.me/MasquerBot" ><h2> https://t.me/MasquerBot </h2> </a> 

<img src="https://img.shields.io/badge/Made%20with-Python-feab00?style=for-the-badge&amp;logo=python" alt="Made with Python"> <a href="https://github.com/ra101/MasquerBot/stargazers"><img src="https://img.shields.io/github/stars/ra101/MasquerBot?style=for-the-badge" alt="Stars"></a> <a href="https://github.com/ra101/MasquerBot/network/members"><img src="https://img.shields.io/github/forks/ra101/MasquerBot?style=for-the-badge" alt="Forks"></a> <a href="https://github.com/ra101/MasquerBot/issues"><img src="https://img.shields.io/github/issues/ra101/MasquerBot?style=for-the-badge" alt="Open Issues"> </a><img src="https://img.shields.io/badge/Open%20Source-%E2%98%95-red?style=for-the-badge&amp;logo=open-source-initiative" alt="Open Source Love">  <img src="https://img.shields.io/badge/Built%20With-%E2%99%A1-critical?style=for-the-badge&amp;logo=github" alt="Built with Love">

</div>

This `TelegramBot` uses state-of-the-art encryption algorithm *(ECDSA)* and pixel manipulation *(steganography)* to masque any given `<text>` within any given `<image>`.

- _If you truly have a paranoia about security. A VPN is recommended during [/encrypt](#desktop_computer-available-commands) and [/decrypt](#desktop_computer-available-commands)._

- _PNGs are recommended better performance._

<br>

**Video Tutorial:** [LRBY](https://lbry.tv/@ra101/MasquerBot)  |  [YouTube](https://www.youtube.com/watch?v=yH3SVmCZD7Q)

<p align="center">
 <iframe id="odysee-iframe" style="width:74vw;height:42vw;" src="https://odysee.com/$/embed/MasquerBot/11376992c29c54efde884284b298a1290ae8d7f8?r=45vpskZGbEGUURSfgbmqd6b53WGvvGuh" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</p>


<br><br>

## 💼About

### 📈Workflow

How this works is, everyone is given a public key, that public key is used to lock information, we call it public key as it can be publicly distributed. 

So to masque a message both sender and receiver must initiate MasquerBot's Service. Each message is masqued only for receiver, if receiver changes xer key then decryption would be impossible.

<br>

### 🖥Available Commands:

- [**/start**](#desktop_computer-available-commands):  It starts and calls **/help** and **/get_key**
- [**/lbry**](#desktop_computer-available-commands) or [**/youtube**](#desktop_computer-available-commands): Return a link of video tutorial. 
- [**/help**](#desktop_computer-available-commands):  Returns the `Workflow` and `Available Commands` .
- [**/get_key**](#desktop_computer-available-commands):  Returns your `public key`.
- [**/encrypt**](#desktop_computer-available-commands):  Returns the `encoded image`.
  - Step 1: Send the `message` to encrypt.
  - Step 2: Send the recipient's `public key` **(not yours)**.
  - Step 3: Send the `image` **(as document)**.
- [**/decrypt**](#desktop_computer-available-commands):  Returns the `hidden text`.
  - Step 1: Send the `encoded image` **(as document)**.
- [**/cancel**](#desktop_computer-available-commands):  Cancels any ongoing events.
- [**/request_new_key**](#desktop_computer-available-commands):  Deletes your account and creates another one. **Beware! Once deleted you cant retrieve any text masqued using previous key.** 

<br>

### ⚡Features:

- Saves `Hashes` instead of username.
- `unique contraint` prevents duplicacy. 
- Message is first `encrypted` then `steganography` is performed.
- `ECDSA` is used. which means less time on computation and powerful encryption.
- `Dynamic URL`: URL changes every `6 hours and 5 minutes`, with `130 char long`, therefore making it impossible to send through any means other than telegram since URL remains unknown to everyone except telegram.
- `Gunicorn` creates multiple workers hence supporting parallel processing.
- Process Management: All process are cancelled before starting a new one. `Triggers` are added to delete any process with timestamp older than 10 minutes.
- Few cool `Easter Eggs` are there as well.



<br>

## ⚙Development

### 💾Setup

The following are the bare necessities for this project.

- [Python3](https://www.python.org/downloads/)
- [TelegramBot with its API key](https://core.telegram.org/bots#3-how-do-i-create-a-bot)



Lets start the standard procedure for python project setup.

- Clone the repository

```bash
$ git clone https://github.com/ra101/MasqureBot.git
```

- Create the virtualenv and activate it

```bash
$ cd MasqureBot
$ virtualenv .
$ source ./bin/activate # unix
$ .\Scripts\activate.bat  # windows
```

- Install requirements
```bash
$ pip install -r requirements.txt
```

<br>

### 💻Run on localhost

To run the project locally download and install

- [ngrok](https://ngrok.com/download)



Following are the steps to run locally

- copy content of .env.template into .env *(one can use [dump-env](https://github.com/sobolevn/dump-env) as well)*

```bash
$ cat .env.template > .env
```

- Fillup the basic info.

```bash
DOMAIN_NAME=


# Flask Variables
# ------------
FLASK_DEBUG=True
FLASK_ENV=development
FLASK_SECRET_KEY=my_precious


# SQLAlchemy Variables
# ------------
DATABASE_URL=
SQLALCHEMY_TRACK_MODIFICATIONS=True


# Telegram Credentials
# ------------
TELEGRAM_BOT_TOKKEN=<your_bot_token>
```



- For `DOMAIN_NAME`

  - run the following command

    ```bash
    $ ngrok http 8000
    ```

  - This will create a local tunnel with address like `https://<nonce>.ngrok.io` that is your value for domain.

- For `DATABASE_URL` 

  - If you use SQLite, that create a file and it does not need any other software. `sqlite:///foo.db`

    is the value for `DATABASE_URL` is that case.

  - For any other SQL the syntax is `dialect+driver://username:password@host:port/database` , here `dialect` refers to SQL. We have used postgreSQL which uses `psycopg2` as default driver which is installed from `requirements.txt`



- Run the application!

```bash
$ make
```

or 

```bash
$ gunicorn wsgi:application -c scheduler.py
```

<br>

###  ☁Run on Server

Following are the steps to run on server.

- If you can host .env, then the steps are pretty much same as running locally, except for `DOMAIN_NAME` , it will be provided by hosting provider.

- If you can't host .env like in case of `heroku`, then you need to export each variable into hosting providers environment.


<br><br>


## 📃Breakdown of `requirements.txt`

| Dependency       | Usage                                                        |
| ---------------- | ------------------------------------------------------------ |
| APScheduler      | Creates a background scheduler in `scheduler.py` which changes webhook URL in every 6 hours and 5 minutes |
| eciespy          | Generates ECDSA key pair and also provides encryption and decryption functionality |
| Flask            | Flask is a lightweight [WSGI](https://wsgi.readthedocs.io/) web application framework. |
| Flask-RESTful    | Adds support for quickly building REST APIs.                 |
| Flask-SQLAlchemy | Provides a Object Relation Mapper which is meant to integrate with |
| gunicorn         | It is a Python WSGI HTTP server. It is a pre-fork worker model, used to create concurrency for resources. |
| psycopg2-binary  | Driver for postgreSQL used by Flask-SQLAlchemy               |
| pyTelegramBotAPI | A simple, but extensible Python implementation for the Telegram Bot API. |
| python-dotenv    | Reads the key-value pair from `.env` file and adds them to environment variable. |
| stegano          | A pure Python Steganography module.                          |

<br><br>


## 🎁Donations

<a href="https://www.buymeacoffee.com/ra101"><img src="https://www.buymeacoffee.com/assets/img/custom_images/black_img.png" title="If this project is helpful to you and love my work and feel like showing love/appreciation, would you like to buy me a coffee?" ></a>

<br>

## 🌟Credit/Acknowledgment

[![Contributors](https://img.shields.io/github/contributors/ra101/MasquerBot?style=for-the-badge)](https://github.com/ra101/MasquerBot/graphs/contributors)

<br>

## 📜License

[![License](https://img.shields.io/github/license/ra101/MasquerBot?style=for-the-badge)](https://github.com/ra101/MasquerBot/blob/core/LICENSE)

<br>

## 🤙Contact Me

[![Protonmail](https://img.shields.io/badge/Protonmail-Email-ab44fe?style=for-the-badge&logo=protonmail)](mailto://agarwal.parth.101@protonmail.com) [![Telegram](https://img.shields.io/badge/Telegram-Chat-informational?style=for-the-badge&logo=telegram)](https://telegram.me/ra_101)
