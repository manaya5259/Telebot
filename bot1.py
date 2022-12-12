import os
from time import sleep
import telebot
from telebot import types
from flask import Flask, request

options = {'Statistics': 'Statistics by today', 'Ways': 'Ways by today', 'Positions': 'Positions by today',
           'URL': 'Open site', 'Languages': 'Languages comparison'}

TOKEN = ('5905681814:AAG7pIHZs_afblZHPudSgsbqtes8fBQXrEc')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

############################################
@bot.message_handler(commands=["start"])
def start_command(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton(text="商品を見る🔍")
    button2 = types.KeyboardButton(text="注文する🛒")
    button3 = types.KeyboardButton(text="期間限定クーポン🎟")
    button4 = types.KeyboardButton(text="保証について")

    keyboard.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, "⬇︎  ⬇︎  ボタンをタップしてください  ⬇︎  ⬇︎", reply_markup=keyboard)
#################メニュー送信################
@bot.message_handler(func=lambda message: message.text == "商品を見る🔍") #"メニューを見る"押下で画像送信(start_command(message)と連携)
def send_menu(message):
    manu_photo = 'https://telegra.ph/file/71577b6a852e6d0059d2d.jpg'
    markup = types.InlineKeyboardMarkup(row_width=2)
    bot.send_photo(message.chat.id, photo=manu_photo,  reply_markup=markup)

##################保証##################
@bot.message_handler(func=lambda message: message.text == "保証について")
def show_sns(message):
    bot.send_message(message.chat.id, parse_mode='HTML', 
                     text="2日間ログイン保証あり\n\n交換も承ります")
##################注文#####################
@bot.message_handler(func=lambda message: message.text == "注文する🛒")
def order(message):
    #keyboard = types.InlineKeyboardMarkup()
    #url_btn = types.InlineKeyboardButton(url="https://t.me/nature_love420", text="販売係の連絡先(タップしてね)")
    #keyboard.add(url_btn)
    bot.send_message(message.chat.id, parse_mode='HTML', 
                     text="下記情報を送ってください。\n\n<b>❶...個数</b>\n\n<b>❷...タイプ</b>\n\nその他ご質問等ございましたらお気軽にお申し付けください。")
##################クーポン##################
@bot.message_handler(func=lambda message: message.text == "期間限定クーポン🎟")
def show_coupon(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("初回割引📣", callback_data="review")
    markup.add(item1)
    bot.send_message(message.chat.id, "🎟 現在使用可能なクーポン 🎟", reply_markup=markup)
############################################
##################コールバック################
#クーポン
@bot.callback_query_handler(func=lambda call:True)
def callback_coupon_inline(call):
    if call.data == "review":
        bot.send_message(call.message.chat.id, "【10%割引き】\n\n購入時に「初回割」とお伝えください。")
###########################################

#Local
bot.remove_webhook()

#Heroku
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return '!', 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://telebot0525.herokuapp.com/" + TOKEN)
    return "!", 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
while True:
    try:
        bot.infinity_polling(True)
        bot.polling(none_stop=True)
    except:
        sleep(10)

