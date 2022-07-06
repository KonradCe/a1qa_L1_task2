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


def get_wait_time_data():
    with open("data/config_data.json") as f:
        j = json.load(f)

    return int(j["explicit_wait_time"])


def extract_nb_of_players(obfuscated_string) -> int:
    return int(obfuscated_string.text.split("\n")[1].replace(",", ""))


def extract_nb_of_results(obfuscated_string):
    return int(obfuscated_string.split(" ")[0])


# It may look like an overkill, but we do this conversion twice in two different places;
# if somehow the method would change in one place and not the other, the test would fail
def calculate_game_price_from_attribute(raw_attribute_value: str) -> float:
    return int(raw_attribute_value) / 100


# Same situation as with calculate_game_price_from_attribute - simple process, but it happens in two different places,
# and has to be done exactly the same
def create_dict_from_game_attr(
    title: str = None, release_date: str = None, price: float = 0.0
):
    return {
        "title": title,
        "release_date": release_date,
        "price": price,
    }
