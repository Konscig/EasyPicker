from telethon import Button

keyboard = [
    [
        Button.inline("Кол-во победителей", data="count_button"),
        Button.inline("Таймер", data="timer_button")
    ],
    [
        Button.inline("Текст сообщения", data="text_button"),
        Button.inline("✅Запуск✅", data="start_button")
    ],
    [
        Button.inline("❌Отмена❌", data="delete_button"),
        Button.inline("Закрыть клавиатуру", data="close_button")
    ]
]
