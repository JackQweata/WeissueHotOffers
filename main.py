from decouple import config
from src.WB.run_parser import start_parse
from src.bots.admin.admin_commads import commands_admin_bot
from utils.run_threading import start_threading


def main():
    active_processes = [
        # {"target": start_parse, "args": ((config("WB_URL_WOMAN_CLOTHES")), ("woman"), )},
        {"target": start_parse, "args": ((config("WB_URL_MEN_CLOTHES")), ("men"), )},
        # {"target": start_parse, "args": ((config("WB_URL_CHILDREN_CLOTHES")), "children",)},
        {"target": commands_admin_bot, "args": ()}

    ]

    start_threading(active_processes)


if __name__ == '__main__':
    main()
