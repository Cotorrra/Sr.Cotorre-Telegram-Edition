import re

import requests
import unidecode

from src.core.utils import is_lvl

pack_data = requests.get('https://es.arkhamdb.com/api/public/packs/').json()


def card_search(query, cards, keyword_func):
    """
    Busca una carta en un conjunto de cartas usando keywords (ej (4E))
    :param query: Nombre de la carta a buscar
    :param cards: Conjunto de cartas
    :param keyword_func: Función para utilizar keywords
    :return:
    """
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    query, pack_query, pack_mode = find_and_extract(query, "[", "]")
    f_cards = cards.copy()

    if sub_text_mode:
        f_cards = [c for c in f_cards if filter_by_subtext(c, sub_query)]

    if keyword_mode:
        f_cards = keyword_func(f_cards, keyword_query)

    if pack_mode:
        pack_search = sorted([pd['name'] for pd in pack_data], key=lambda pd: -hits_in_string(pack_query, pd))
        if len(pack_search) > 0:
            pack_tag = [pd["code"] for pd in pack_data if pd["name"].lower() == pack_search[0].lower()][0]
            f_cards = [c for c in f_cards if c["pack_code"] == pack_tag]

    cards_were_filtered = len(cards) > len(f_cards)

    r_cards = search(query, f_cards)

    if len(r_cards) == 0 \
            or (not cards_were_filtered and len(r_cards) == len(f_cards)) \
            or (cards_were_filtered and len(r_cards) == len(cards)):
        return []
    else:
        return r_cards


def search(query: str, cards: list):
    """
    Realiza una búsqueda según un grupo de palabras dentro del nombre (atributo 'name') de cada carta.
    :param query: Texto para buscar
    :param cards: Cartas
    :return:
    """
    r_cards = sorted(cards, key=lambda card: -hits_in_string(query, card['name']))

    # Sales en los resultados aparte si estas igual de hits con las palabras
    r_cards = [c for c in r_cards if hits_in_string(query, c['name']) > 0]
    return r_cards


def find_by_id(code: str, cards: list):
    """
    Retorna la carta que haga match con el id entregado, de otra forma devuelve False.
    :param code:
    :param cards:
    :return:
    """
    r_cards = [c for c in cards if c['code'] == code]
    try:
        return r_cards[0]
    except IndexError:
        return False


def filter_by_subtext(card: dict, sub: str):
    """
    Retorna True si la carta contiene el subsombre dado, de otra forma False.
    :param card:
    :param sub:
    :return:
    """
    if "subname" in card:
        return hits_in_string(card['subname'], sub) > 0
    else:
        return False


def find_and_extract(string: str, start_s: str, end_s: str):
    """
    Encuentra y extrae un substring delimitado por start_s y end_s, regresando una triada de valores:
    (string base, string extraido, si fue extraido algo)
    :param string:
    :param start_s:
    :param end_s:
    :return:
    """
    if start_s == end_s:
        enable = string.find(start_s) > 0
    else:
        enable = string.__contains__(start_s) and string.__contains__(end_s)
    if enable:
        fst_occ = string.find(start_s) + 1
        snd_occ = string[fst_occ:].find(end_s)
        extract = string[fst_occ: fst_occ + snd_occ]
        base = string.replace(" %s%s%s" % (start_s, extract, end_s), "", 1)
        return base, extract, enable
    else:
        return string, "", enable


def hits_in_string(query: str, find: str, pos_hit=True):
    """
    Retorna la cantidad de veces únicas en las que un string contiene una palabra en el otro.
    Va por palabras.
    :param pos_hit:
    :param find:
    :param query:
    :return:
    """
    hits = 0
    set1 = query.lower().replace("-", " ").split()
    set2 = find.lower().replace("-", " ").split()
    hit_list = []
    for w1 in set1:
        for w2 in set2:
            w1_c = re.sub(r'[^a-z0-9]', '', unidecode.unidecode(w1))
            w2_c = re.sub(r'[^a-z0-9]', '', unidecode.unidecode(w2))
            if w1_c == w2_c and w1_c not in hit_list:
                hits += 2 if len(w1_c) > 3 else 1
                hit_list.append(w1_c)
                if set1.index(w1) == set2.index(w2) and pos_hit and len(w1) > 3:
                    hits += 1
    return hits


def use_all_keywords(cards: list, key_list: str):
    """
    Filtra cartas de jugador según los caracteres del string dado
    :param cards: Lista de cartas
    :param key_list: Argumentos dados
    :return:
    """
    filtered_cards = cards
    for char in key_list.lower():
        if char.isdigit():
            filtered_cards = [c for c in filtered_cards if is_lvl(c, int(char))]
        if char == "e":
            filtered_cards = [c for c in filtered_cards if 'spoiler' in c]
        if char == "b":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'seeker']
        if char == "g":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'guardian']
        if char == "r":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'rogue']
        if char == "s":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'survivor']
        if char == "m":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'mystic']
        if char == "n":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'neutral']
        if char == "u":
            filtered_cards = [c for c in filtered_cards if c['unique']]
        if char == "p":
            filtered_cards = [c for c in filtered_cards if c['permanent']]
        if char == "c":
            filtered_cards = [c for c in filtered_cards if "deck only." in c['real_text']]
        if char == "a":
            filtered_cards = [c for c in filtered_cards if "Advanced." in c['real_text']]

    return filtered_cards
