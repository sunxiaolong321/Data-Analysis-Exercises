import configparser
import os
import pickle

from analysis_data import format_date
from spider import require_data


def read_config(section, key):
    config = configparser.ConfigParser()
    config.read(r'./.vscode/config.conf')
    return config.get(section, key)


def save_local(datat, path):
    with open(path, 'wb') as f:
        pickle.dump(datat, f)


def run():
    url = read_config('config', 'url')
    page = int(read_config('config', 'page'))
    count_movie = int(read_config('config', 'count_movie'))
    path = read_config('path', 'path')
    new_path = os.getcwd()+path
    # print(new_path)
    if not os.path.exists(new_path) or not os.path.getsize(new_path):
        data = require_data(url, count_movie, count_movie//page)
        save_local(data, new_path)
    else:
        with open(new_path, 'rb') as f:
            data = pickle.load(f)
    # print(data)
    chart_path = os.getcwd()+read_config('path', 'chart_path')
    format_date(data, chart_path)


if __name__ == "__main__":
    run()