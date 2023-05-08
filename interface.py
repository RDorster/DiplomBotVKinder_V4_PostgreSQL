# импорты
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from core import VkTools
from data_store import *
from keyboard import keyboard

import data_store


class BotInterface():

    def __init__(self, comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.params = None
        self.keyboard = keyboard
        print('Бот запущен!')

    def message_send(self, user_id, message, attachment=None, keyboard=None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id(),
                               'keyboard': keyboard
                               }
                              )

    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Приветствую тебя, {self.params["name"]}')
                elif command == 'поиск':
                    creating_database()
                    users = self.api.search_users(self.params)
                    user = users.pop()
                    print(user)

                    # здесь логика для проверки бд
                    # Проверка на наличие пользователей в базе данных

                    # data_store.check(vk_id=user["id"])

                    # check()
                    # if user in data_store.user:
                    #     print(f"{user} уже есть в базе данных")
                    # else:
                    #     insert_data_seen_users()
                        # users.append(seen_user)
                    # print(f"{user} добавлен в базу данных")

                    photos_user = self.api.get_photos(user['id'])

                    attachment = ''
                    for num, photo in enumerate(photos_user):
                        attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                        if num == 2:
                            break
                    self.message_send(event.user_id,
                                      f'Посмотри, это - {user["name"]}',
                                      attachment=attachment
                                      )
                    self.message_send(event.user_id,
                                      f'Ссылка на страницу профиля в VK: https://vk.com/id{user["id"]}')
                    # здесь логика для добавления в бд
                    data_store.insert_data_seen_users(vk_id=user["id"], offset=offset)
                elif command == 'cледующие':
                    continue
                elif command == 'пока':
                    self.message_send(event.user_id, 'пока')
                else:
                    self.message_send(event.user_id, 'команда не опознана')


if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()
