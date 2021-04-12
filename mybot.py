#kutubxonani import(chaqirib olish) qilish
import telebot
from pprint import pprint
import nltk
from random import choice
import json

# tokenni ruyxatdan utkazish
bot = telebot.TeleBot("1748606537:AAHwPzN-WCc7R0tn_0LpIiU00XnlSMlwfCU", parse_mode=None)
BOT_CONFIG = {}
find = ''
gintents = ''
gexamples = ''
ganswers = ''

# file load from json

def file_open(arg):
    if (arg == 'uz'):
        with open('uz.json','r') as f:
            global BOT_CONFIG
            BOT_CONFIG = json.load(f)
            print(BOT_CONFIG['intents'])
            print(BOT_CONFIG.keys())
    else:
        with open('ru.json','r') as f:
            BOT_CONFIG = json.load(f)
            print(BOT_CONFIG)

# function for file upload and create

def file_save(arg):
    if (arg == 'uz'):
        with open('uz.json','w') as f:
            json.dump(BOT_CONFIG,f)
    else:
        with open('ru.json','w') as f:
            json.dump(BOT_CONFIG,f)


def filter(text):  #filter funksiyasi
    text = text.lower()
    text = [c for c in text if c in 'abdefghijklmnopqrstuvxz -']
    text = "".join(text) # alfabit harflaridan boshqa simvollarni uchiradi
    return text

def get_answer_by_intent(intent): # javob izlash funksiyasi
    global BOT_CONFIG
    answer = BOT_CONFIG["intents"][intent]["answers"]
    return choice(answer)

def add_answers(message):
    chat_id = message.chat.id
    answers = (message.text).split(',')
    global BOT_CONFIG
    global gexamples
    global ganswers
    ganswers = answers
    BOT_CONFIG["intents"][gintents]= '{ "examples" : ['+",".join(gexamples)+' ], "answers : [ '+",".join(answers)+' ]"}' 
    file_save('uz')
    text = 'Yangi intent muvofaqiyatli kiritildi sizni tabrikliyman!'
    bot.send_message(message.chat.id,text)

def add_examples(message):
    chat_id = message.chat.id
    examples = (message.text).split(',')
    global BOT_CONFIG
    global gexamples
    gexamples = examples
    BOT_CONFIG["intents"][gintents]= '{ "examples" : ['+",".join(gexamples)+' ], "answers : [ ]"}' 
    msg = bot.reply_to(message, 'Endi Javob variantlarini kiriting! masalan : salom assalom hello hi ')
    bot.register_next_step_handler(msg, add_answers)

    
def add_intents(message):
    chat_id = message.chat.id
    intent = message.text
    global BOT_CONFIG
    global gintents
    BOT_CONFIG["intents"][intent]= '{ "examples" : [] , "answers : [ ]"}'
    gintents = intent
    msg = bot.reply_to(message, 'Endi intentni barcha ehtimolini kiriting!')
    bot.register_next_step_handler(msg, add_examples)
    

# biz hozir start comandasi va help comandasini qaytaishlaymiz


@bot.message_handler(commands=['start','help','intents'])
def handle_start_help(message):
    file_open('uz')
    if(message.text == '/start'):
        bot.reply_to(message, "Suhbatlashamizmi???")    
    elif(message.text == '/help'):
        print("helpni bosdi")
        bot.reply_to(message, "qonday yordam kerak ")
    elif(message.text == '/intents'):
        text = "Yangi maqsadni nomini kiriting!"
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, add_intents)
    
@bot.message_handler(content_types=['document'])

def handle_text_doc(message):
    file_open('uz')
    bot.reply_to(message, "Men telegram bot man va fayllar bilan ishlay olmayman!?")    
# ikkinchi dars python da textlar va spiskalar bilan ishlash
# 
@bot.message_handler(content_types=['text'])

def get_intent(message):
    text = message.text
    text = filter(text)
    global BOT_CONFIG
    global find
    for intent, value in BOT_CONFIG["intents"].items():
        for example in value["examples"]:
            example = filter(example)
            if (len(example) != 0):
                distance = nltk.edit_distance(text,example)/len(example)           
            if (example == text or distance <= 0.2):
                print(f" Sizni suxbatdoshiz  {intent} {distance}")
                bot.reply_to(message,  get_answer_by_intent(intent))          
                find = 'topdi'
            
    
    if(find != 'topdi'):
        failer = choice(BOT_CONFIG["failer_phrases"])
        bot.reply_to(message,  failer)
        find = 'topdi'
    
                
                
                

bot.polling()
