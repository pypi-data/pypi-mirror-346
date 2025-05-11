import json
import os
import logging
import traceback


def check_if_dir_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        # try:
        #     os.makedirs(directory_path)
        # except OSError as e:
        #     if e.errno != OSError.errno.EXIST:
        #         raise
    # from pathlib import Path
    # Path("/my/directory").mkdir(parents=True, exist_ok=True)


def read_json_file(map_file_name, directory_path=None):
    if directory_path:
        check_if_dir_exists(directory_path)
        map_file_name = directory_path + os.sep + map_file_name
        try:
            a_file = open(map_file_name+".json", "r")
            return json.loads(a_file.read())
        except FileNotFoundError:
            logging.error("File Not Found: {}".format(map_file_name))
            traceback.print_exc()
            # print("Wrong file or file path")
    else:
        return None


def write_json_file(map_file_name, dictionary_data, directory_path=None):
    if directory_path:
        check_if_dir_exists(directory_path)
        map_file_name = directory_path + os.sep + map_file_name

    a_file = open(map_file_name+".json", "w")
    json.dump(dictionary_data, a_file)
    a_file.close()
