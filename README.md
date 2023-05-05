# QuizBot

Боты предназначены для викторины: "вопрос-ответ"

#### Пример работы ботов [Телеграм](https://t.me/spv_quiz_bot) и [VK](https://vk.com/club220264064)

#### Требования перед установкой:
1. Создайте бота в телеграм - напишите отцу ботов [@BotFather](https://t.me/BotFather)
2. Аналогично создайте еще одного бота - он будет высылать вам отчеты об ошибках
3. Получите ID своего чата - в него будут приходить сообщения об ошибках [@userinfobot](https://t.me/userinfobot)
4. Создайте сообщество в [VK](https://vk.com/groups?tab=admin)
5. Получите токен на кладке _Управление -> Работа с API_
6. Получите url, порт и пароль для подключения к облачному сервису [Redis](https://redis.com/) 

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.9.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

#### Установка и запуск:
Скопируйте файлы из репозитория в папку:
```sh
git clone https://github.com/spawlov/QuizBot.git
```

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`

В корне проекта создайте файл _.env_ со следующим содержимым:

```text
TG_TOKEN=<Токен вашего бота в телеграм>
LOGGER_BOT_TOKEN=6221846115:<Токен вашего бота-логгера в телеграм>
ALLOWED_CHAT_ID=<ID вашего чата, в который будут прилодить сообщения от логера>

VK_TOKEN=<Токен вашего сообщества во ВКонакте>

REDIS_HOST=<URL для подключения к Redis>
REDIS_PORT=<Порт для подключения к Redis>
REDIS_USER=<Логин для Redis>
REDIS_PASSWORD=<Пароль для Redis>
```

В корне проекта создайте папку _quections_ - в ней должны раполагаться текстовые 
файлы с вопросами и ответами на них. 

Папка _questions_ определена по-умолчанию, если у вас файлы будут расположены в другой папке - определите в файле _.env_ переменную:

```text
QUESTIONS_DIR=<Имя вашей папки без кавычек и слешей в начале и конце>
```

По-умолчанию предполагается, что кодировка файлов с вопросами _UTF-8_ - если ваши файлы будут в другой кодировке - определите в файле  -.env- переменную:

```text
QUESTIONS_ENCODE=<Кодировка ваших файлов с вопросами, например KOI8-R>
```

**Важно! - все файлы с вопросами должны быть _txt_ и одинаковой кодировки!**

Архив с вопросами можно скачать [по этой ссылке...](https://dvmn.org/media/modules_dist/quiz-questions.zip)

Формат файла с вопросами, должен иметь следующий формат:

```text
Вопрос:
Разработчик проекта первой полудеревянной цифровой вычислительной машины
Чарлз Бэббидж (1792-1872) изобрел, кроме этого, еще одно устройство,
которое он назвал "Difference Engine". Бэббидж предполагал, что это
устройство будет использоваться в навигации, проектировании, банковском
и страховом деле. Как сейчас называется подобное устройство?

Ответ:
Принтер.

Автор:
Максим Поташев
```

Установите зависимости:

```sh
pip install -r requirements.txt
```

Запуск обоих ботов осуществляется командой:

```sh
python main.py
```
