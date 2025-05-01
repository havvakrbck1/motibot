import telebot
import random
import json
import os

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'itiraflar.json'
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# Bot'un çalışma döngüsü için polling bir kez çağrılır
try:
    bot.polling(none_stop=True, interval=5)  # interval parametresi ile bekleme süresi
except KeyboardInterrupt:
    print("Botu manuel olarak durdurdunuz.")
except Exception as e:
    print(f"Bir hata oluştu: {e}")

# Şans mesajları
sans_mesajlari = [
    "🍀 Bugün şans seninle! Yeni fırsatlara açık ol!",
    "🌟 Harika bir haber alabilirsin bugün!",
    "🚀 Risk almaktan korkma, ödül büyük olacak!",
    "💖 Birileri seni düşünüyor... 😉",
    "🔥 Enerjin çevrendekilere ilham verecek!"
]

# Günlük görevler
gunluk_gorevler = [
    "🎯 Bugün 3 kişiye güzel bir iltifat et!",
    "📚 10 dakika bir şeyler oku!",
    "🚶‍♀️ 20 dakika yürüyüş yap!",
    "🌱 Küçük bir iyilik yap, gizlice!",
    "✍️ 5 olumlu düşünceni yaz bir kağıda!"
]

# Quiz soruları
quiz_sorulari = [
    {"soru": "🌍 Dünya'nın en büyük okyanusu hangisidir?", "cevap": "Pasifik"},
    {"soru": "⚡ Elektronu keşfeden bilim insanı kimdir?", "cevap": "Thomson"},
    {"soru": "🎶 Beatles grubunun en ünlü şarkılarından biri?", "cevap": "Hey Jude"}
]

# Hediyeler
hediyeler = [
    "🎁 Bugün için küçük bir kahve molası hak ettin!",
    "🎁 Kendine tatlı bir ödül ver!",
    "🎁 Bu akşam sadece kendin için zaman ayır!",
    "🎁 Bir arkadaşına beklemediği bir mesaj gönder!",
    "🎁 Mini tatil planı yap, hak ettin!"
]

# Kullanıcıyı karşılayan komut
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 
        "🎉 Hoş geldin! Kullanabileceğin komutlar:\n\n"
        "/sans 🍀 Şans Mesajı\n"
        "/gorev 📌 Günlük Görev\n"
        "/quiz 🧠 Mini Quiz\n"
        "/itiraf 🤫 Anonim İtiraf\n"
        "/hediye 🎁 Sürpriz Hediye\n")

# Şans mesajı
@bot.message_handler(commands=['sans'])
def sans_mesaji(message):
    bot.send_message(message.chat.id, random.choice(sans_mesajlari))

# Günlük görev
@bot.message_handler(commands=['gorev'])
def gorev_mesaji(message):
    bot.send_message(message.chat.id, random.choice(gunluk_gorevler))

# Quiz başlatma
@bot.message_handler(commands=['quiz'])
def quiz_basla(message):
    soru = random.choice(quiz_sorulari)
    bot.send_message(message.chat.id, soru["soru"])
    bot.register_next_step_handler(message, lambda m: quiz_cevapla(m, soru["cevap"]))

def quiz_cevapla(message, dogru_cevap):
    if message.text.strip().lower() == dogru_cevap.lower():
        bot.send_message(message.chat.id, "✅ Doğru cevap! Aferin! 🎉")
    else:
        bot.send_message(message.chat.id, f"❌ Yanlış! Doğru cevap: {dogru_cevap}")

# İtiraf alma ve kaydetme
@bot.message_handler(commands=['itiraf'])
def itiraf_al(message):
    bot.send_message(message.chat.id, "🤭 Paylaşmak istediğin itirafı yaz:")
    bot.register_next_step_handler(message, itiraf_kaydet)

def itiraf_kaydet(message):
    itiraf = message.text
    with open(DATA_FILE, 'r') as f:
        itiraflar = json.load(f)
    itiraflar.append(itiraf)
    with open(DATA_FILE, 'w') as f:
        json.dump(itiraflar, f)
    bot.send_message(message.chat.id, "✅ İtiraf kaydedildi! Başka zaman rasgele okunacak! 🎭")

# Hediye mesajı
@bot.message_handler(commands=['hediye'])
def hediye_mesaji(message):
    bot.send_message(message.chat.id, random.choice(hediyeler))
