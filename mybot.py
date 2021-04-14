#kutubxonani import(chaqirib olish) qilish
import telebot
from pprint import pprint
import nltk
from random import choice
import json

# tokenni ruyxatdan utkazish
bot = telebot.TeleBot("1242724893:AAFDauEH7EOOAQLEojulFOtH0hW6NkRomGM", parse_mode=None)
find = ''
gintents = ''
gexamples = ''
ganswers = ''


# file load from json

def file_open(arg):
    global BOT_CONFIG
    if (arg == 'uz'):
        with open('uz.json','r') as f:
            
            BOT_CONFIG = json.load(f)
    else:
        with open('ru.json','r') as f:
            BOT_CONFIG = json.load(f)


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
    answer_line = message.text
    answers = (answer_line).split(',')
    global BOT_CONFIG
    global gexamples
    global ganswers
    global gintents   
    ganswers = answers
    BOT_CONFIG["intents"][gintents] = { "examples" : [] , "answers" : [] }
    for item in gexamples:
        BOT_CONFIG["intents"][gintents]["examples"].append(item)
    for item in ganswers:
        BOT_CONFIG["intents"][gintents]["answers"].append(item)
    
    file_save('uz')
    text = 'Yangi intent muvofaqiyatli kiritildi sizni tabrikliyman!'
    bot.send_message(message.chat.id,text)

def add_examples(message):
    chat_id = message.chat.id
    examples_line = message.text
    examples = (examples_line).split(',')
    global gexamples
    gexamples = examples
    msg = bot.reply_to(message, 'Endi Javob variantlarini kiriting! masalan : salom assalom hello hi ')
    bot.register_next_step_handler(msg, add_answers)

    
def add_intents(message):
    chat_id = message.chat.id
    intent = str(message.text)
    global gintents
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
    file_open('uz')
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
