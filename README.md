## install python
## install git
## install node.js

## install virtualenv
pip3 install virtualenv --user

## build env
python3 -m venv env

## start env 
source env/bin/activate

## Install dependencies
Run:
```bash
pip install -r requirements.txt
```

To install development dependencies:

```bash
pip install -r requirements-dev.txt
python -m spacy download en_core_web_md en
python -m spacy link en_core_web_md en
```

## Run the bot

rasa train

## new directory

git clone https://github.com/RasaHQ/chatroom
npm i yarn -g
yarn install
yarn build
yarn serve

In one terminal window:
```bash
rasa run --enable-api --cors "*" --port 5005 --debug
```
In another terminal window:
```bash
rasa run actions --port 5055 --debug
```
