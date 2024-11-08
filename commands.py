from telebot.types import BotCommand
default_commands = [
    BotCommand(command='start', description='Начало работы с ботом'),
    BotCommand(command='help', description='Команды для работы с ботом'),
    BotCommand(command='new_list', description='Добавление нового списка задач'),
    BotCommand(command='show_lists', description='Вывод всех списков задач'),
    BotCommand(command='choose_list', description='Выбрать список задач'),
    BotCommand(command='get_current_list', description='Вывод текущего списка задач'),
    BotCommand(command='rename_list', description='Переименование текущего списка задач'),
    BotCommand(command='remove_list', description='Удаление текущего списка задач'),
    BotCommand(command='new_task', description='Создание новой задачи'),
    BotCommand(command='show_tasks', description='Вывод всех задач в выбарнном списке'),
    BotCommand(command='choose_task', description='Выбор задачи в текущем списке'),
    BotCommand(command='get_current_task', description='Вывод выбранной задачи'),
    BotCommand(command='update_status', description='Обновление статуса выбранной задачи'),
    BotCommand(command='remove_task', description='Удаление выбранной задачи'),
]

