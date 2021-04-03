import requests
import smtplib
import datetime as dt
from dotenv import load_dotenv
import os
import random
import smtplib
from email.message import EmailMessage
import imghdr
from pymongo import MongoClient

load_dotenv()

companies = ["Amazon", "Apple", "Uber Eats", "Starbucks", "Steam"]
giftcards = {
    "Amazon": "https://www.pcgamesupply.com/media/assets/images/MobileGroupImages/Amazon.png",
    "Apple": """\
        https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/giftcard-unselect-2020-family?wid=4000&hei=3836&fmt=jpeg&qlt=80&.v=1613588703000
    """,
    "Uber Eats": "https://www.uber-assets.com/image/upload/f_auto,q_auto:eco,c_fill,w_1116,h_744/v1588111355/assets/90/b81c92-4af3-4102-8151-dcce9bbb28af/original/Tasty-food-gifts-delivered-anytime-DESKTOP-TABLET-MOBILE-3x2.jpg",
    "Starbucks": "https://globalassets.starbucks.com/assets/086b81f31abb4615bd71d5689f6823a2.png",
    "Steam": "https://store.cloudflare.steamstatic.com/public/images/gift/steamcards_cards_02.png"
}

DATE = dt.datetime.now().strftime('%m-%d')
#print(DATE)
client = MongoClient(os.getenv('MONGO_CONFIG_URL'))
people = client.get_database('ppldb')
available_gift_cards = client.get_database('giftcarddb').cards
friends = list(people.friends.find())
#subscribers = list(people.subscribers.find())
#print(friends)
my_email = os.getenv("MY_EMAIL")
my_password = os.getenv("MY_EMAIL_PASSWORD")

with smtplib.SMTP("outlook.office365.com") as connection:
    connection.starttls()
    connection.login(my_email, my_password)
    for friend in friends:
        if (friend['bday'] != DATE):
            continue
        message = EmailMessage()
        message['From'] = os.getenv("MY_EMAIL")
        message['To'] = friend['email']
        f_name = friend['name'].split(' ')[0]
        message['Subject'] = f"Good day, {f_name}!"
        letter_path = f"./letters/lt{random.randint(1,5)}.txt"
        with open(letter_path) as letter:
            letter_content = letter.read()
            letter_content = letter_content.replace("[NAME]", f_name)
        ending_path = f"./ending/e{random.randint(1,5)}.txt"
        with open(ending_path) as ending:
            ending_content = ending.read()
        company = companies[random.randint(0,4)]
        url = giftcards[company]
        gift_card_query = { "name": company }
        code = available_gift_cards.find_one(gift_card_query)['code']
        gift_card_note = f"""\
        <p>Here's a gift card from {company}, which I hope you will enjoy! Its Redeem Code is {code}.</p>
        <img src={url} style="height:30%;width:30%;"alt="Gift Card">
        <br/>
        """
        if (friend['tag'] != 'f'):
            draw_num = random.randint(1, 2)
            if (draw_num != 2):
                gift_card_note = ' '
        message.set_content(f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1 style="background-image: linear-gradient(to left, violet, indigo, blue, green, yellow, orange, red); -webkit-background-clip: text;   color: transparent;">Happy Birthday!</h1>
                <p>{letter_content}</p>
                {gift_card_note}
                <div>Additionally, please, should you be interested, visit <a href="http://172.105.18.194/public/tianhaos_station">my station on Azuracast<a/>, where you can hear the livestreaming of a favourite song of mine!</div> <br/>
                <span>{ending_content}</span>
                <br/>
                <span>Tianhao</span>
            </body>
        </html>
        """, subtype = "html")
        connection.send_message(message)
