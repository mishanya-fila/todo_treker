from telebot import TeleBot
from telebot import types

import messages
from commands import default_commands
from config.config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)
user_states = {}
current_list = {}
current_task = {}


class Task:
    def __init__(self, name, status=False):
        self.name = name
        self.status = status

    def update_status(self):
        self.status = not self.status


def command_in_text(msg: types.Message):
    if any(['/' + str(i.command) in msg.text for i in default_commands]):
        return True


@bot.message_handler(commands=['start'])
def send_start_message(msg: types.Message):
    if msg.chat.id not in user_states.keys():
        user_states[msg.chat.id] = {}
    bot.send_message(chat_id=msg.chat.id, text=messages.start_msg, parse_mode='HTML')


@bot.message_handler(commands=['help'])
def send_help_message(msg: types.Message):
    bot.send_message(chat_id=msg.chat.id, text=messages.help_msg, parse_mode='HTML')


@bot.message_handler(commands=['new_list'])
def handle_new_list_msg(msg: types.Message):
    message = bot.send_message(chat_id=msg.chat.id, text=messages.add_new_task_list_msg)
    bot.register_next_step_handler(message=message, callback=callback_new_list)


def callback_new_list(msg: types.Message):
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        return
    user_states[msg.chat.id][msg.text] = {}
    bot.send_message(chat_id=msg.chat.id, text=messages.success_add_new_task_list)


@bot.message_handler(commands=['show_lists'])
def show_lists(msg: types.Message):
    if user_states[msg.chat.id] == {}:
        bot.send_message(chat_id=msg.chat.id, text=messages.no_lists, parse_mode='HTML')
        return
    text = messages.prepare_show_lists_msg(user_states[msg.chat.id].keys())
    bot.send_message(chat_id=msg.chat.id, text=text)


@bot.message_handler(commands=['choose_list'])
def choose_list(msg: types.Message):
    if user_states[msg.chat.id] == {}:
        bot.send_message(chat_id=msg.chat.id, text=messages.no_lists, parse_mode='HTML')
        return
    message = bot.send_message(chat_id=msg.chat.id, text=messages.choose_list_msg)
    if current_task.get(msg.chat.id):
        current_task.pop(msg.chat.id)
    bot.register_next_step_handler(message=message, callback=callback_choose_list)


def callback_choose_list(msg: types.Message):
    if msg.text not in user_states[msg.chat.id].keys():
        bot.send_message(chat_id=msg.chat.id, text=messages.invalid_choose_list, parse_mode='HTML')
        return
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        return
    current_list[msg.chat.id] = msg.text
    bot.send_message(chat_id=msg.chat.id, text=messages.success_choose_list.format(msg.text))


@bot.message_handler(commands=['rename_list'])
def rename_list(msg: types.Message):
    if current_list.get(msg.chat.id) is None:
        bot.send_message(chat_id=msg.chat.id, text=messages.current_list_not_chosen, parse_mode='HTML')
        return
    message = bot.send_message(chat_id=msg.chat.id, text=messages.rename_message)
    bot.register_next_step_handler(message=message, callback=rename_callback)


def rename_callback(msg: types.Message):
    if current_list.get(msg.chat.id) == msg.text:
        bot.send_message(chat_id=msg.chat.id, text=messages.same_names, parse_mode='HTML')
        return
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        return
    old_name = current_list[msg.chat.id]
    new_name = msg.text
    current_list[msg.chat.id] = new_name
    user_states[msg.chat.id][new_name] = user_states[msg.chat.id][old_name]
    user_states[msg.chat.id].pop(old_name)
    bot.send_message(chat_id=msg.chat.id, text=messages.rename_success)


@bot.message_handler(commands=['get_current_list'])
def get_current_list(msg: types.Message):
    if current_list.get(msg.chat.id) is None:
        bot.send_message(chat_id=msg.chat.id, text=messages.current_list_not_chosen, parse_mode='HTML')
        return
    bot.send_message(chat_id=msg.chat.id, text=messages.get_current_list.format(current_list[msg.chat.id]),
                     parse_mode='HTML')


@bot.message_handler(commands=['remove_list'])
def remove_list(msg: types.Message):
    if current_list.get(msg.chat.id) is None:
        bot.send_message(chat_id=msg.chat.id, text=messages.current_list_not_chosen, parse_mode='HTML')
        return
    message = bot.send_message(chat_id=msg.chat.id, text=messages.remove_list_msg)
    bot.register_next_step_handler(message=message, callback=callback_remove_list)


def callback_remove_list(msg: types.Message):
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        return
    if msg.text.lower() not in ['да', 'нет']:
        bot.send_message(chat_id=msg.chat.id, text=messages.invalid_remove_list, parse_mode='HTML')
    if msg.text.lower() == 'нет':
        return
    if msg.text.lower() == 'да':
        list_name = current_list[msg.chat.id]
        user_states[msg.chat.id].pop(list_name)
        current_list.pop(msg.chat.id)
        bot.send_message(chat_id=msg.chat.id, text=messages.success_remove_list)


@bot.message_handler(commands=['new_task'])
def create_task(msg: types.Message):
    if current_list.get(msg.chat.id) is None:
        bot.send_message(chat_id=msg.chat.id, text=messages.current_list_not_chosen, parse_mode='HTML')
        return
    message = bot.send_message(chat_id=msg.chat.id, text=messages.new_task)
    bot.register_next_step_handler(message=message, callback=callback_create_task)


def callback_create_task(msg: types.Message):
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        return
    chat_id = msg.chat.id
    cur_list = current_list[chat_id]
    user_states[chat_id][cur_list].setdefault(msg.text, Task(name=msg.text))
    bot.send_message(chat_id=msg.chat.id, text=messages.success_create_task.format(msg.text, cur_list))


@bot.message_handler(commands=['show_tasks'])
def show_tasks(msg: types.Message):
    if current_list.get(msg.chat.id) is None:
        bot.send_message(chat_id=msg.chat.id, text=messages.current_list_not_chosen, parse_mode='HTML')
        return
    cur_ls = current_list[msg.chat.id]
    if not user_states[msg.chat.id][cur_ls]:
        bot.send_message(chat_id=msg.chat.id, text=messages.prepare_no_tasks_msg(cur_ls), parse_mode='HTML')
        return
    task_list: [Task] = user_states[msg.chat.id][cur_ls].values()
    bot.send_message(chat_id=msg.chat.id, text=messages.prepare_show_tasks_msg(task_list, cur_ls))


@bot.message_handler(commands=['choose_task'])
def choose_task(msg: types.Message):
    key = current_list.get(msg.chat.id)
    if key is None:
        bot.send_message(chat_id=msg.chat.id, text=messages.current_list_not_chosen, parse_mode='HTML')
        return
    if not user_states[msg.chat.id][key]:
        bot.send_message(chat_id=msg.chat.id, text=messages.prepare_no_tasks_msg(key), parse_mode='HTML')
        return
    message = bot.send_message(chat_id=msg.chat.id, text=messages.choose_task.format(key))
    bot.register_next_step_handler(message=message, callback=callback_choose_task)


def callback_choose_task(msg: types.Message):
    task_name = msg.text
    cur_ls = current_list.get(msg.chat.id)
    user_lists = [i.lower() for i in user_states[msg.chat.id][cur_ls].keys()]
    if command_in_text(msg):
        bot.send_message(chat_id=msg.chat.id, text=messages.command_in_text_msg)
        return
    if task_name.lower() not in user_lists:
        bot.send_message(chat_id=msg.chat.id, text=messages.prepare_invalid_name_task_msg(task_name, cur_ls),
                         parse_mode='HTML')
        return
    current_task[msg.chat.id] = task_name
    bot.send_message(chat_id=msg.chat.id, text=messages.success_choose_task.format(task_name))


@bot.message_handler(commands=['get_current_task'])
def get_current_task(msg: types.Message):
    if current_task.get(msg.chat.id) is None:
        bot.send_message(chat_id=msg.chat.id, text=messages.task_not_chosen_msg, parse_mode='HTML')
        return
    bot.send_message(chat_id=msg.chat.id, text=messages.get_current_task.format(current_task[msg.chat.id]))


@bot.message_handler(commands=['update_status'])
def update_status(msg: types.Message):
    if current_task.get(msg.chat.id) is None:
        bot.send_message(chat_id=msg.chat.id, text=messages.task_not_chosen_msg, parse_mode='HTML')
        return
    task_name = current_task[msg.chat.id]
    list_name = current_list[msg.chat.id]
    user_states[msg.chat.id][list_name][task_name].update_status()
    bot.send_message(chat_id=msg.chat.id, text=messages.update_status_msg.format(task_name))


@bot.message_handler(commands=['remove_task'])
def remove_task(msg: types.Message):
    if current_task.get(msg.chat.id) is None:
        bot.send_message(chat_id=msg.chat.id, text=messages.task_not_chosen_msg, parse_mode='HTML')
        return

    user_states[msg.chat.id][current_list[msg.chat.id]].pop(current_task[msg.chat.id])
    current_task.pop(msg.chat.id)
    bot.send_message(chat_id=msg.chat.id, text=messages.remove_task_msg)


@bot.message_handler(func=lambda msg: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                           'text', 'location', 'contact', 'sticker'])
def echo_message(msg: types.Message):
    bot.send_message(chat_id=msg.chat.id, text=messages.echo_message, parse_mode='HTML')


if __name__ == '__main__':
    bot.enable_saving_states()
    bot.enable_save_next_step_handlers(delay=1)
    bot.load_next_step_handlers()
    bot.set_my_commands(default_commands)
    bot.infinity_polling(skip_pending=True)
