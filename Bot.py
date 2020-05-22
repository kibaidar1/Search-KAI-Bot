
from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import os
import apiai
import datetime
import json
import logging
import Manager_Database
import Parser_Students

# Ключи
bot_token = os.environ['BOT_TOKEN']
ai_token = os.environ['AI_TOKEN']
PORT = int(os.environ.get('PORT', '8443'))

# Настройка логи
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния дял ConversationHandler
COURSE, FAC, GROUP, ANSWER = range(4)

#  списки для команды LISTS
group = [0, 0, 0, 0]
faculties = ['1 - Институт авиации, наземного транспорта и энергетики',
             '2 - Факультет физико-математический',
             '3 - Институт автоматики и электронного приборостроения',
             '4 - Институт компьютерных технологий и защиты информации',
             '5 - Институт радиоэлектроники и телекоммуникаций',
             '9 - Институт экономики, управления и социальных технологий']
courses = [1, 2, 3, 4, 5, 6]
chat_id = ''


def create_db():
    # Создание БД
    print('Создаётся База данных')
    par_stud = Parser_Students.find_student()  # Список студентов полученных парсингом
    Manager_Database.add_to_db(par_stud)  # Добавления списка в БД
    print('База данных создана')


def update_db(context):
    print('Начинается обновление базы данных')
    par_stud = Parser_Students.find_student()  # Список студентов полученных парсингом
    Manager_Database.update_db(par_stud)  # Обновление БД
    print("База данных обновлена")


def start_comm(update, context):
    # Команда START
    print("start")
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text='Привет, пообщаемся или найдём кого-нибудь?')


def help_comm(update, context):
    # Команда HELP
    print('help')
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text('Пообщайся со мной или можешь попробовать найти кого-нибудь из '
                              'КНИТУ-КАИ - команда "/find"\n'
                              'А с помощью команды "/lists" можешь посмотреть список любой группы КАИ. ')


def error(update, context):
    # Вывод логи
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def finder(arg):
    # Поиск в БД
    print('finder')

    # Поиск по имени
    if arg.replace(' ', '').isalpha():
        # Размер имень не должен превышать 6-ти слов
        if len(arg.split()) <= 6:
            students_lst = Manager_Database.get_student(name=arg.lower())  # Список найденых студентов
            answer_lst = []  # Список для ответа
            for i in students_lst:
                answer_lst += [''.join(i[0:3]) + ' ' + i[3].title()]  # Формирование списка ответа
            if answer_lst:
                return answer_lst
            else:
                return 'К сожалению, нет студента(ки) "%s"(((' \
                       'Можешь пропробовать поискать снова' % arg.title()
        else:
            return 'Кажется, неверный формат имени - слишком много слов.\nПопробуй ещё раз;)'

    # Поиск по номеру группы
    elif arg.replace(' ', '').isdigit():
        if len(list(arg)) == 4:
            students_lst = Manager_Database.get_group_list(group=arg)
            answer_lst = []
            for i in students_lst:
                answer_lst += [i[3].title()]
            if answer_lst:
                return answer_lst
            else:
                return 'К сожалению, нет группы "%s"(((' \
                       'Попробуй написать другую' % arg
        else:
            return 'Кажется, неверный формат группы - номер должен состоять из 4-х цифр.' \
                   '\nПопробуй ещё раз;)'
    else:
        return 'В номере группы не могут быть буквы или знаки,' \
               'а в имени студента не могут быть цифры или знаки ' \
               '\nПопробуй ещё раз;)'


def fac_comm(update, context):
    print('fac')
    keyboard = [[fac] for fac in faculties]  # Кавиатура
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text='\n'.join(sum(keyboard, [])))

    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Это список факультетов КАИ, выбери какой-нибудь, '
                                  'чтобы посмотреть список курсов и групп в этом факультете.'
                                  '\nИли тыкай в "/cancel" для отмены.',
                             reply_markup=reply_markup)
    return COURSE


def course_comm(update, context):
    print('course')
    message = update.message.text

    # Если сообщение есть в списке faculties
    if message in faculties:
        group[0] = message[0]  # Изменение номера факультета на переданное собщение
        answer = sorted(set(Manager_Database.get_courses(group[0])))  # Найденные номера курсов факультета
        keyboard = [i[0] for i in answer]  # Клвиатура
        global courses
        courses = keyboard  # Изменение списка курсов
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text='\n'.join(keyboard))

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Это список курсов факультета, если хочешь посмотреть список групп - '
                                      'выбери нужный курс, если нет - жми на "/cancel"',
                                 reply_markup=reply_markup)
        return GROUP
    else:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text='Выбери что-нибудь из списка')
        return COURSE


def group_comm(update, context):
    print('group')
    # Если сообщение есть в списке courses
    if update.message.text in courses:
        group[1] = update.message.text  # Изменение номера курса
        answer = sorted(
            set(Manager_Database.get_groups(group[0], group[1])))  # Списки групп факультета group[0] и курса group[1]
        keyboard = [[''.join([group[0] + group[1] + i[0]])] for i in answer]  # Клавиатура
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text='\n'.join(sum(keyboard, [])))

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Это писок групп, можешь выбрать одну, чтобы посмотреть список студентов.'
                                      '\nИли используй отмену - "/cancel"',
                                 reply_markup=reply_markup)
        return ANSWER

    else:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text='Выбери что-нибудь из списка')
        return GROUP


def find_comm(update, context):
    # Команда ПОИСК
    print('find')
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text('Напиши ФИО полностью или просто имя человека которого хочешь найти в КАИ. '
                              'Или, если хочешь получить список группы, напиши её номер.'
                              '\nДля отмены ткни в /cancel')
    return ANSWER


def answer_comm(update, context):
    print('answer')
    answer = finder(update.message.text)  # Ответ от поиска

    # Если ответ является списком (список студентов)
    if isinstance(answer, list):
        # Длина сообщения имеет максимум в 4096 символов, поэтом ограничим сообщение в 100 строк
        max_text = 100  # Максимальное количество строк имён в одном сообщении
        if len(answer) > max_text:
            range_answer = int(len(answer) / max_text)  # Количество целых сообщений
            for j in range(range_answer):
                context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
                context.bot.send_message(chat_id=update.message.chat.id,
                                         text='\n'.join(answer[max_text * j:max_text * (j + 1)]),
                                         reply_markup=ReplyKeyboardRemove())

                # Остаточное сообщение, если есть остаток
                if (j + 2) > int(len(answer) / max_text):
                    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
                    context.bot.send_message(chat_id=update.message.chat.id,
                                             text='\n'.join(answer[max_text * (j + 1):]))
        else:
            context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
            context.bot.send_message(chat_id=update.message.chat.id,
                                     text='\n'.join(answer),
                                     reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    # Если ответ является строкой (отрицательный ответ)
    elif isinstance(answer, str):
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat.id, text=answer)
        return ANSWER


def cancel(update, context):
    # Команда CANCEL
    print('cancel')
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text='Поиск отменён', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def text_message(update, context):
    # Ответ на обычные сообщения
    request = apiai.ApiAI(ai_token).text_request()  # Токен API Dialogflow
    request.lang = 'ru'  # Язык запроса
    request.session_id = 'Botegram'  # ID Сессии диалога
    request.query = update.message.text  # Запрос к ИИ с сообщением юзера

    response_json = json.loads(request.getresponse().read().decode('utf-8'))  # Разборка Json
    response = response_json['result']['fulfillment']['speech']  # Получаемый ответ

    if response:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text='Я не понимаю!')


def main():
    updater = Updater(token=bot_token, use_context=True)
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=bot_token)
    dispatcher = updater.dispatcher
    job = updater.job_queue
    print("Bot is running")

    # Хендлеры
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('find', find_comm)],
        states={
            ANSWER: [MessageHandler(Filters.text, answer_comm)]},
        fallbacks=[CommandHandler('cancel', cancel)]))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('lists', fac_comm)],
        states={
            FAC: [MessageHandler(Filters.text, fac_comm)],
            COURSE: [MessageHandler(Filters.text, course_comm)],
            GROUP: [MessageHandler(Filters.text, group_comm)],
            ANSWER: [MessageHandler(Filters.text, answer_comm)]},
        fallbacks=[CommandHandler('cancel', cancel)]))
    dispatcher.add_handler(MessageHandler(Filters.text, text_message))
    dispatcher.add_handler(CommandHandler('start', start_comm))
    dispatcher.add_handler(CommandHandler('help', help_comm))
    dispatcher.add_error_handler(error)

    # Работа по обновлению БД, каждый понеденльник в 3:00 ночи.
    job.run_daily(update_db, days=(6,), time=datetime.time(hour=14, minute=40), name='Updater DB')

    # Начало поиска обновлений
    # updater.start_polling(clean=True)
    updater.bot.set_webhook("https://searcher-telegram-bot.herokuapp.com/" + bot_token)
    # Останавка бота, если были нажаты Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()
