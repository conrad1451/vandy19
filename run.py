import requests
import sys
from PIL import Image
from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC4cebdb3f91c465dd8de9ebebe399148c'
auth_token = '6a42c296e68579a60d925ac8c39e61d3'
client = Client(account_sid, auth_token)

printMenu = 0
giveChoice = 0
menuChoice = -1
app = Flask(__name__)


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    global menuChoice
    global printMenu
    global giveChoice
    if giveChoice == 0:
        number = request.form['From']
        menuChoice = request.form['Body']

    if printMenu == 0:
        resp = MessagingResponse()
        resp.message = (client.messages.create(
            body=" \n"
                 "Welcome to Meme Hotline!\n"
                 "Text \"1\" for Gif search\n"
                 "Text \"2\" for //NEW MODE//\n"
                 "Text \"0\" to Quit",
            from_='+14243214684',
            to='+14848853093'))
        printMenu = 1
    else:
        if menuChoice == "1":
            if giveChoice == 1:

                try:
                    number2 = request.form['From']
                    message_body = request.form['Body']

                    if message_body != "0":
                        payload = {'api_key': 'seXC2fGDNpVjAnTtg4qLhZiBvKqLTLzp', 'q': message_body, 'limit': 1}
                        r = requests.get('http://api.giphy.com/v1/gifs/search', params=payload)
                        print(r.url)

                        def gotData(stuff):
                            print(stuff.json())

                        resp = MessagingResponse()
                        resp.message = (client.messages.create(
                            body="\n"
                                 "Press 0 to quit to menu",
                            from_='+14243214684',
                            media_url=(r.json()['data'][0]['images']['downsized']['url']),
                            to='+14848853093'))
                    else:
                        resp = MessagingResponse()
                        resp.message = (client.messages.create(
                            body=" \n"
                                 "Returning to menu\n"
                                 "Type anything to start",
                            from_='+14243214684',
                            to='+14848853093'))
                        printMenu = 0
                        giveChoice = 0
                except IndexError:
                    resp = MessagingResponse()
                    resp.message = (client.messages.create(
                        body="\n"
                             "I can't find any gifs\n"
                             "with that keyword,\n"
                             "Try Again!",
                        from_='+14243214684',
                        to='+14848853093'))
            else:
                resp = MessagingResponse()
                resp.message = (client.messages.create(
                    body=" \n"
                         "Welcome to Gif Search!\n"
                         "Type some keywords and\n"
                         "see what you get!",
                    from_='+14243214684',
                    to='+14848853093'))
                giveChoice = 1
        elif menuChoice == "2":
            if giveChoice == 1:

                resp = MessagingResponse()
                try:
                    if request.values['NumMedia'] != '0':

                        # Use the message SID as a filename.
                        filename = request.values['MessageSid'] + '.png'
                        with open('./Uploads/{}'.format(filename), 'wb') as f:
                            image_url = request.values['MediaUrl0']
                            f.write(requests.get(image_url).content)
                            input = PIL.Image.open('./Uploads/{}'.format(filename))

                            #enter cool stuff here having to do with the image inside the Uploads folder
                            #Then output the product back to the user
                        resp.message("very funny, thanks")
                    else:
                        resp.message("Try sending a picture message.")
                except Exception:
                    resp.message("Try sending a picture message.")
            else:
                resp = MessagingResponse()
                resp.message = (client.messages.create(
                    body="\n"
                         "Welcome to Meme picture\n"
                         "Enter sumn funny",
                    from_='+14243214684',
                    to='+14848853093'))
                giveChoice = 1
        elif menuChoice == "0":
            resp = MessagingResponse()
            resp.message = (client.messages.create(
                body="\n"
                     "Meme sesh quit\n"
                     "Type anything to restart",
                from_='+14243214684',
                to='+14848853093'))
            printMenu = 0
        else:
            resp = MessagingResponse()
            resp.message = (client.messages.create(
                body="\n"
                     "That was not an option\n"
                     "Type anything to restart",
                from_='+14243214684',
                to='+14848853093'))
            printMenu = 0
    return str(resp)


if __name__ == "__main__":
    app.run()
