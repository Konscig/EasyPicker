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
timer = None
count = None
text = None
is_raffle_running = None
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


    # for i in range(len(participants)):
    #     if participants[i].id != 673819158 and participants[i].id != 5300757743 and participants[i].id != 6381033226:
    #         win_list.append(str(participants[i].id) + " " + str(participants[i].username))


@bot.on(events.NewMessage(pattern='/fake'))
async def fake(event):
    if event.peer_id.user_id == settings.bot.admin_id:
        await bot.delete_messages(event.chat_id, message_ids=event.message.id)
        await bot.send_message(settings.bot.group_name, "Это фейк...")


@bot.on(events.NewMessage(pattern='/go'))
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
    chat_id = event.chat_id
    if int(chat_id) == settings.bot.admin_id:
        global data_message, timer, count, text, message_list, keyboard
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
            except:
                await bot.send_message(event.peer_id.user_id, "Неверный формат времени, повторите ввод:")
                return
        elif data_message == "text_button":
            text = event.message.message
        data_message = ""
        if len(message_list) != 0:
            for message in reversed(message_list):
                await bot.delete_messages(entity=settings.bot.admin_id, message_ids=message.id)
            message_list = []
        mesg1 = await bot.send_message(settings.bot.admin_id, 'Перед запуском конкурса не забудьте установить '
                                                              'все необходимые параметры в **"Меню управления"**:',
                                       parse_mode='md', buttons=keyboard)
        message_list.append(mesg1)


@bot.on(events.CallbackQuery())
async def checkout(event):
    global timer, count, text, message_list, message_list1, keyboard, data_message, is_raffle_running
    # await bot.catch_up()
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
                    await bot.edit_message(settings.bot.group_name, message_list1[0],
                                           buttons=[Button.inline(f'Уже участников: {len(user_ids) + 1}🤠', data='checkout')])
                    random_index = randint(0, len(in_list) - 1)
                    random_element = in_list[random_index]
                    await event.answer(f"{random_element} Вы теперь участник! {random_element}")
                else:
                    await event.answer("💢 Вы не подписаны 💢")
            else:
                await event.answer("💢 Вы уже участвуете 💢")
    elif event_data == "start_button":
        if count and timer and text:
            keyboard = keyboard_started
            await bot.edit_message(settings.bot.admin_id, message_list[0], buttons=keyboard)
            if len(message_list1) == 0:
                await event.answer("🔥 Конкурс запущен 🔥")
                mesg = await bot.send_message(settings.bot.group_name, message=text,
                                              buttons=[Button.inline('Участвовать в розыгрыше🤓', data='checkout')])
                message_list1.append(mesg)

                is_raffle_running = True

                await asyncio.sleep(int(timer))

                if is_raffle_running:
                    winners = []
                    with open('root_package/go_list.txt', 'r') as file:
                        user_ids = list(line.strip() for line in file)
                        for i in range(min(len(user_ids),count)):
                            if user_ids:
                                winner_index = randint(0, len(user_ids) - 1)
                                winners.append(user_ids.pop(winner_index))

                    i = 1
                    for i in range(len(winners)):
                        winners[i] = await bot.get_entity(int(winners[i]))
                    print(len(winners))
                    for participant in winners:
                        current_info = ""
                        current_info += "[ " + str(i) + " ]\n"

                        if participant.first_name:
                            current_info += f"├ {participant.first_name}\n"
                        if participant.last_name:
                            current_info += f"├ {participant.last_name}\n"
                        if participant.username:
                            current_info += f"├ USER: @{participant.username}\n"

                        current_info += f"└ ID: {participant.id}\n"
                        winners[i-1] = current_info

                        i += 1

                    await event.respond(f'Победители:\n{"".join(winners)}')
            else:
                await event.answer("💢 Розыгрыш запущен 💢")
        else:
            ans_list = []
            if not(count): ans_list.append("кол-во победителей")
            if not(timer): ans_list.append("таймер")
            if not(text): ans_list.append("текст")

            await event.answer("Установите: " + ", ".join(ans_list))
    elif event_data == "stop_button":
        is_raffle_running = False

        keyboard = keyboard_stopped
        await bot.edit_message(settings.bot.admin_id, message_list[0], buttons=keyboard)
        for message in message_list1:
            await bot.delete_messages(entity=settings.bot.group_name, message_ids=message.id)
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
            await bot.delete_messages(entity=settings.bot.group_name, message_ids=message.id)
        message_list1 = []
        keyboard = keyboard_stopped
        timer = None
        count = None
        text = None
        is_raffle_running = False
        await event.answer("💢 Розыгрыш удалён 💢")
    elif event_data == "count_button":
        data_message = event_data
        await bot.send_message(settings.bot.admin_id, "Введите количество победителей:")
        await event.answer()
    elif event_data == "timer_button":
        data_message = event_data
        await bot.send_message(settings.bot.admin_id, "Установите таймер в секундах:")
        await event.answer()
    elif event_data == "text_button":
        data_message = event_data
        await bot.send_message(settings.bot.admin_id, "Введите текст сообщения розыгрыша:")
        await event.answer()


async def main():
    await bot.start(bot_token=settings.bot.bot_token)
    await bot.run_until_disconnected()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
