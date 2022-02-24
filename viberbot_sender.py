from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from connection_sql import Connection


class vibersender():

    def __init__(self, botname, bot_token, username, password):
        self.botname = botname
        self.bot_token = bot_token
        self.username = username
        self.password = password
        self.viber = Api(BotConfiguration(
            name=self.botname,
            avatar='',
            auth_token=self.bot_token
        ))
        print(f' BotName: {self.botname} , BotToken: {self.bot_token}')

    def message_sender(self, viber_id, viber_message):
        if isinstance(viber_id, str):
            print('Viber Class String detected')
            self.viber.send_messages(viber_id, [TextMessage(text=viber_message)])
        elif isinstance(viber_id, list):
            print('Viber Class List detected')
            # get the ids from database
            self.log_in = Connection(self.username, self.password)
            # debugging purposes
            viber_id.append('7')
            viber_id.append('9999')
            #####################
            result = self.log_in.login_viber_ids(viber_id)
            for id in result:
                if id[1] != '':
                    self.viber.send_messages(id[1], [TextMessage(text=viber_message)])
