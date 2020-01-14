from datetime import datetime

import requests
import config


class BotHandler:

    def __init__(self):
        self.token = config.token
        self.api_url = f"https://api.telegram.org/bot{config.token}/"

    def get_updates(self, timeout=30, offset=None):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(f'{self.api_url}{method}', data=params)
        result_json = response.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        response = requests.post(f'{self.api_url}{method}', data=params)
        return response

    def get_last_updates(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update

    def get_chat_id(update):
        chat_id = update['message']['chat']['id']
        return chat_id


greet_bot = BotHandler()
greetings = ('Hello', 'hi', '', '')
now = datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(offset=new_offset)

        last_update = greet_bot.get_last_updates()

        if last_update is None:
        	continue

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, f'Доброе утро. {last_chat_name}')
            today += 1
        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, f'Добрый день. {last_chat_name}')
        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, f'Добрый вечер. {last_chat_name}')

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
