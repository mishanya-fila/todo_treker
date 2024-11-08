from telebot import formatting

from main import Task

help_msg = f'Команды для работы с ботом:\n' \
           f'- {formatting.hcode("/start")} - начало работы с ботом\n' \
           f'- {formatting.hcode("/help")} - команды для работы с ботом\n' \
           f'- {formatting.hcode("/new_list")} - добавление нового списка задач\n' \
           f'- {formatting.hcode("/show_lists")} - вывод всех списков задач\n' \
           f'- {formatting.hcode("/choose_list")} - выбрать список задач\n' \
           f'- {formatting.hcode("/get_current_list")} - вывод текущего списка задач\n' \
           f'- {formatting.hcode("/rename_list")} - переименование текущего списка задач\n' \
           f'- {formatting.hcode("/remove_list")} - удаление текущего списка задач\n' \
           f'- {formatting.hcode("/new_task")} - создание новой задачи\n' \
           f'- {formatting.hcode("/show_tasks")} - вывод всех задач в выбарнном списке\n' \
           f'- {formatting.hcode("/choose_task")} - выбор задачи в текущем списке\n' \
           f'- {formatting.hcode("/get_current_task")} - вывод выбранной задачи\n' \
           f'- {formatting.hcode("/update_status")} - обновление статуса выбранной задачи\n' \
           f'- {formatting.hcode("/remove_task")} - удаление выбранной задачи\n'
start_msg = f'Привет! Это бот для отслеживания задач.\n' \
            f'Для просмотра доступных команд введите {formatting.hcode("/help")}'
add_new_task_list_msg = 'Введите название нового списка задач'
success_add_new_task_list = 'Новый список задач успешно добавлен'

no_lists = f'Не добавлено ни одного списка задач.\n' \
           f'Добавьте новый список задач командой {formatting.hcode("/new_list")}'


def prepare_show_lists_msg(lists_name: dict.keys):
    show_list_msg = 'Текущие списки задач:\n'
    for i in lists_name:
        show_list_msg += "• " + str(i) + '\n'
    return show_list_msg


choose_list_msg = "Пожалуйста, напишите название списка задач, который хотите выбрать"
success_choose_list = 'Список задач "{}" успешно выбран!'
invalid_choose_list = f'Данный список задач не найден. Убедитесь в правильности написании названия списка. ' \
                      f'Доступные списки можно просмотреть командой {formatting.hcode("/show_lists")}'
rename_message = 'Введите новое название для текущего списка задач'
current_list_not_chosen = f'Список задач не выбран. Список задач можно выбрать командой ' \
                          f'{formatting.hcode("/choose_list")}'
same_names = f'Новое название текущего списка совпадает со старым. ' \
             f'Введите команду {formatting.hcode("/rename_list")} и введите {formatting.hbold("новое")} имя списка задач'
rename_success = 'Название списка успешно обновлено'
get_current_list = f'Текущий список задач: {formatting.hbold("{}")}'
remove_list_msg = f'Вы уверенны, что хотите удалить текущий список задач? Ответьте Да/Нет'
success_remove_list = 'Текущий список задач был успешно удалён'
invalid_remove_list = f'Пожалуйста, введите либо {formatting.hcode("Да")}, либо {formatting.hcode("Нет")}'
invalid_current_list = f'Список задач не выбран. Выберите список задач командой {formatting.hcode("/choose_list")}'
new_task = 'Введите имя новой задачи'
name_new_task = 'Введите имя новой задачи'
success_create_task = 'Задача "{}" успешно добавлена в список "{}"'


def prepare_no_tasks_msg(ls_name):
    msg = f'В список "{ls_name}" не добавлено ни одной задачи.\n' \
          f'Добавить новую задачу можно командой {formatting.hcode("/new_task")}'
    return msg


def prepare_show_tasks_msg(res_list: [Task], key: str):
    msg = f'Текущие задачи в списке "{key}":\n'
    for i in res_list:
        i: Task
        msg += f'•Имя задачи - "{i.name}"; Статус задачи - "{"Выполнено✔" if i.status else "Не выполнено❌"}"\n'
    return msg[:-1]


choose_task = 'Введите имя задачи из списка "{}", которую хотите выбрать'
success_choose_task = 'Задача "{}" успешно выбрана'


def prepare_invalid_name_task_msg(task_name, key):
    return f'Задача "{task_name}" не найдена.\n' \
           f'Просмотреть все задачи в списке "{key}" можно командой {formatting.hcode("/show_tasks")}'


task_not_chosen_msg = f'Задача не выбрана. Выберите задачу командой {formatting.hcode("/choose_task")}'
update_status_msg = 'Статус задачи "{}" обновлён'
get_current_task = 'Текущая задача "{}"'
remove_task_msg = 'Задача была успешно удалена'
echo_message = f'Бот не понимает данного сообщения.\n' \
               f'Воспользуйтесь командой {formatting.hcode("/help")} чтобы увидеть возможности бота'
command_in_text_msg = 'В переданном тексте указано имя команды.\n' \
                      'Пожалуйста, не используйте имена команд в качестве имён задач и имён списков задач!'
