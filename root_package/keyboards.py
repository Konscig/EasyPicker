from telethon import Button

keyboard_stopped = [
    [
        Button.inline("Победители", data="count_button"),
        Button.inline("Таймер", data="timer_button"),
        Button.inline("Текст", data="text_button")
    ],
    [
        Button.inline("✅       Запуск       ✅", data="start_button")
    ],
    [
        Button.inline("Отмена", data="delete_button"),
        Button.inline("Скрыть", data="close_button")
    ]
]

keyboard_started = [
    [
        Button.inline("Победители", data="count_button"),
        Button.inline("Таймер", data="timer_button"),
        Button.inline("Текст", data="text_button")
    ],
    [
        Button.inline("❌   Остановить   ❌", data="stop_button")
    ],
    [
        Button.inline("Отмена", data="delete_button"),
        Button.inline("Скрыть", data="close_button")
    ]
]
