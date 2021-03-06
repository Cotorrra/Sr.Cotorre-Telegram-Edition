from src.core.utils import is_lvl


def use_ec_keywords(cards: list, key_list: str):
    """
    Filtra cartas de encuentro según los caracteres del string dado
    :param cards: Lista de cartas
    :param key_list: Argumentos dados
    :return:
    """
    filtered_cards = cards
    for char in key_list.lower():
        if char.isdigit():
            filtered_cards = [c for c in filtered_cards if is_lvl(c, int(char))]
        if char == "e":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "enemy"]
        if char == "a":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "act"]
        if char == "p":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "agenda"]
        if char == "t":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "treachery"]
        if char == "s":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "scenario"]
        if char == "l":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "location"]
        if char == "j":
            filtered_cards = [c for c in filtered_cards if c['type_code'] in ['asset', 'event', 'skill']]
        if char == "m":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == "mythos"]

    return filtered_cards


def format_query_ec(nombre, tipo, subtitulo, pack):
    sub = f" ~{subtitulo}~" if subtitulo else ""
    extra = f" ({tipo})" if 'tipo' else ""
    pack = f" [{pack}]" if 'pack'  else ""
    return nombre + sub + extra + pack
