import telebot
from environs import Env
from root_package.settings import settings
import requests

# Считываем настройки из .env файла
env = Env()
env.read_env("api")

# Инициализируем бота
bot = telebot.TeleBot(env.str("HTTP_API"))

# Обработчики команд
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}")

@bot.message_handler(commands=['count'])
def subs_count(message):
    members_count = bot.get_chat_members_count(settings.bot.group_id)
    bot.send_message(message.chat.id, f'Количество участников: {members_count}')

@bot.message_handler(commands=['members'])
def subs_list(message):
    members = get_chat_members_from_api(settings.bot.group_id)
    if members is not None:
        member_list = [f'{member.user.first_name} {member.id}' for member in members]
        bot.send_message(message.chat.id, '\n'.join(member_list))

def get_chat_members_from_api(chat_id):
    try:
        bot_token = env.str("HTTP_API")
        url = f'https://api.telegram.org/bot{bot_token}/getChatMembersCount?chat_id={chat_id}'

        # Получите количество участников чата
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                members_count = data['result']
                bot.send_message(chat_id, f'Количество участников: {members_count}')
            else:
                print('Ошибка при запросе данных чата:', data['description'])
        else:
            print('Ошибка при выполнении запроса:', response.status_code)
    except Exception as e:
        print(f'Ошибка при получении списка участников: {e}')

if __name__ == "__main__":
    bot.polling(none_stop=True)
