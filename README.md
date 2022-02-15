# Разговаривающий орган Бендера
Выделен в отдельный сервис из проекта The Headless Bot

## Функциональная часть
Базируется на модели [отсюда.](https://huggingface.co/Grossmend/rudialogpt3_medium_based_on_gpt2)
Описание [здесь.](https://habr.com/ru/company/icl_services/blog/548244)

### Внешний вид
Одна страничка, на экране окно ввода, кнопка 'Send' и ниже - диалог с Бендером.

### Сценарии:
- пользователь открывает страничку, что-то пишет - Бендер отвечает.
- бот или пользователь обращается к приложению посредством REST запроса - Бендер отвечает.

### Структура каталогов
- app - функционал сервиса.
- data - данные для веб-интерфейса.
- data_local/gpt2 - файлы модели. В репозиторий и в контейнер не уходят ввиду объемности, необходимо скачивать отдельно по ссылке выше.
- env - вспомогательные файлы - скрипты проверки, файлы докера. В скриптах *.cmd предполагается что окружение находится в venv.
- tests - юнит-тесты pytest и коллекция тестов Postman'а. Тесты Постмана приложены информационно, их необходимо вручную импортировать и запускать в Постмане.
- utils - вспомогательные классы, которые не относятся напрямую ни к функционалу, ни к веб-приложению.
- webapp - веб-приложение и API.
