#kutubxonani import(chaqirib olish) qilish
import telebot


# tokenni ruyxatdan utkazish
bot = telebot.TeleBot("1748606537:AAHM8vltcvQMrtub7p_GoafJ_vEk8ZZczM0", parse_mode=None)


# biz hozir start comandasi va help comandasini qaytaishlaymiz

@bot.message_handler(commands=['start', 'help','elbek','salom'])

def handle_start_help(message):
    if(message.text == '/start'):
        print("siz start knopkasini bosdiz!")
        bot.reply_to(message, "Siz start knopkasini bosdiz!?")
    elif(message.text == '/help'):
        print("siz help knopkasini bosdiz!")
        bot.reply_to(message, "Iltimos bezovta qilmang!?")
    elif(message.text == '/elbek'):
        print("siz elbek knopkasini bosdiz!")
        bot.reply_to(message, "Siz elbekka murojat qilmoqchimisiz!?")
    else:
        if(message.text == '/salom'):
            bot.reply_to(message, "Salom ishlar yaxshimi man telegram bot man!?")
        else:
            bot.reply_to(message, "Siz mani aqlim yetmaydigan suz yozdiz iltimos boshqa suz yozing!?")
   
@bot.message_handler(content_types=['document'])

def handle_text_doc(message):
    bot.reply_to(message, "Men telegram bot man va fayllar bilan ishlay olmayman!?")    

bot.polling()
