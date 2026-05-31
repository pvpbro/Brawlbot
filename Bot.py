import requests
import telebot
import ssl

# Отключаем предупреждения SSL
requests.packages.urllib3.disable_warnings()

TELEGRAM_TOKEN = "8805792061:AAHbfrOhBKCtrj_1N6avksmylmDSQ2uhDFI"
BRAWL_STARS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijg2MzY3MDNjLWQyMTEtNDVhNS05ZjUyLTk1NGVjM2VlM2QzOSIsImlhdCI6MTc4MDIzNDI1NSwic3ViIjoiZGV2ZWxvcGVyLzExODlkMWUzLTA0MGEtYjVlMy1kN2ZmLTQzMTg1MGYxMTJmNSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiOTEuNzkuMjI1LjExNyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.JqbYH9Qin4Fcbc1u31Vg63Tsqd21wEdPoDGlPXUw4CRSuL5GQyGAyroHxgMgGX-6c7XI_hIgV4_HNe8iqcHqZg"

# Создаём бота без дополнительных настроек
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_player_info(tag):
    tag = tag.strip().upper()
    if not tag.startswith("#"):
        tag = "#" + tag
    
    encoded_tag = tag.replace("#", "%23")
    url = f"https://api.brawlstars.com/v1/players/{encoded_tag}"
    headers = {"Authorization": f"Bearer {BRAWL_STARS_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            
            message = f"""
🎮 Brawl Stars - Профиль игрока
━━━━━━━━━━━━━━━━━━━━━━━━

👤 Имя: {data.get('name', '?')}
🏷️ Тег: {tag}
🏆 Кубки: {data.get('trophies', 0)}
⭐ Уровень: {data.get('expLevel', 0)}
🎯 Максимум кубков: {data.get('highestTrophies', 0)}
👥 Бойцов: {data.get('brawlersCount', 0)}
"""
            
            if data.get('club'):
                message += f"━━━━━━━━━━━━━━━━━━━━━━━━\n🏰 Клуб: {data['club'].get('name', '?')}\n"
            
            return message
        elif response.status_code == 404:
            return f"❌ Игрок с тегом {tag} не найден"
        elif response.status_code == 403:
            return "❌ Ошибка доступа к API. Твой IP не в белом списке."
        else:
            return f"❌ Ошибка API: {response.status_code}"
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎮 Привет! Отправь мне тег игрока Brawl Stars.\n\nПример: #2PPQVUQ8J")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "🔍 Ищу информацию...")
    result = get_player_info(message.text)
    bot.reply_to(message, result)

print("🤖 Бот запущен!")
bot.infinity_polling()
