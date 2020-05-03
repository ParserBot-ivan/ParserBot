import telebot
from telebot import apihelper
from telebot import types
from bs4 import BeautifulSoup
import requests as req
import time

#PROXY = 'socks5://userproxy:password@148.251.234.93:1080' 
TOKEN = "1212450339:AAHeyDwrUnEuwQ1dmugnhs8tKv1POuOIxIY"
BTC_DOLLAR = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD%D0%B0+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&oq=rehc+%2Cbnrjbyf+d+&aqs=chrome.1.69i57j0l7.2672j1j7&sourceid=chrome&ie=UTF-8"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"}
bot = telebot.TeleBot(TOKEN)
#apihelper.proxy = {'https': PROXY}

DIFF  = 1 # разница в долларах
Money = 0.0

def chech_currency(Money):
	full_page = req.get(BTC_DOLLAR, headers=headers)

	soup = BeautifulSoup(full_page.content, "html.parser")

	convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", })
	for element in convert:
   		btc = float(element['data-value'])
	if Money == 0.0:
		Money = btc
		print(Money)
	if Money + DIFF <= btc:
		print("Курс вырос на ", round(btc - Money, 2), '$')
		print("Сейчас его цена: ", btc)
		message_str = "Курс вырос на " + str(round(btc - Money, 2)) + '$\n' + "Сейчас его цена: " + str(btc) + '$'
		bot.send_message(764490361, message_str)
		Money = btc
	if Money - DIFF >= btc:
		print("Курс упал на ", Money - btc, '$')
		print("Сейчас его цена: ", btc)
		message_str = "Курс упал на " + str(round(Money - btc,2)) + '$\n' + "Сейчас его цена: " + str(btc) + '$'
		bot.send_message(764490361, message_str)
		Money = btc
	print('-')

	time.sleep(10)
	chech_currency(Money)

@bot.message_handler(commands = ["start"])
def start(message):
	bot.send_message(764490361, "Запустился")
	print(message.chat.id)
	chech_currency(Money)


@bot.message_handler(func=lambda message: True)
def send_all(message):
	pass

bot.polling(none_stop=True)