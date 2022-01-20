import unittest
from random import random
from unittest.mock import Mock, patch, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from python_base.chatbot.vk_bot import VkBot


class MyTestCase(unittest.TestCase):
    # RAW_EVENT = {
    #     'type': 'message_new',
    #     'object': {'date': , 'from_id': , 'id': , 'out': , 'peer_id': ,
    #                'text': , 'conversation_message_id': , 'fwd_messages': , 'important': ,
    #                'random_id': , 'attachments': , 'is_hidden': },
    #     'group_id': }

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.RAW_EVENT = None

    def test_run(self):
        count = 5
        events = [{}] * count
        long_poller_mosk = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mosk

        with patch('vk_api.VkApi'):
            with patch('python_base.chatbot.vk_bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = VkBot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call({})
                bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_mock = Mock()

        with patch('vk_api.VkApi'):
            with patch('python_base.chatbot.vk_bot.VkBotLongPoll'):
                bot = VkBot('', '')
                bot.api = Mock()
                bot.api.messages.send = send_mock
                bot.on_event(event)

        send_mock.assert_called_once_with(
                message='Приветствую Вас, Землянин!!',
                random_id=ANY,
                peer_id=event.message.peer_id,
            )


if __name__ == '__main__':
    unittest.main()
