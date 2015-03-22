# Project: WeeBullet
# Description: A PushBullet notification plugin for Weechat
# Author: Kevin Romano <kevrom@gmail.com> @kevrom

import weechat as weechat
from pushbullet import Pushbullet

API_Key = None
pb = None

SCRIPT_PROJECT     = 'WeeBullet'
SCRIPT_AUTHOR      = 'kevrom'
SCRIPT_VERSION     = '0.0.1'
SCRIPT_LICENSE     = 'GPL3'
SCRIPT_DESCRIPTION = 'A PushBullet notification plugin for Weechat'

def main():
    weechat.register(SCRIPT_PROJECT, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESCRIPTION, '', '')
    config()

def prnt(p):
    weechat.prnt('', p)

def config():
    try:
        global pb
        API_Key = weechat.config_get_plugin('api_key')
        if API_Key == '':
            raise Exception()
        pb = Pushbullet(API_Key)
        print_hook = weechat.hook_print('', '', '', 1, 'handle_msg', '')
    except:
        weechat.config_set_plugin('api_key', '')
        prnt('Please `/set plugins.var.python.weebullet.api_key <API_KEY>` to use this plugin.')


def handle_msg(data, print_buffer, date, tags, displayed, highlight, prefix, message):
    buffer_type = weechat.buffer_get_string(print_buffer, 'localvar_type')
    buffer_name = weechat.buffer_get_string(print_buffer, 'short_name')

    if buffer_type == 'private':
        push(buffer_name, message)

    elif buffer_type == 'channel' and highlight:
        push('{} @ {}'.format(prefix, buffer_name), message)

    return weechat.WEECHAT_RC_OK

def push(sender, message):
    pb.push_note(sender, message)

if __name__ == '__main__':
    main()
