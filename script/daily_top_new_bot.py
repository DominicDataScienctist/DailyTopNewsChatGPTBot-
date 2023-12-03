import os
import yaml
import argparse

from news.news_scraper import running_spider
from chat.bot import bot, get_q_and_a


def main(config, parse_new_data, to_activate_chatbot):
    with open(os.path.join(os.getcwd(), f"config/{config}"), "r") as stream:
        try:
            env_variables = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    if parse_new_data:
        running_spider()
    if to_activate_chatbot:
        api_type = env_variables['api_type']
        api_version = env_variables['api_version']
        openai_api_base = env_variables['api_base']
        openai_api_key = env_variables['api_key']
        qa = get_q_and_a(api_type=api_type, openai_api_key=openai_api_key, openai_api_base=openai_api_base,
                         openai_api_version=api_version)
        bot(qa)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=False, default="env.yaml", type=str,
                    help="name config file")
    ap.add_argument("-p", "--parse", required=False, default=False, action='store_true',
                    help="to parse new data")
    ap.add_argument("-b", "--bot", required=True, default=False, action='store_true',
                    help="to activate chatbot")
    args = ap.parse_args()
    config = args.config
    parse_new_data = args.parse
    to_activate_chatbot = args.bot
    main(config, parse_new_data, to_activate_chatbot)
