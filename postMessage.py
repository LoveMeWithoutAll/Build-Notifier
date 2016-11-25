from slacker import Slacker

token = 'put your slack api token'
slack = Slacker(token)

def post(str):
    slack.chat.post_message('#github', str)