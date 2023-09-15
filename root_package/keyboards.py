from telethon import Button

button1 = Button.inline('hi', data='checkout')

keyboard = [
    [
        Button.inline("Кол-во участников", data="count_button"),
        Button.inline("Таймер", data="timer_button")
    ],
    [
        Button.inline("Текст сообщения", data="text_button"),
        Button.inline("Удалить сообщение", data="delete_button")
    ],
    [
        Button.inline("Закрыть клавиатуру", data="close_button")
    ]
]
