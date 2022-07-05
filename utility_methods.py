import json


def get_chrome_parameters_data() -> list:
    with open("data/config_data.json") as f:
        j = json.load(f)
        chrome_parameters = [*j["chrome_options"]]
    return chrome_parameters


def get_filter_checkboxes_data() -> dict:
    with open("data/test_data.json") as f:
        j = json.load(f)

    return j["filter_checkbox_data_values"]


def extract_nb_of_players(obfuscated_string) -> int:
    return int(obfuscated_string.text.split("\n")[1].replace(",", ""))


def extract_nb_of_results(obfuscated_string):
    return int(obfuscated_string.split(" ")[0])
