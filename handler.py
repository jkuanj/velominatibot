import json
import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def manualLoad(headersfilename='headers.txt'):
    unorderedlist = []
    with open(headersfilename, "r") as f:
        unorderedlist = f.read().splitlines()
    datadict = {}
    for i in range(len(unorderedlist)):
        datadict[i+1] = unorderedlist[i]
    return datadict

def hello(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"]).strip('/')
        chat_id = data["message"]["chat"]["id"]

        response = f"Enter rule number:"

        try:
            num = int(message)
            datadict = manualLoad()
            if num in datadict:
                response = f"RULE #{num} // {datadict[num]}"
            else:
                response = "No such rule number."
        except ValueError as ve:
            print(ve)

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = f"{BASE_URL}/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}