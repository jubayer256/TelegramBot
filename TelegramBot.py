import telebot
import requests
def scrape(tab_name):
    url = "https://api.arogga.com/general/v3/search/?_page=1&_perPage=5&_search=" + tab_name
    response = requests.get(url).json()
    medicines = response["data"]
    lst = []
    for data1 in medicines:
        pv = data1["pv"][0]
        name = data1["p_name"].strip()
        amount = data1["p_strength"].strip()
        medicine_type = data1["p_form"].strip()
        generic_name = data1["p_generic_name"].strip()
        brand = data1["p_manufacturer"].strip()
        description = data1["p_meta_description"].strip()
        strip = pv["pu_b2c_sales_unit_label"].strip()
        total = pv["pu_b2c_base_unit_multiplier"]
        discount_price = pv["pv_b2c_price"]
        price = pv["pv_b2c_mrp"]
        try:
            image = data1["attachedFiles_p_images"][0]["src"].strip()
        except:
            image = ""
        result = "{} {} {}\n{}\n{}{}\n{}\nTotal : {}\nPrice : {}\nDiscounted Price : {}\n{}".format(name, amount, medicine_type, generic_name, brand, description, strip, str(total), str(price), str(discount_price), image)
        lst.append(result)
    return lst

API_TOKEN = "8062425004:AAGk27lBvzFFEEWYmN2lb7blnlPyvH7r50g"
bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=["start", "Help", "get", "Cancel"])
def welcome(message):
    bot.reply_to(message, "Welcome to our Medicine helping bot. This bot will help you to find out the all kind of medicine. to know about this type /info for details")

@bot.message_handler(commands=["info"])
def welcome2(message):
    bot.reply_to(message, "Type any name of medicine to get the details of those medicine. If there is any problem type /help & contact with us")

@bot.message_handler(commands=["help"])
def welcome3(message):
    bot.reply_to(message, "Not available yet")

@bot.message_handler(content_types="text")
def search_tablet(message):
    medicine_name = message.text

    results = scrape(medicine_name)
    for r in results:
        bot.reply_to(message, r)

bot.polling()
