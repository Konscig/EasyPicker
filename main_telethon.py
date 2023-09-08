import asyncio
import sys
import logging

from random import randint

from telethon import TelegramClient, events
from root_package.settings import settings

bot = TelegramClient('bot_session', settings.bot.api_id, settings.bot.api_hash)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(f"Здравствуйте, {event.sender.first_name}")


@bot.on(events.NewMessage(pattern='/count'))
async def subs_count(event):
    count = await bot.get_participants(settings.bot.group_name)
    await event.respond(f'Количество участников: {count.total}')


@bot.on(events.NewMessage(pattern='/members'))
async def subs_list(event):
    participants = await bot.get_participants(settings.bot.group_name)

    string = ""
    for participant in participants:
        string += "ID: " + str(participant.id) + " USERNAME:" + str(participant.username) + '\n'
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


@bot.on(events.NewMessage(pattern='/random'))
async def random_winner(event):
    participants = await bot.get_participants(settings.bot.group_name)
    win_list = list()
    for i in range(len(participants)):
        if (participants[i].id != 673819158 and participants[i].id != 5300757743 and participants[i].id != 6381033226):
            win_list.append(str(participants[i].id)+" "+str(participants[i].username))
    winners = []
    count = 2
    for i in range(count):
        winner = randint(0, len(win_list))
        winners.append(win_list[winner])
        del win_list[winner]
    print(winners)


async def main():
    await bot.start(bot_token=settings.bot.bot_token)
    await bot.run_until_disconnected()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
