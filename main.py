import csv

from telebot import TeleBot
from telebot import types

import messages
from commands import default_commands
from config.config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)
user_states = {}
current_lists = {}
current_tasks = {}


class Task:
    def __init__(self, name, status=False):
        self.name = name
        self.status = status

    def update_status(self):
        self.status = not self.status


def read_data():
    with open('data.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'id':
                continue
            row = list(filter(lambda x: x, row))
            identifier = int(row[0])
            if len(row) == 1 and user_states.get(identifier) is None:
                user_states[identifier] = {}
            if len(row) == 2:
                list_name = row[1]
                if user_states.get(identifier) is None:
                    user_states[identifier] = {}
                user_states[identifier][list_name] = {}
            if len(row) == 4:
                list_name = row[1]
                task_name = row[2]
                task_satus = True if row[3] == 'True' else False
                if user_states.get(identifier) is None:
                    user_states[identifier] = {}
                if user_states[identifier].get(list_name) is None:
                    user_states[identifier][list_name] = {}
                user_states[identifier][list_name].update({task_name: Task(name=task_name, status=task_satus)})


def save_data():
    columns = ['id', 'list_name', 'task_name', 'task_status']
    with open(file='data.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for identifier in user_states:
            if not user_states[identifier]:
                writer.writerow([identifier, None, None, None])
                continue
            for list_name in user_states[identifier]:
                if not user_states[identifier][list_name].values():
                    writer.writerow([identifier, list_name, None, None])
                for task in user_states[identifier][list_name].values():
                    row = [identifier, list_name, task.name, task.status]
                    writer.writerow(row)


def save_current_list():
    columns = ['id', 'list_name']
    with open('current_lists.csv', encoding='utf-8', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for row in current_lists.items():
            writer.writerow(list(row))


def get_current_list():
    with open('current_lists.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'id':
                continue
            identifier = int(row[0])
            list_name = row[1]
            current_lists[identifier] = list_name


def save_current_task():
    columns = ['id', 'task_name']
    with open('current_task.csv', encoding='utf-8', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for row in current_tasks.items():
            writer.writerow(list(row))


def get_current_task():
    with open('current_task.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'id':
                continue
            identifier = int(row[0])
            task_name = row[1]
            current_tasks[identifier] = task_name


def command_in_text(msg: types.Message):
    buttons_text = ['Новый список задач', 'Списки задач', 'Переименовать список задач', 'Удалить список задач',
                    'Новая задача', 'Задачи в списке', '📝', '🗑', '❌', '✅']
    if any(['/' + str(i.command) in msg.text for i in default_commands]) or msg.text in buttons_text:
        return True


@bot.message_handler(commands=['start'])
def send_start_message(msg: types.Message):
    if msg.chat.id not in user_states.keys():
        user_states[msg.chat.id] = {}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    show_lists_button = types.KeyboardButton(text='Списки задач')
    create_new_list = types.KeyboardButton(text='Новый список задач')
    keyboard.add(show_lists_button, create_new_list)
    bot.send_message(chat_id=msg.chat.id, text=messages.start_msg, parse_mode='HTML', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send_help_message(msg: types.Message):
    bot.send_message(chat_id=msg.chat.id, text=messages.help_msg, parse_mode='HTML')


@bot.message_handler(func=lambda msg: msg.text == 'Новый список задач')
def handle_new_list_msg(msg: types.Message):
    message = bot.send_message(chat_id=msg.chat.id, text=messages.add_new_task_list_msg)
    bot.register_next_step_handler(message=message, callback=callback_new_list)


def callback_new_list(msg: types.Message):
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        return
    user_states[msg.chat.id][msg.text] = {}
    current_lists[msg.chat.id] = msg.text
    bot.send_message(chat_id=msg.chat.id, text=messages.success_add_new_task_list)
    save_data()
    save_current_list()


@bot.message_handler(func=lambda msg: msg.text == 'Списки задач')
def show_lists(msg: types.Message):
    if user_states[msg.chat.id] == {}:
        bot.send_message(chat_id=msg.chat.id, text=messages.no_lists, parse_mode='HTML')
        return
    text, keyboard = messages.prepare_show_lists_msg(user_states[msg.chat.id].keys())
    bot.send_message(chat_id=msg.chat.id, text=text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in user_states[call.message.chat.id])
def callback_choose_list(call: types.CallbackQuery):
    if current_tasks.get(call.message.chat.id):
        current_tasks.pop(call.message.chat.id)
    current_lists[call.message.chat.id] = call.data
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    show_lists_button = types.KeyboardButton(text='Списки задач')
    show_tasks_button = types.KeyboardButton(text='Задачи в списке')
    create_new_list = types.KeyboardButton(text='Новый список задач')
    create_new_task = types.KeyboardButton(text='Новая задача')
    rename_list_button = types.KeyboardButton(text='Переименовать список задач')
    remove_list_button = types.KeyboardButton(text='Удалить список задач')
    keyboard.add(show_lists_button, show_tasks_button, create_new_list, create_new_task, rename_list_button,
                 remove_list_button)
    bot.send_message(chat_id=call.message.chat.id, text=messages.success_choose_list.format(call.data),
                     reply_markup=keyboard)
    save_current_list()


@bot.message_handler(func=lambda msg: msg.text == 'Переименовать список задач')
def rename_list(msg: types.Message):
    message = bot.send_message(chat_id=msg.chat.id, text=messages.rename_message)
    bot.register_next_step_handler(message=message, callback=rename_callback)


def rename_callback(msg: types.Message):
    if current_lists.get(msg.chat.id) == msg.text:
        bot.send_message(chat_id=msg.chat.id, text=messages.same_names, parse_mode='HTML')
        return
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        return
    old_name = current_lists[msg.chat.id]
    new_name = msg.text
    current_lists[msg.chat.id] = new_name
    user_states[msg.chat.id][new_name] = user_states[msg.chat.id][old_name]
    user_states[msg.chat.id].pop(old_name)
    bot.send_message(chat_id=msg.chat.id, text=messages.rename_success)
    save_current_list()
    save_data()


@bot.message_handler(func=lambda msg: msg.text == 'Удалить список задач')
def remove_list(msg: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text='Да', callback_data='yes')
    no_button = types.InlineKeyboardButton(text='Нет', callback_data='not')
    keyboard.add(yes_button, no_button)
    bot.send_message(chat_id=msg.chat.id, text=messages.remove_list_msg, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'yes' or call.data == 'not')
def callback_remove_list(call: types.CallbackQuery):
    if call.data == 'not':
        bot.send_message(chat_id=call.message.chat.id, text=messages.list_not_remove)
        return
    if call.data == 'yes':
        list_name = current_lists[call.message.chat.id]
        user_states[call.message.chat.id].pop(list_name)
        current_lists.pop(call.message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        show_lists_button = types.KeyboardButton(text='Списки задач')
        create_new_list = types.KeyboardButton(text='Новый список задач')
        keyboard.add(show_lists_button, create_new_list)
        bot.send_message(chat_id=call.message.chat.id, text=messages.success_remove_list, reply_markup=keyboard)
        save_current_list()
        save_data()


@bot.message_handler(func=lambda msg: msg.text == 'Новая задача')
def create_task(msg: types.Message):
    message = bot.send_message(chat_id=msg.chat.id, text=messages.new_task)
    bot.register_next_step_handler(message=message, callback=callback_create_task)


def callback_create_task(msg: types.Message):
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        return
    chat_id = msg.chat.id
    cur_list = current_lists[chat_id]
    user_states[chat_id][cur_list].setdefault(msg.text, Task(name=msg.text))
    bot.send_message(chat_id=msg.chat.id, text=messages.success_create_task.format(msg.text, cur_list))
    save_data()


@bot.message_handler(func=lambda msg: msg.text == 'Задачи в списке')
def show_tasks(msg: types.Message):
    cur_ls = current_lists[msg.chat.id]
    if not user_states[msg.chat.id][cur_ls]:
        bot.send_message(chat_id=msg.chat.id, text=messages.prepare_no_tasks_msg(cur_ls), parse_mode='HTML')
        return
    task_list: [Task] = user_states[msg.chat.id][cur_ls].values()
    text, keyboard = messages.prepare_show_tasks_msg(task_list, cur_ls)
    bot.send_message(chat_id=msg.chat.id, text=text, reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data in user_states[call.message.chat.id][current_lists[call.message.chat.id]])
def update_status(call: types.CallbackQuery):
    current_task = call.data
    chat_id = call.message.chat.id
    current_list = current_lists[chat_id]
    user_states[chat_id][current_list][current_task].update_status()
    call.data = user_states[chat_id][current_list][current_task].status
    show_tasks(msg=call.message)
    save_data()


@bot.callback_query_handler(func=lambda call: 'rename' in call.data.split())
def rename_task(call: types.CallbackQuery):
    if len(call.data.split()) > 2:
        task_name = ' '.join(call.data.split()[:-1])
    else:
        task_name = call.data.split()[0]
    current_tasks[call.message.chat.id] = task_name
    message = bot.send_message(chat_id=call.message.chat.id, text=messages.rename_task_message)
    bot.register_next_step_handler(message=message, callback=rename_task_callback)
    save_current_task()


def rename_task_callback(msg: types.Message):
    new_name = msg.text
    old_name = current_tasks[msg.chat.id]
    if old_name == new_name:
        bot.send_message(chat_id=msg.chat.id, text=messages.rename_same_tasks, parse_mode='HTML')
        show_tasks(msg=msg)
        return
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        show_tasks(msg=msg)
        return
    curr_list = current_lists[msg.chat.id]
    current_tasks[msg.chat.id] = new_name
    user_states[msg.chat.id][curr_list][new_name] = user_states[msg.chat.id][curr_list][old_name]
    user_states[msg.chat.id][curr_list].pop(old_name)
    user_states[msg.chat.id][curr_list][new_name].name = new_name
    bot.send_message(chat_id=msg.chat.id, text=messages.rename_task_success)
    save_current_task()
    save_data()


@bot.callback_query_handler(func=lambda call: call.data.split())
def remove_task(call: types.CallbackQuery):
    if len(call.data.split()) > 2:
        task_name = ' '.join(call.data.split()[:-1])
    else:
        task_name = call.data.split()[0]
    user_states[call.message.chat.id][current_lists[call.message.chat.id]].pop(task_name)
    bot.send_message(chat_id=call.message.chat.id, text=messages.remove_task_msg)
    show_tasks(msg=call.message)
    save_data()


@bot.message_handler(func=lambda msg: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                           'text', 'location', 'contact', 'sticker'])
def echo_message(msg: types.Message):
    bot.send_message(chat_id=msg.chat.id, text=messages.echo_message, parse_mode='HTML')


if __name__ == '__main__':
    read_data()
    get_current_list()
    get_current_task()
    bot.enable_saving_states()
    bot.enable_save_next_step_handlers(delay=1)
    bot.load_next_step_handlers()
    bot.set_my_commands(default_commands)
    bot.infinity_polling(skip_pending=True)
