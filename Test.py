import Manager_Database
import datetime
# names = ['name bran stark', 'SoName', 'EndName']
group = [['5'], ['5'], ['08']]
# out = []
# for i in names:
#     out.append(group + [i])
# print(out)
# hero = 'hero mir var '
# print(hero.lower())
#

faculties = ['1 - Институт авиации, наземного транспорта и энергетики',
             '2 - Факультет физико-математический',
             '3 - Институт автоматики и электронного приборостроения',
             '4 - Институт компьютерных технологий и защиты информации',
             '5 - Институт радиоэлектроники и телекоммуникаций',
             '9 - Институт экономики, управления и социальных технологий']

print(Manager_Database.count())

# def finder(update, context):
#     print('finder')
#     if update.message.text.isalpha():
#         if len(update.message.text.split()) < 6:
#             name = update.message.text.lower()
#             students_lst = Manager_Database.get_student(name=name)
#             answer_lst = []
#             for i in students_lst:
#                 answer_lst += [''.join(i[0:3]) + ' ' + i[3].title()]
#             # print(answer_lst)
#             if answer_lst:
#                 max_text = 100  # Максимальное количество строк имён в одном сообщении
#                 if len(answer_lst) > max_text:
#                     range_arg = int(len(answer_lst) / max_text)
#                     for j in range(range_arg):
#                         print('\n'.join(answer_lst[max_text * j:max_text * (j + 1)]))
#                         context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#                         context.bot.send_message(chat_id=update.message.chat.id,
#                                                  text='\n'.join(answer_lst[max_text * j:max_text * (j + 1)]))
#                         if (j + 2) > int(len(answer_lst) / max_text):
#                             print('\n'.join(answer_lst[max_text * (j + 1):]))
#                             context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#                             context.bot.send_message(chat_id=update.message.chat.id,
#                                                      text='\n'.join(answer_lst[max_text * (j + 1):]))
#                 else:
#                     context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#                     context.bot.send_message(chat_id=update.message.chat.id, text='\n'.join(answer_lst))
#
#             # answer = '\n'.join(answer_lst)
#             # print(answer)
#             # if answer:
#             #     if len(answer) > 4096:
#             #         for x in range(0, len(answer), answer.find('\n', 4096, 0)):
#             #             context.bot.send_message(chat_id=update.message.chat.id, text=answer[x:x + 4096])
#             #     else:
#             #         context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#             #         context.bot.send_message(chat_id=update.message.chat.id, text=answer)
#             else:
#                 context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#                 context.bot.send_message(chat_id=update.message.chat_id,
#                                          text='К сожалению, нет студента(ки) "%s"(' % name.title())
#
#         else:
#             context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#             context.bot.send_message(chat_id=update.message.chat.id,
#                                      text='Кажется, неверный формат имени - слишком много слов. Попробуй ещё раз;)')
#             return ANSWER
#
#     elif update.message.text.isdigit():
#         if len(list(update.message.text)) == 4:
#             group_num = update.message.text
#             students_lst = Manager_Database.get_group_list(group=group_num)
#             answer_lst = []
#             for i in students_lst:
#                 answer_lst += [i[3].title()]
#             if answer_lst:
#                 context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#                 context.bot.send_message(chat_id=update.message.chat.id, text='\n'.join(answer_lst))
#             else:
#                 context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#                 context.bot.send_message(chat_id=update.message.chat_id,
#                                          text='К сожалению, нет группы "%s"(' % group)
#         else:
#             context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#             context.bot.send_message(chat_id=update.message.chat.id,
#                                      text='Кажется, неверный формат группы - номер должен состоять из 4-х цифр. '
#                                           'Попробуй ещё раз;)')
#             return ANSWER
#     else:
#         context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#         context.bot.send_message(chat_id=update.message.chat.id,
#                                  text='В номере группы не могут быть буквы или знаки, '
#                                       'а в имени студента не могут быть цифры или знаки))). '
#                                       'Попробуй ещё раз;)')
#         return ANSWER
#
#     return ConversationHandler.END

