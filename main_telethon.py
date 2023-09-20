import asyncio
import sys
import logging
import time

from random import randint

from telethon import Button

from telethon import TelegramClient, events, types
from root_package.settings import settings
from root_package.mess_list import phrases, farewell_phrases
from root_package.keyboards import keyboard_stopped, keyboard_started

from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.messages import SendInlineBotResultRequest

bot = TelegramClient('bot_session', settings.bot.api_id, settings.bot.api_hash)
bot.parse_mode = "html"

keyboard = keyboard_stopped
timer = 0
count = 0
text = ""
message_list = []
message_list1 = []
data_message = ""

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.peer_id.user_id == settings.bot.admin_id:
        await bot.delete_messages(event.chat_id, message_ids=event.message.id)
        await event.respond(f"Здравствуйте, {event.sender.first_name}")


@bot.on(events.NewMessage(pattern='/count'))
async def subs_count(event):
    if event.peer_id.user_id == settings.bot.admin_id:
        await bot.delete_messages(event.chat_id, message_ids=event.message.id)
        count = await bot.get_participants(settings.bot.group_name)
        await event.respond(f'Количество участников: {count.total}')


@bot.on(events.NewMessage(pattern='/members'))
async def subs_list(event):
    if event.peer_id.user_id == settings.bot.admin_id:
        await bot.delete_messages(event.chat_id, message_ids=event.message.id)
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


in_list = ['🌚', '🔥', '✅', '😍', '👑', '✔', '☑️', '⚡', '😈', '❤️', '❤️‍🔥', '⭐', '🌟', '♥️', '💖', '💎', '⚜️', '🥳', '🥵', '🧲',
           '🚀', '😱', '💛', '🤩', '🍺', '🍻', '🇨🇳', '🍚']
out_list = ['🗿', '💩', '🐁', '✍', '🐷', '❌', '😕', '☠️', '😭', '😔', '🤖', '🐔', '🍆', '💦', '🐭', '🤬', '😡', '🐤', '🐒', '🙉', '🐟',
            '🤡', '👽', '👾']


@bot.on(events.ChatAction())
async def chat_action(event):
    if str(event.chat_id) == str(settings.bot.group_id):

        if event.user_added:
            user = await event.get_user()
            if user.username:
                name = user.username
            elif user.first_name:
                name = user.first_name
            else:
                name = user.id
            await bot.send_message(settings.bot.admin_id, f'Участник {name} вошел в канал.')
            random_index = randint(0, len(in_list) - 1)
            random_element = in_list[random_index]
            await bot.send_message(settings.bot.admin_id,
                                   f'{random_element} {phrases[randint(0, len(phrases))]} - {name}!')
        elif event.user_left:
            user = await event.get_user()
            if user.username:
                name = user.username
            elif user.first_name:
                name = user.first_name
            else:
                name = user.id
            await bot.send_message(settings.bot.admin_id, f'Участник {name} вышел из канала.')
            random_index = randint(0, len(out_list) - 1)
            random_element = out_list[random_index]
            await bot.send_message(settings.bot.admin_id,
                                   f'{random_element} {farewell_phrases[randint(0, len(farewell_phrases))]} {name}...')


@bot.on(events.NewMessage(pattern='/random'))
async def random_winner(event):
    global Kmsg
    if event.sender.id == settings.bot.admin_id:
        await event.respond('Введите количество победителей (count):')
        await bot.get_messages(5867206789, limit=1)
        print(await bot.get_messages(5867206789, limit=1))

        await event.respond('Введите таймер (в секундах) перед определением победителей (timer):')
        Kmsg = bot.get_messages(5867206789, limit=1).text
        print(Kmsg, " r")

    else:
        await event.respond('Вы не администратор бота.')
        return

    await asyncio.sleep(int(timer))

    participants = await bot.get_participants(settings.bot.group_name)
    win_list = list()
    for i in range(len(participants)):
        if participants[i].id != 673819158 and participants[i].id != 5300757743 and participants[i].id != 6381033226:
            win_list.append(str(participants[i].id) + " " + str(participants[i].username))

    winners = []
    for i in range(int(count)):
        if win_list:
            winner_index = randint(0, len(win_list) - 1)
            winners.append(win_list.pop(winner_index))

    await event.respond(f'Победители: {", ".join(winners)}')


# @bot.on(events.NewMessage(pattern='/go'))
# async def randomchik(event):
#     await bot.delete_messages(event.chat_id, message_ids=event.message.id)
#     mesg = await bot.send_message(settings.bot.group_name, "🎁Конкурс🎁\n"
#                                                            "Чтобы принять участие, вам необходимо:\n"
#                                                            "1) Быть участником канала🧬\n"
#                                                            "2) Не быть Кашалотиком (Ильей🐳) и Женьком🤡\n"
#                                                            "3) Нажать на кнопку и ждать результат!!💋💋💋",
#                                   buttons=[Button.inline('Участвовать Первым🤓', data='checkout')])



@bot.on(events.NewMessage(pattern='/fake'))
async def fake(event):
    if event.peer_id.user_id == settings.bot.admin_id:
        await bot.delete_messages(event.chat_id, message_ids=event.message.id)
        await bot.send_message(settings.bot.group_name, "Это фейк...")


@bot.on(events.NewMessage(pattern='/give'))
async def give(event):
    if event.peer_id.user_id == settings.bot.admin_id:
        global message_list, keyboard
        await bot.delete_messages(event.chat_id, message_ids=event.message.id)
        if len(message_list) != 0:
            for message in reversed(message_list):
                await bot.delete_messages(entity=settings.bot.admin_id, message_ids=message.id)
            message_list = []
        mesg1 = await bot.send_message(settings.bot.admin_id, 'Перед запуском конкурса не забудьте установить '
                                                              'все необходимые параметры в **"Меню управления"**:',
                                       parse_mode='md', buttons=keyboard)
        message_list.append(mesg1)


@bot.on(events.NewMessage())
async def process_executor(event):
    if event.peer_id.user_id == settings.bot.admin_id:
        global data_message, timer, count, text
        if data_message == "":
            return
        elif data_message == "count_button":
            try:
                count = int(event.message.message)
            except:
                await bot.send_message(event.peer_id.user_id, "Неверный формат количества победителей, повторите ввод:")
                return
        elif data_message == "timer_button":
            try:
                timer = int(event.message.message)
                await bot.send_message(event.peer_id.user_id, "Неверный формат времени, повторите ввод:")
            except:
                return
        elif data_message == "text_button":
            text = event.message.message
        data_message = ""


@bot.on(events.CallbackQuery())
async def checkout(event):
    global timer, count, message_list, message_list1, keyboard, data_message
    # message = await bot.get_messages(entity)
    # print(message.text)
    event_data = event.data.decode('utf-8')
    if event_data == 'checkout':
        participants = await bot.get_participants(settings.bot.group_name)
        with open('root_package/go_list.txt', 'r+') as file:
            user_ids = set(line.strip() for line in file)
            user_id = str(event.query.user_id)
            if user_id not in user_ids:
                in_channel = False
                for participant in participants:
                    if str(participant.id) == user_id:
                        in_channel = True
                        break
                if in_channel:
                    file.write(user_id + '\n')
                    await bot.edit_message(settings.bot.admin_id, message_list1[0],
                                           buttons=[Button.inline(f'Уже участников: {len(user_ids) + 1}🤠', data='checkout')])
                    random_index = randint(0, len(in_list) - 1)
                    random_element = in_list[random_index]
                    await event.answer(f"{random_element} Вы красавчик! {random_element}", alert=True)
                else:
                    await event.answer("💢 Вы не подписаны 💢", alert=True)
            else:
                await event.answer("💞 Вы уже участник 💞", alert=True)
    elif event_data == "start_button":
        keyboard = keyboard_started
        await bot.edit_message(settings.bot.admin_id, message_list[0], buttons=keyboard)
        #if timer and count and mesg:
        if len(message_list1) == 0:
            await event.answer("🔥 Конкурс запущен 🔥", alert=True)
            mesg = await bot.send_message(settings.bot.admin_id, "🎁Конкурс🎁\n"
                                                                   "Чтобы принять участие, вам необходимо:\n"
                                                                   "1) Быть участником канала🧬\n"
                                                                   "2) Не быть Кашалотиком (Ильей🐳) и Женьком🤡\n"
                                                                   "3) Нажать на кнопку и ждать результат!!💋💋💋",
                                          buttons=[Button.inline('Участвовать в розыгрыше🤓', data='checkout')])
            message_list1.append(mesg)
        else:
            await event.answer("💢 Розыгрыш запущен 💢", alert=True)
    elif event_data == "stop_button":
        keyboard = keyboard_stopped
        await bot.edit_message(settings.bot.admin_id, message_list[0], buttons=keyboard)
        for message in message_list1:
            await bot.delete_messages(entity=settings.bot.admin_id, message_ids=message.id)
        message_list1 = []
        await event.answer("💢 Остановочка 💢", alert=True)
    elif event_data == "close_button":
        for message in message_list:
            await bot.delete_messages(entity=settings.bot.admin_id, message_ids=message.id)
        message_list = []
        await event.answer("Не забудьте про розыгрыш!")
    elif event_data == "delete_button":
        for message in message_list:
            await bot.delete_messages(entity=settings.bot.admin_id, message_ids=message.id)
        message_list = []
        for message in message_list1:
            await bot.delete_messages(entity=settings.bot.admin_id, message_ids=message.id)
        message_list1 = []
        keyboard = keyboard_stopped
        timer = 0
        count = 0
        await event.answer("💢 Розыгрыш удалён 💢", alert=True)
    elif event_data == "count_button":
        data_message = event_data
        await bot.send_message(settings.bot.admin_id, "Введите количество победителей:")
    elif event_data == "timer_button":
        data_message = event_data
        await bot.send_message(settings.bot.admin_id, "Установите таймер в формате(чч:мм:сс):")
    elif event_data == "text_button":
        data_message = event_data
        await bot.send_message(settings.bot.admin_id, "Введите текст сообщения розыгрыша:")


async def main():
    await bot.start(bot_token=settings.bot.bot_token)
    await bot.run_until_disconnected()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
