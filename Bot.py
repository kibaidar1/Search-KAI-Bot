
from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import apiai
import datetime
import json
import logging
import Manager_Database
import Parser_Students

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

COURSE, FAC, GROUP, ANSWER = range(4)
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
    par_stud = Parser_Students.find_student()
    Manager_Database.add_to_db(par_stud)
    print('База данных создана')


def update_db(context):
    print('Начинается обновление базы данных')
    par_stud = Parser_Students.find_student()
    Manager_Database.update_db(par_stud)
    print("База данных обновлена")


def start_comm(update, context):
    print("start")
    # create_db()
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text='Привет, пообщаемся?')
    print(update.message.chat_id)
    global chat_id
    chat_id = update.message.chat_id


def test_comm(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Напиши что-нибудь')
    print(update.message.chat_id)
    global chat_id
    chat_id = update.message.chat_id


def help_comm(update, context):
    print('help')
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text('Пообщайся со мной или можешь попробовать найти кого-нибудь из '
                              'КНИТУ-КАИ - команда "/find"\n'
                              'А с помощью команды "/lists" можешь посмотреть список любой группы КАИ. ')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def finder(arg):
    print('finder')
    if arg.isalpha():
        if len(arg.split()) <= 6:
            students_lst = Manager_Database.get_student(name=arg.lower())
            answer_lst = []
            for i in students_lst:
                answer_lst += [''.join(i[0:3]) + ' ' + i[3].title()]
            if answer_lst:
                return answer_lst
            else:
                return 'К сожалению, нет студента(ки) "%s"(((' \
                       'Можешь пропробовать поискать снова' % arg.title()
        else:
            return 'Кажется, неверный формат имени - слишком много слов.\nПопробуй ещё раз;)'

    elif arg.isdigit():
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
    keyboard = [[fac] for fac in faculties]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text='\n'.join(sum(keyboard, [])))

    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Это список факультетов КАИ, выбери какой-нибудь, '
                                  'чтобы посмотреть список курсов и групп в этом факультете.'
                                  '\nИли используй команду "/cancel" для отмены.',
                             reply_markup=reply_markup)
    return COURSE


def course_comm(update, context):
    print('course')
    message = update.message.text
    if message in faculties:
        group[0] = message[0]
        answer = sorted(set(Manager_Database.get_courses(group[0])))
        keyboard = [i[0] for i in answer]
        global courses
        courses = keyboard
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
    if update.message.text in courses:
        group[1] = update.message.text
        answer = sorted(set(Manager_Database.get_groups(group[0], group[1])))
        keyboard = [[''.join([group[0] + group[1] + i[0]])] for i in answer]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text='\n'.join(sum(keyboard, [])))

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Это писок групп, можешь выбрать одну, чтобы посмотреть список студентов.'
                                      '\nИли используй отмену - "/cancel"',
                                 reply_markup=reply_markup)
        return ANSWER
    elif update.message.text == 'Назад':
        return COURSE
    else:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat_id, text='Выбери что-нибудь из списка')
        return GROUP


def find_comm(update, context):
    print('find')
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text('Напиши ФИО полностью или просто имя человека которого хочешь найти в КАИ. '
                              'Или, если хочешь получить список группы, напиши её номер.')
    return ANSWER


def answer_comm(update, context):
    print('answer')
    answer_lst = finder(update.message.text)
    if isinstance(answer_lst, list):
        max_text = 100  # Максимальное количество строк имён в одном сообщении
        if len(answer_lst) > max_text:
            range_arg = int(len(answer_lst) / max_text)
            for j in range(range_arg):
                print('\n'.join(answer_lst[max_text * j:max_text * (j + 1)]))
                context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
                context.bot.send_message(chat_id=update.message.chat.id,
                                         text='\n'.join(answer_lst[max_text * j:max_text * (j + 1)]),
                                         reply_markup=ReplyKeyboardRemove())
                if (j + 2) > int(len(answer_lst) / max_text):
                    print('\n'.join(answer_lst[max_text * (j + 1):]))
                    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
                    context.bot.send_message(chat_id=update.message.chat.id,
                                             text='\n'.join(answer_lst[max_text * (j + 1):]))
        else:
            context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
            context.bot.send_message(chat_id=update.message.chat.id,
                                     text='\n'.join(answer_lst),
                                     reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    elif isinstance(answer_lst, str):
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(chat_id=update.message.chat.id, text=answer_lst)
        return ANSWER


def cancel(update, context):
    print('cancel')
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text='Поиск отменён', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def text_message(update, context):
    request = apiai.ApiAI('ff6294d116844a5d8921d9c29b508dce').text_request()  # Токен API Dialogflow
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
    token = "797118751:AAGAmqwB5uhCLyLcWUd0mkvMNogMsODl0N0"
    request_kwargs = {
        'proxy_url': 'socks5://111.223.75.178:8888'
    }
    updater = Updater(token=token, request_kwargs=request_kwargs, use_context=True)
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

    # Работы
    job.run_daily(update_db, days=(4,), time=datetime.time(14, 50), name='Updater DB')

    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()
