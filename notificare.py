import weechat
import requests

SCRIPT_NAME = "notificare"

weechat.register(
    SCRIPT_NAME,
    "ClifHouck",
    "0.1",
    "MIT",
    SCRIPT_NAME + ": Send notifications on mentions and private messages."
)

config = {
    'user_token': '',
    'api_token': '',
    'api_url': '',
    'sound': 'magic'
    'api_url': 'https://api.pushover.net/1/messages.json',
}

for option, default_value in config.items():
    weechat_config_value = weechat.config_get_plugin(option)
    if weechat_config_value == '' and config[option] == '':
        weechat.prnt("",
                     weechat.prefix("error") + SCRIPT_NAME +
                     ": Option '%s' not set and no default is provided." %
                        option)
    if weechat_config_value != '':
        config[option] = weechat_config_value


weechat.hook_print("",
        "irc_privmsg", "", 1,
        "handle_mention_or_private_message", "")

def handle_mention_or_private_message(data, buffer, date, tags, displayed,
                                      highlight, prefix, message):
    buffer_type = weechat.buffer_get_string(buffer, "localvar_type")

    if buffer_type == "private":
        send_push_notification(prefix, message)
    elif int(highlight):
        send_push_notification(buffer, message)

    return weechat.WEECHAT_RC_OK


def send_push_notification(origin, message):
    post_data = {
        'token': config['api_token'],
        'user': config['user_token'],
        'message': origin + ": " + message,
        'sound':  config['sound']
    }
    response = requests.post(config['api_url'], data=json.dumps(post_data))
    if response.status_code != 200:
        weechat.prnt("",
                     weechat.prefix("error") + SCRIPT_NAME +
                     "Push notification request failed!")
