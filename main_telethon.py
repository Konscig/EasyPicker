import asyncio
import sys
import logging
import time

from random import randint

from telethon import TelegramClient, events
from root_package.settings import settings

bot = TelegramClient('bot_session', settings.bot.api_id, settings.bot.api_hash)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(f"Здравствуйте, {event.sender.first_name}")

@bot.on(events.CallbackQuery)
async def top(event):
    async for message in bot.iter_messages(581154838, limit=1):
        print(message.id, message.text)

@bot.on(events.NewMessage(pattern='/try'))
async def prov(event):
    await top(event)
@bot.on(events.NewMessage(pattern='/count'))
async def subs_count(event):
    count = await bot.get_participants(settings.bot.group_name)
    await event.respond(f'Количество участников: {count.total}')

@bot.on(events.NewMessage(pattern='/members'))
async def subs_list(event):
    participants = await bot.get_participants(settings.bot.group_name)

    string = ""
    i = 1
    for participant in participants:

        string += str(i) + ".\n"
        if participant.username != None:
            string += "├ ID: " + str(participant.id) + "\n"
            string += "└ USERNAME: " + str(participant.username) + "\n"
        else:
            string += "└ ID: " + str(participant.id) + "\n"
        i += 1
    await event.respond(f'{string}')

@bot.on(events.ChatAction())
async def chat_action(event):
    if str(event.chat_id) == str(settings.bot.group_id):
        if event.user_added:
            user = await event.get_user()
            await bot.send_message(settings.bot.admin_id, f'Участник {user.first_name} {user.id} вошел в канал.')
        elif event.user_left:
            user = await event.get_user()
            await bot.send_message(settings.bot.admin_id, f'Участник {user.first_name} {user.id} вышел из канала.')

async def admin_reply():
    global Kmsg
    while True:
        if Kmsg != bot.get_messages(5867206789, limit=1):
            break
    return bot.get_messages(5867206789, limit=1)

@bot.on(events.NewMessage(pattern='/random'))
async def random_winner(event):
    global Kmsg
    if event.sender.id == settings.bot.admin_id:
        await event.respond('Введите количество победителей (count):')
        await bot.get_messages(5867206789, limit=1)
        print(await bot.get_messages(5867206789, limit=1))
        count = admin_reply()

        await event.respond('Введите таймер (в секундах) перед определением победителей (timer):')
        Kmsg=bot.get_messages(5867206789, limit=1).text
        print(Kmsg, " r")
        timer = admin_reply()

    else:
        await event.respond('Вы не администратор бота.')
        return
    
    await asyncio.sleep(int(timer))

    participants = await bot.get_participants(settings.bot.group_name)
    win_list = list()
    for i in range(len(participants)):
        if (participants[i].id != 673819158 and participants[i].id != 5300757743 and participants[i].id != 6381033226):
            win_list.append(str(participants[i].id) + " " + str(participants[i].username))

    winners = []
    for i in range(int(count)):
        if win_list:
            winner_index = randint(0, len(win_list) - 1)
            winners.append(win_list.pop(winner_index))

    await event.respond(f'Победители: {", ".join(winners)}')



async def main():
    await bot.start(bot_token=settings.bot.bot_token)
    await bot.run_until_disconnected()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
