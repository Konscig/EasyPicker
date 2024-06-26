import asyncio
import sys
import logging
import time

from random import randint

from telethon import TelegramClient, events
from root_package.settings import settings
from root_package.mess_list import phrases, farewell_phrases

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

    max_message_length = 4096
    i = 1
    message = ""

    for participant in participants:
        current_info = ""
        current_info += "[ " + str(i) + " ]\n"
        
        if participant.first_name:
            current_info += f"├ {participant.first_name}\n"
        if participant.last_name:
            current_info += f"├ {participant.last_name}\n"
        if participant.username:
            current_info += f"├ USER: @{participant.username}\n"
        
        current_info += f"└ ID: {participant.id}\n"

        if len(message + current_info) < max_message_length:
            message += current_info
        else:
            await event.respond(message)
            message = current_info

        i += 1

    if message:
        await event.respond(message)

in_list  = ['🌚', '🔥', '✅', '😍', '👑', '✔', '☑️', '⚡', '😈', '❤️', '❤️‍🔥', '⭐', '🌟', '♥️', '💖', '💎', '⚜️', '🥳', '🥵', '🧲', '🚀', '😱', '💛', '🤩', '🍺', '🍻', '🇨🇳', '🍚']
out_list = ['🗿', '💩', '🐁', '✍', '🐷', '❌', '😕', '☠️', '😭', '😔', '🤖', '🐔', '🍆', '💦', '🐭', '🤬', '😡', '🐤', '🐒', '🙉', '🐟', '🤡', '👽', '👾']

@bot.on(events.ChatAction())
async def chat_action(event):
    if str(event.chat_id) == str(settings.bot.group_id):
        
        if event.user_added:
            user = await event.get_user()
            name = ""
            if user.username:
                name = user.username
            elif user.first_name:
                name = user.first_name
            else:
                name = user.id
            await bot.send_message(settings.bot.admin_id, f'Участник {name} вошел в канал.')
            random_index = randint(0, len(in_list) - 1)
            random_element = in_list[random_index]
            await bot.send_message(settings.bot.group_id, f'{random_element} {phrases[randint(0,len(phrases))]} - {name}!')
        elif event.user_left:
            user = await event.get_user()
            
            name = ""
            if user.username:
                name = user.username
            elif user.first_name:
                name = user.first_name
            else:
                name = user.id
            await bot.send_message(settings.bot.admin_id, f'Участник {name} вышел из канала.')
            random_index = randint(0, len(out_list) - 1)
            random_element = out_list[random_index]
            await bot.send_message(settings.bot.group_id, f'{random_element} {farewell_phrases[randint(0,len(farewell_phrases))]} {name}...')

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

