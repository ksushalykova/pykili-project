from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import collections
import time

TOKEN = '1131392983:AAEX-qE7vH1ikK_KW_fCjCzUEjK2UZtgN_M'

START_MESSAGE = 'Привет!\nЯ бот, помогающий найти съёмное жильё на авито. Так что выбирай, что хочешь снимать :)'

UNKNOWN_MESSAGE = 'Даже не знаю, что Вам ответить. Попробуйте /start'

ALLOWED_SPACES = ['квартира','студия']
ALLOWED_PERIODS = ['1', '2', '3']



def command_start(update, context):
    update.message.reply_text(
        START_MESSAGE,
        reply_markup=ReplyKeyboardMarkup.from_column(ALLOWED_SPACES))
    
def handle_space(update, context):
    global r_or_s
    r_or_s = update.message.text
    r_or_s.lower()
    message = 'Отлично! Сколько комнат? Если неважно, напиши "-".'
    update.message.reply_text(message)
    return "next0"

def info_1_page(page_num):

    html_doc = urlopen('https://www.avito.ru/moskva/kvartiry/sdam-ASgBAgICAUSSA8gQ?p={}'.format(page_num)).read()
    
    soup = BeautifulSoup(html_doc, features="lxml")

    for tag in soup.find_all('div'):
        
        item = "{0}: {1}".format(tag.name, tag.text)
        if "₽" in tag.text and "м²," in tag.text and len(tag.text) <= 160:
            
            for link in tag.find_all('a'):
                global href1
                href1 = link.get('href')
                
                global title1
                title1 = link.get('title')
                if title1 is not None:
                    title1 = title1.lower()
                
            for link in tag.findAll('span', {'data-marker':'item-price'}):
                price_ = str(link.contents)
                price0 = re.sub(r"[\\n]", "", price_)
                price00 = price0.replace( "['", "")
                global price1
                price1 = price00.replace( "']", "")
                price1 = price1.lower()
                
            for link in tag.findAll('span', {'class':'item-address__string'}):
                addr_ = str(link.contents)
                addr0 = re.sub(r"[\\n]", "", addr_)
                addr00 = addr0.replace( "['", "")
                global addr1
                addr1 = addr00.replace( "']", "")
                addr1 = addr1.lower()
                
            for link in tag.findAll('span', {'class':'item-address-georeferences-item__content'}):
                metro_ = str(link.contents)
                metro0 = metro_.replace( "['", "")
                global metro1
                metro1 = metro0.replace( "']", "")
                metro1 = metro1.lower()
                    
            for link in tag.findAll('span', {'class':'item-address-georeferences-item__after'}):
                metro_way_ = str(link.contents)
                metro_way11 = re.sub(r"[\\n]", "", metro_way_)
                metro_way0 = re.sub(r"[\xa0]", "", metro_way11)
                metro_way00 = metro_way0.replace( "['", "")
                metro_way000 = metro_way00.replace( "']", "")
                global metro_way1
                metro_way1 = metro_way000.replace( "xa0", " ")
                metro_way1 = metro_way1.lower()
                    
            for link in tag.findAll('div', {'flow':'down'}):
                time_ = str(link.contents)
                time0 = re.sub(r"[\\n]", "", time_)
                time00 = time0.replace( "['", "")
                global time1
                time1 = time00.replace( "']", "")
                time1 = time1.lower()

            content_1_elem = { href1: [ title1, price1, addr1, metro1, metro_way1, time1] }

            if href1 is not None and title1 is not None:
                dicty.update(content_1_elem)     
        
    return dicty


def room_number(update, context):
    global rm_nmbr
    rm_nmbr = update.message.text
    rm_nmbr.lower()
    message = 'Чудесно, а что насчёт площади? Напиши цифру в м² без пробелов. Для пропуска пиши "-".'
    update.message.reply_text(message)
    
    return "next1"

def square(update, context):
    global sqr
    sqr = update.message.text
    update.message.reply_text(
        'Выбери оплату: 1 - только за сутки, 2 - только за месяц, 3 - за месяц, но с учётом посуточных предложений',
        reply_markup=ReplyKeyboardMarkup.from_column(ALLOWED_PERIODS)
    )
        
    return "next2"

def daymonth(update, context):
    global dm
    dm = update.message.text
    message = 'А теперь укажи верхнюю границу цены в рублях без пробелов (просто циферку). Если в предыдущем вопросе ты выбрал 3, то сумму укажи в рублях в месяц.'
    update.message.reply_text(message)

    return "next3"

def price(update, context):
    global prc
    prc = update.message.text
    message = 'Если есть предпочтения по точному адресу, то напиши только название - улицы, или проспекта, или проезда, или переулка, или района, или посёлка в Московской области, или площади и т. д. Для пропуска этого пункта жми "-".'
    update.message.reply_text(message)

    return "next4"

def address(update, context):
    global ddrss
    ddrss = update.message.text
    message = 'Название ближайшего метро? Напиши "-" для пропуска этого пункта.'
    update.message.reply_text(message)

    return "next5"

def metro(update, context):
    global mtr
    mtr = update.message.text
    message = 'Максимальное расстояние до метро (в метрах без пробелов). "-" для пропуска'
    update.message.reply_text(message)

    return "next6"

def metro_way(update, context):
    global mtrw
    mtrw = update.message.text
    message = 'Класс, скоро будут результаты. Напиши "ок" для подтверждения)'
    update.message.reply_text(message)

    return "next7"

def good_hrefs(update, context):
    
    open('helper.txt', 'w', encoding = 'utf-8').write('Suitable:\n')
    
    u = update.message.text
    
    message = 'Квартиры для Вас:\n'
    update.message.reply_text(message)

    
    for hr, cont in dicty.items():
                  
        if r_or_s not in cont[0]:
            continue
        
        if r_or_s != 'студия' and rm_nmbr != '-' and '{}-к'.format(rm_nmbr) not in cont[0]:
            continue
        
        platz = re.findall(r'[0-9]* м²,', cont[0])
        platz = str(platz)
        platz0 = platz.replace(" м²,']", "")
        platz1 = platz0.replace("['", "")
        if sqr != '-' and abs(float(platz1) - float(sqr)) >= 10:
            continue

        pri = re.findall(r'[0-9]* [0-9]*  ₽', cont[1])
        pri = str(pri)
        pri0 = pri.replace(" ", "")
        pri1 = pri0.replace("₽", "")
        pri1 = pri1.replace("['", "")
        pri1 = pri1.replace("']", "")
        if dm == '1' and 'сутки' not in cont[1] or dm =='1' and float(pri1) > float(prc):
            continue
        if dm == '2' and 'месяц' not in cont[1] or dm =='2' and float(pri1) > float(prc):
            continue
        if dm == '3':
            if 'сутки' in cont[1]:
                pri1 = float(pri1)*30
            if float(pri1) > float(prc):
                continue

        if ddrss != '-' and ddrss not in cont[2]:
            continue

        if mtr != '-' and mtr not in cont[3]:
            continue

        cont[4] = cont[4].replace(" ", "")
        if 'км' in cont[4]:
            cont[4] = cont[4].replace("км", "")
            if ',' in cont[4]:
                cont[4] = cont[4].replace(",", "")
                cont[4] = int(cont[4])*100
                cont[4] = str(cont[4])
            else:
                cont[4] = int(cont[4])*1000
                cont[4] = str(cont[4])
        if 'км' not in cont[4]:
            cont[4] = cont[4].replace("м", "")
            cont[4] = cont[4].replace("['", "")
            cont[4] = cont[4].replace("']", "")
        if mtrw != '-' and float(mtrw) < float(cont[4]):
            continue
                    
        message = 'https://www.avito.ru'
        message  += hr
        message += '\n'
        
        open('helper.txt', 'a', encoding = 'utf-8').write('https://www.avito.ru')
        open('helper.txt', 'a', encoding = 'utf-8').write(hr)
        open('helper.txt', 'a', encoding = 'utf-8').write('\n')

        time.sleep(1)
        update.message.reply_text(message)

    if message == 'Квартиры для Вас:\n':
        message = 'К сожалению, подходящих вариантов не найдено ('
        
        update.message.reply_text(message)

    return "next8"
            

def handle_unknown1(update, context):
    update.message.reply_text(UNKNOWN_MESSAGE)
    dicty = {}

    return "next00"

def handle_unknown(update, context):
    update.message.reply_text(UNKNOWN_MESSAGE)
 


            
def main():

    global dicty
    dicty = {}

    
    for i in range(1, 90):
        info_1_page(i)

    time.sleep(3)
    for i in range(90, 101):
        info_1_page(i)
    print(dicty)

    
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', command_start))
   
    dp.add_handler(
        ConversationHandler(entry_points = [MessageHandler(Filters.text(ALLOWED_SPACES),handle_space)],
                            states = {
                                "next00": [MessageHandler(Filters.text(ALLOWED_SPACES),handle_space)],
                                "next0": [MessageHandler(Filters.text, room_number)],
                                "next1": [MessageHandler(Filters.text, square)],
                                "next2": [MessageHandler(Filters.text(ALLOWED_PERIODS), daymonth)],
                                "next3": [MessageHandler(Filters.text, price)],
                                "next4": [MessageHandler(Filters.text, address)],
                                "next5": [MessageHandler(Filters.text, metro)],
                                "next6": [MessageHandler(Filters.text, metro_way)],
                                "next7": [MessageHandler(Filters.text, good_hrefs)],
                                "next8": [MessageHandler(Filters.all, handle_unknown1)]
                            },
                            fallbacks = []
                            ))  

    dp.add_handler(MessageHandler(Filters.all, handle_unknown))

    updater.start_polling()
    updater.idle()


   
if __name__ == '__main__':
    main()
