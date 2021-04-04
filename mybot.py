#kutubxonani import(chaqirib olish) qilish
import telebot
import nltk
from random import choice

# tokenni ruyxatdan utkazish
bot = telebot.TeleBot("1791602674:AAE5fFNB9-ees55kiCZdtWZxRab3NSrEFH0", parse_mode=None)



BOT_CONFIG ={
        "intents" :
           {
               "hello" : {
                       "examples" : ["Salom","sava","Assalom","qanday","buloptimi"],
                       "answers"  : ["Salom","Xayrli kun","Va aleykum as-salom","qandaysan","ishing nima mazgi","nima qilasan"], 
                   },
               "bye"   : {
                        "examples" : ["by","bupti","paka","xayr","kurishamiz","gaplashamiz"],
                        "answers"  : ["kurishguncha","xayr","yana yozishamiz deb uylanmay","kechroq gaplashamiz"],
                   },
               "qitmirlik"  :{
                        "examples" :["raqamingdi ber","budilnika quyaman"],
                        "answers" : ["nima qilasan", "sur","damini ol","toshingni ter","nomerim yuq"],
                    },
               "maqasad"    :{
                        "examples" :["tanishaylik","hikoya ayt","yordam kerak","yordam ber","rasmchiz","yoz","qushiq ayt"],
                        "answers"  :["yoq","xop","uzur bajarolmayman","gap bulishi mumkinmas","xop demasam uyat bular;)"],
                   },
           },
        "failer_phrases" : ["tushunarli qilib yozing inson ","man bot man xolos tushunarli yozing","nima demoqchiligingizni tushunmadim","balkim uziz javob berarsiz"]
    }

def filter(text):  #filter funksiyasi
    text = text.lower()
    text = [c for c in text if c in 'abdefghijklmnopqrstuvxz -']
    text = "".join(text) # alfabit harflaridan boshqa simvollarni uchiradi
    return text

def get_answer_by_intent(intent): # javob izlash funksiyasi
    answer = BOT_CONFIG["intents"][intent]["answers"]
    return choice(answer)
    
# biz hozir start comandasi va help comandasini qaytaishlaymiz

@bot.message_handler(commands=['start','help'])

def handle_start_help(message):
    if(message.text == '/start'):
        print("foydalanuvchi starni bosdi")
        bot.reply_to(message, "qonday ishlar ")
   
    if(message.text == '/help'):
        print("helpni bosdi")
        bot.reply_to(message, "qonday yordam kerak ")
    
@bot.message_handler(content_types=['document'])

def handle_text_doc(message):
    bot.reply_to(message, "Men telegram bot man va fayllar bilan ishlay olmayman!?")    
# ikkinchi dars python da textlar va spiskalar bilan ishlash
# 
@bot.message_handler(content_types=['text'])

def get_intent(message):
    text = message.text
    text = filter(text)
    
    for intent, data in BOT_CONFIG["intents"].items():
        for example in data["examples"]:
            example = filter(example)
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
