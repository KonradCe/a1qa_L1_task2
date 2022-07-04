import json


def get_chrome_parameters() -> list:
    with open("data/config_data.json") as f:
        j = json.load(f)
        chrome_parameters = [*j["chrome_options"]]
    return chrome_parameters


def extract_nb_of_players(obfuscated_string) -> int:
    return int(obfuscated_string.text.split("\n")[1].replace(",", ""))
