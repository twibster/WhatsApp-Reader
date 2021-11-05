![flask](https://img.shields.io/badge/Flask-v2.0.1-blue.svg?&logo=flask&color=success)
![python](https://img.shields.io/badge/python-v3.9-blue.svg?&logo=python&logoColor=yellow)
![GitHub repo size](https://img.shields.io/github/repo-size/twibster/IEEE-ZSB?color=red&logo=github)
![Lines of code](https://img.shields.io/tokei/lines/github/twibster/IEEE-ZSB?color=blueviolet)

# WhatsApp-Reader

WhatsApp Reader is a **web application** designed to read exported whatsapp conversations in a very similar experience to the original app.

## Online version
* Visit **[WhatsApp Chat Reader](https://whatsapp-chat-reader.herokuapp.com)** to see an online running version of the application which uses a database to load the conversations.
* Visit **[WhatsApp Reader](https://twibster123.pythonanywhere.com)** to see an online running version of the application which uses a temporary data structure to load the conversations

## Installation

Use the package manager **[pip](https://pip.pypa.io/en/stable/)** to install the required packages to run the application.

```bash
git clone https://github.com/twibster/WhatsApp-Reader.git
cd Whatsapp-Reader
pip install -r requirements.txt
```

## Setup
There is one environment variable needed for the application to work:

| Syntax | Description | Defualt | Importance |
| ----------- | ----------- | ---------- | ---------- |
| *DATABASE_URL* | Url configuration for the database | sqlite:///site.db | High |

## Usage
```bash
reset.py    # for the first time only
python run.py
```
Navigate to your browser and enter the address that appeared in your terminal.

[//]: <> ( ## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.)
