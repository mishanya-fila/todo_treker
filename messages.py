from telebot import formatting
from telebot import types

from main import Task

help_msg = f'Команды для работы с ботом:\n' \
           f'- {formatting.hcode("/start")} - начало работы с ботом\n' \
           f'- {formatting.hcode("/help")} - команды для работы с ботом\n' \
           f'- {formatting.hcode("Новый список задач")} - добавление нового списка задач\n' \
           f'- {formatting.hcode("Списки задач")} - вывод всех списков задач\n' \
           f'- {formatting.hcode("Переименовать список задач")} - переименование текущего списка задач\n' \
           f'- {formatting.hcode("Удалить список задач")} - удаление текущего списка задач\n' \
           f'- {formatting.hcode("Новая задача")} - создание новой задачи\n' \
           f'- {formatting.hcode("Задачи в списке")} - вывод всех задач в выбарнном списке\n' \
           f'- {formatting.hcode("✅/❌")} - обновление статуса выбранной задачи\n' \
           f'- {formatting.hcode("🗑")} - удаление выбранной задачи\n' \
           f'Команды доступны через нажатие по кнопке, поэтому не нужно набирать их вручную'
start_msg = f'Привет! Это бот для отслеживания задач.\n' \
            f'Для просмотра доступных команд введите {formatting.hcode("/help")}'
add_new_task_list_msg = 'Введите название нового списка задач'
success_add_new_task_list = 'Новый список задач успешно добавлен'

no_lists = f'Не добавлено ни одного списка задач.\n' \
           f'Добавьте новый список задач нажав {formatting.hcode("Новый список задач")}'


def prepare_show_lists_msg(lists_name: dict.keys):
    keyboard = types.InlineKeyboardMarkup()
    show_list_msg = 'Текущие списки задач:'
    for i in lists_name:
        inline_button = types.InlineKeyboardButton(text=i, callback_data=i)
        keyboard.add(inline_button)
    return show_list_msg, keyboard


success_choose_list = 'Список задач "{}" успешно выбран!'
rename_message = 'Введите новое название для текущего списка задач'

same_names = f'Новое название текущего списка совпадает со старым. ' \
             f'Нажмите кнопку {formatting.hcode("Переименовать список задач")} и введите {formatting.hbold("новое")} ' \
             f'имя списка задач'
rename_success = 'Название списка успешно обновлено'
remove_list_msg = f'Вы уверенны, что хотите удалить текущий список задач?'
success_remove_list = 'Текущий список задач был успешно удалён'
new_task = 'Введите имя новой задачи'
success_create_task = 'Задача "{}" успешно добавлена в список "{}"'


def prepare_no_tasks_msg(ls_name):
    msg = f'В список "{ls_name}" не добавлено ни одной задачи.\n' \
          f'Добавить новую задачу можно кнопкой {formatting.hcode("Новая задача")}'
    return msg


list_not_remove = 'Список задач не был удалён'


def prepare_show_tasks_msg(res_list: [Task], key: str):
    msg = f'Текущие задачи в списке "{key}":\n'
    keyboard = types.InlineKeyboardMarkup()
    for i in res_list:
        i: Task
        task_name_button = types.InlineKeyboardButton(text=i.name, callback_data='task')
        task_status_button = None
        if i.status:
            task_status_button = types.InlineKeyboardButton(text='✅', callback_data=i.name)
        elif not i.status:
            task_status_button = types.InlineKeyboardButton(text='❌', callback_data=i.name)
        to_trash_button = types.InlineKeyboardButton(text='🗑', callback_data=f'{i.name} to_trash')
        keyboard.add(task_name_button, task_status_button, to_trash_button, row_width=4)
    return msg, keyboard


remove_task_msg = 'Задача была успешно удалена'
echo_message = f'Бот не понимает данного сообщения.\n' \
               f'Воспользуйтесь командой {formatting.hcode("/help")} чтобы увидеть возможности бота'
command_in_text_msg = 'В переданном тексте указано имя команды.\n' \
                      'Пожалуйста, не используйте имена команд в качестве имён задач и имён списков задач!'
