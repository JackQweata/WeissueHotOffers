from modules.channel_object import ChannelObject
from src.WB.run_parser import start_parse
from src.bots.admin.admin_commads import commands_admin_bot
from utils.run_threading import start_threading


def main():
    ChannelObject.collect_data()
    for channels_dict in ChannelObject.channels_dict.values():
        url, name = channels_dict['class'].url, channels_dict['class'].name
        date_dict = {'target': start_parse, 'args': (url, name,), 'name': name}
        thread = start_threading(date_dict)
        channels_dict['thread'] = thread


if __name__ == '__main__':
    main()
