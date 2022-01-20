import random
import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from python_base.chatbot.settings import GROUP_ID, TOKEN
import logging.config

log_config = {
    'version': 1,
    'formatters': {
        'my_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'my_formatter_2': {
            'format': '%(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'my_formatter',
            'filename': 'bot.log',
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'my_formatter_2',
        }
    },
    'loggers': {
        'bot': {
            'handlers': ['file_handler'],
            'level': 'INFO',
        },
    },
}


logging.config.dictConfig(log_config)
log = logging.getLogger("bot")

# stream_hendler = logging.StreamHandler()
# stream_hendler.setFormatter(logging.Formatter('%(levelname)s % (message)s'))
# log.addHandler(stream_hendler)
# file_handler = logging.FileHandler('bot.log')
# file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s % (message)s'))
# log.addHandler(file_handler)
#
# log.setLevel(logging.INFO)
# stream_hendler.setLevel(logging.INFO)
# file_handler.setLevel(logging.INFO)

# log.setLevel(logging.ERROR)
# stream_hendler.setLevel(logging.ERROR)
# file_handler.setLevel(logging.ERROR)

# log.setLevel('DEBUG')
# stream_hendler.setLevel('DEBUG')
# file_handler.setLevel('DEBUG')

# logging.DEBUG
# logging.INFO
# logging.WARNING
# logging.ERROR
# logging.CRITICAL


class VkBot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.user_states = {}

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.info('Возвращаем сообщение')
            self.api.messages.send(
                message='Приветствую Вас!!',
                random_id=random.randint(0, 100000),
                peer_id=event.message.peer_id,
            )
        else:
            log.debug('Я так не умею!')

    def message(self):
        pass


if __name__ == '__main__':
    bot = VkBot(GROUP_ID, TOKEN)
    bot.run()
