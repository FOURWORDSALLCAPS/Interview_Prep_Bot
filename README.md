# Interview_Prep_Bot

Этот код представляет собой бота Telegram, который поможет подготовиться к собеседованию

## Установка зависимостей

Запускаем CMD (можно через Win+R, дальше вводим cmd) и вписываем команду cd /D <путь к папке с ботом>

```
pip install -r requirements.txt
```

## Шаблон вопросов
Ваши вопросы и ответы могут быть описаны в отдельном файле `questions.json`:

- Откройте файл questions.json в текстовом редакторе, таком как Notepad, Visual Studio Code, Sublime Text или любом другом удобном редакторе.

- JSON-файл представляет собой словарь, где ключами являются разделы (например, "Python", "Django", "General"), и каждый раздел содержит массив объектов вопросов и ответов.

```json
{
  "Python": [
    {
      "id": 1,
      "text": "Какой-то вопрос по Python",
      "answer": "Ответ на вопрос по Python",
      "example": "def some_function(*args):"
    },
    {
      "id": 2,
      "text": "Какой-то вопрос по Python",
      "answer": "Ответ на вопрос по Python",
      "example": "False"
    }
  ],
  "Django": [
    {
      "id": 1,
      "text": "Какой-то вопрос по Django",
      "answer": "Ответ на вопрос по Django",
      "example": "def some_function(*args):"
    },
    {
      "id": 2,
      "text": "Какой-то вопрос по Python",
      "answer": "Ответ на вопрос по Python",
      "example": "False"
    }
  ],
  "General": [
    {
      "id": 1,
      "text": "Какой-то общий вопрос",
      "answer": "Ответ на общий вопрос",
      "example": "def some_function(*args):"
    },
    {
      "id": 2,
      "text": "Какой-то вопрос по Python",
      "answer": "Ответ на вопрос по Python",
      "example": "False"
    }
  ]
}
```
- Для каждого раздела (например, "Python"), добавьте новые объекты в массив, представляя вопрос и соответствующий ему ответ. Убедитесь, что каждый объект имеет уникальный id.

- Добавьте пример кода в массив, если такой имеется! Иначе оставьте ```"example": "False"```

- Сохраните изменения в файле questions.json.

- После заполнения файла вопросами и ответами по вашим предпочтениям, вы можете использовать этот файл в вашем боте.

## Запуск бота 

```
python tg_interview_bot.py
```

## Деплой

Тут можно проверить бота Телеграм в работе: [Telegram](https://t.me/interview_py_bot)
Напишите ему /start и он начнет работать

## Переменные окружения

Часть настроек берётся из переменных окружения. Чтобы их определить, создайте файл `.env` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступна 1 переменная:
- `TG_BOT_TOKEN` — Токен Telegram-бота, полученный от [BotFather](https://t.me/BotFather)

## Версия Python: 
Я использовал Python `3.8.3`, но он должен работать на любой более новой версии.

## Цель проекта:
Цель проекта Interview_Prep_Bot состоит в создании бота для Telegram, который будет предоставлять пользователю помощь в подготовке к собеседованиям. Бот предоставляет информацию и ресурсы, необходимые для успешной подготовки, помогает в изучении материалов и задач

## Автор
(2023) Zaitsev Vladimir
