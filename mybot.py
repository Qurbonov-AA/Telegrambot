#kutubxonani import(chaqirib olish) qilish
import telebot
from pprint import pprint
import nltk
from random import choice
import json

# tokenni ruyxatdan utkazish
bot = telebot.TeleBot("1791602674:AAE5fFNB9-ees55kiCZdtWZxRab3NSrEFH0", parse_mode=None)

find = ''
gintents = ''
gexamples = ''
ganswers = ''
# file load from json

def file_open(arg):
    if (arg == 'uz'):
        with open('uz.json','r') as f:
            BOT_CONFIG = json.load(f)
            print(f)
    else:
        with open('ru.json','r') as f:
            BOT_CONFIG = json.load(f)
            print(f)

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
    answer = BOT_CONFIG["intents"][intent]["answers"]
    return choice(answer)

def add_answers(message):
    chat_id = message.chat.id
    answers = (message.text).split()
    global BOT_CONFIG
    global gexamples
    global ganswers
    ganswers = answers
    BOT_CONFIG["intents"][gintents]= '{ "examples" : ['+",".join(gexamples)+' ], "answers : [ '+",".join(answers)+' ]"}' 
    pprint(BOT_CONFIG)
    text = 'Yangi intent muvofaqiyatli kiritildi sizni tabrikliyman!'
    bot.send_message(message.chat.id,text)

def add_examples(message):
    chat_id = message.chat.id
    examples = (message.text).split()
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


BOT_CONFIG ={
        "intents" :
           {
               "hello_men" : {
                       "examples" : ["Salom","sava","qonday","buloptimi","tinchmi","mazang qalay","qanneysan","qanaqasan","🙋‍♂️"] ,
                       "answers"  : ["Salomaleykum","Va aleykum as-salom","qandaysan","qalaysan"],},
               "hello_women":{
                       "examples" : ["Assalom","qalisan","qalisiz","🙋‍♀️","Assalomu aleykum"],
                       "answer"  : ["Xayrli kun","🙋‍♀️","ishlariz joyidami"],  },
               "bye_men"   : {
                        "examples" : ["bye","bupti","kurishamiz","gaplashamiz"],
                        "answers"  : ["kurishguncha","xayr","kechroq gaplashamiz"],
                   },
               "bye_women"   : {
                        "examples" : ["paka","xayr","sog buling","xayrcha"],
                        "answers"  : ["gaplashguncha 🙋‍♀️","xayrcha 😘","yana yozishamiz deb uyliymay 🌹 "], },
               "qitmirlik"  :{
                        "examples" :["raqamingdi ber","budilnika quyaman"],
                        "answers" : ["nima qilasan", "sur","damini ol","toshingni ter","nomerim yuq"],
                    },
               "maqasad"    :{
                        "examples" :["tanishaylik","hikoya ayt","yordam kerak","yordam ber","rasmchiz","yoz","qushiq ayt"],
                        "answers"  :["yoq","xop","uzur bajarolmayman","gap bulishi mumkinmas","xop demasam uyat bular;)"],
                   },
           },
        "failer_phrases" : ["tushunarli qilib yozing inson ","man bot man xolos tushunarli yozing","nima demoqchiligingizni tushunmadim","balkim uziz javob berarsiz"], }

@bot.message_handler(commands=['start','help','intents'])
def handle_start_help(message):
    if(message.text == '/start'):
        file_save('uz')   
    elif(message.text == '/help'):
        print("helpni bosdi")
        bot.reply_to(message, "qonday yordam kerak ")
    elif(message.text == '/intents'):
        text = "Yangi maqsadni nomini kiriting!"
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, add_intents)
    
@bot.message_handler(content_types=['document'])

def handle_text_doc(message):
    bot.reply_to(message, "Men telegram bot man va fayllar bilan ishlay olmayman!?")    
# ikkinchi dars python da textlar va spiskalar bilan ishlash
# 
@bot.message_handler(content_types=['text'])

def get_intent(message):
    text = message.text
    text = filter(text)
    global find
    for intent, data in BOT_CONFIG["intents"].items():
        for example in data["examples"]:
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
