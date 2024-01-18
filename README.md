# Simple Discord bot, with VKAPI integration

## Что умеет?

Определять тип странице по ссылке, выводить имя и id, а так же дату регистрации если это страница юзера.

## Установка

```bash
git clone https://github.com/VenueYounk/TestTaskGetInfo.git
```

Создать файл .env и указать переменные окружения.

```bash
docker build -t discord_bot .
docker run -d discord_bot
```

## Использование

Команда /get_info ` <link> в дискорд боте`

Вывод:

![1705607596616](image/README/1705607596616.png)
