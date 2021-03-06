import json
import os

import requests

from src.core.formating import format_text


def load_from_repo(file_src):
    try:
        with open(file_src, "r", encoding='utf-8') as pack:
            info = json.load(pack)
    except FileNotFoundError as e:
        # Get the file from and download it to
        url = f"https://raw.githubusercontent.com/Cotorrra/Sr.Cotorre-Data/main/{file_src}"
        req = requests.get(url)
        path = split_files(file_src)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(file_src, 'w', encoding='utf-8') as pack:
            pack.write(req.text)

        info = json.loads(req.text)

    return info


def split_files(src: str):
    splits = src.split("/")
    rest = ""
    for a in splits[:-1]:
        rest += f"{a}/"
    return rest


def is_lvl(card: dict, lvl: int):
    """
    Equipara el nivel de una carta con el numero dado, si no tiene nivel, se equipara con 0.
    :param card: carta
    :param lvl: nivel
    :return:
    """
    if 'xp' in card:
        return card['xp'] == lvl
    else:
        return 0 == lvl


def get_qty(deck, card_id):
    for c_id, qty in deck['slots'].items():
        if c_id == card_id:
            return qty
    return 0


def has_trait(card, trait):
    try:
        traits = card['real_traits'].lower().split()
        return "%s." % trait in traits

    except KeyError:
        return False


def make_str_from_args(args):
    text = ""
    for a in args:
        text += f"{a} "

    return text[:-1]


def get_title(c):
    text = ""
    if 'faction_code' in c:
        text += format_text("[%s]" % c['faction_code'])
    text += c['name']
    text += format_xp(c)
    return text


def format_xp(c):
    if "xp" in c:
        if c['xp'] == 0:
            text = ""
        elif c['exceptional']:
            text = " (%sE)" % c['xp']
        else:
            text = " (%s)" % c['xp']
    else:
        text = ""
    return text
