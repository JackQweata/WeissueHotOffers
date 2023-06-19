from modules.channel_object import ChannelObject
from src.OZON.parser_management_ozon import ParserManagementOzon
from src.WB.parser_management_wb import ParserManagementWB
from src.bots.admin.admin_commads import admin_commands_polling


def main():

    ChannelObject.collect_data()
    for channels_dict in ChannelObject.channels_dict.values():
        channels = channels_dict['class']
        type_parser = channels_dict['type']

        if not type_parser or type_parser == 3:
            parser_management_wb = ParserManagementWB(channels)
            parser_management_wb.start()
            channels_dict['thread'] = parser_management_wb

        if type_parser or type_parser == 3:
            parser_management_oznon = ParserManagementOzon(channels)
            parser_management_oznon.start()
            channels_dict['mp'] = parser_management_oznon

    admin_commands_polling()


if __name__ == '__main__':
    main()
