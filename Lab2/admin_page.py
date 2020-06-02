import datetime
from threading import Thread
import logging
import consolemenu
import redis

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

logging.basicConfig(filename='events.log', level=logging.INFO)


class EventListener(Thread):

    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def run(self):
        pubsub = self.connection.pubsub()
        pubsub.subscribe(['users', 'spam'])
        for item in pubsub.listen():
            if item['type'] == 'message':
                message = '\nEVENT: %s | %s' % (item['data'], datetime.datetime.now())
                logging.info(message)


def admin_menu():
    menu = consolemenu.SelectionMenu(['Переглянути користувачів, що онлайн:', 'Отримати рейтинг відправників', 'Отримати рейтинг спамерів'], title=f'{bcolors.BOLD}З поверненням, адміністраторе{bcolors.ENDC}')
    menu.show()
    if menu.is_selected_item_exit():
        exit()
    return menu.selected_option + 1


def main():
    loop = True
    connection = redis.Redis(charset='utf-8', decode_responses=True)
    listener = EventListener(connection)
    listener.setDaemon(True)
    listener.start()

    while loop:
        choice = admin_menu()

        if choice == 1:
            online_users = connection.smembers('online:')
            print(f'{bcolors.WARNING}Онлайн:{bcolors.ENDC}')
            for user in online_users:
                print(user)

        elif choice == 2:
            top_senders_count = int(input(f'{bcolors.OKGREEN}Скільки показати осіб в рейтингу?: {bcolors.ENDC}'))
            senders = connection.zrange('sent:', 0, top_senders_count - 1, desc=True, withscores=True)
            print(f'{bcolors.WARNING}Рейтинг %s відправників{bcolors.ENDC}' % top_senders_count)
            for index, sender in enumerate(senders):
                print(index + 1, ') ', sender[0], ': ', int(sender[1]), 'смс')

        elif choice == 3:
            top_spamers_count = int(input(f'{bcolors.OKGREEN}Скільки показати осіб в рейтингу?: {bcolors.ENDC}'))
            spamers = connection.zrange('spam:', 0, top_spamers_count - 1, desc=True, withscores=True)
            print(f'{bcolors.WARNING}Рейтинг %s спамерів {bcolors.ENDC}' % top_spamers_count)
            for index, spamer in enumerate(spamers):
                print(index + 1, ') ', spamer[0], ': ', int(spamer[1]), 'спам смс')

        input('--Натисніть будь-яку клавішу щоб продовжити--')


if __name__ == '__main__':
    main()
