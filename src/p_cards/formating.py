from src.core.formating import format_name, format_subtext, format_faction, format_number, format_card_text, format_text, \
    faction_order, format_victory, format_illus_pack, create_embed
from src.errata.formating import format_errata_text
from src.p_cards.utils import format_slot, format_skill_icons, format_health_sanity, format_inv_skills, \
    format_sub_text_short
from src.core.utils import format_xp
from src.taboo.formating import format_taboo_text


def format_player_card(c):
    f = {"name": format_name(c),
         "level": format_xp(c),
         "subtext": format_subtext(c),
         "faction": format_faction(c),
         "type": "%s" % c['type_name'],
         "slot": format_slot(c),
         "traits": "%s\n" % c['traits'] if 'traits' in c else "",
         "icons": "%s\n" % format_skill_icons(c) if format_skill_icons(c) != "" else "",
         "costs": "Coste: %s \n" % format_number(c['cost']) if "cost" in c else "",
         "text": "%s \n" % format_card_text(c) if "text" in c else "",
         "flavour": "<i>%s</i>\n\n" % format_text(c['flavor']) if "flavor" in c else "",
         "health_sanity": "%s \n" % format_health_sanity(c) if format_health_sanity(c) != "" else "",
         "taboo_text": format_taboo_text(c['code']),
         "errata_text": format_errata_text(c['code']),
         "victory": format_victory(c),
         }
    m_title = "%(faction)s %(name)s%(subtext)s%(level)s" % f
    m_description = "%(type)s %(slot)s\n" \
                    "%(traits)s" \
                    "%(costs)s" \
                    "%(icons)s\n" \
                    "%(text)s" \
                    "%(victory)s" \
                    "%(health_sanity)s\n" \
                    "%(flavour)s " \
                    "%(errata_text)s" \
                    "%(taboo_text)s" % f
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_inv_card_f(c):
    formater = {"class": format_faction(c),
                "name": format_name(c),
                "subname": format_subtext(c),
                "skills": "%s \n" % format_inv_skills(c),
                "health_sanity": format_text("%s%s\n" % ("[health] %s " % c['health'], "[sanity] %s" % c['sanity'])),
                "ability": "%s \n" % format_card_text(c),
                "traits": "%s\n" % c['traits'],
                "taboo_text": format_taboo_text(c['code']),
                "errata_text": format_errata_text(c['code']),
                "flavour": "<i>%s</i>\n" % c['flavor'] if "flavor" in c else "",
                }

    m_title = "%(class)s %(name)s %(subname)s " % formater
    m_description = "%(skills)s" \
                    "%(traits)s \n" \
                    "%(ability)s" \
                    "%(health_sanity)s \n" \
                    "%(flavour)s" \
                    "%(errata_text)s" \
                    "%(taboo_text)s\n" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_player_card_deck(c, qty=0):
    formater = {"name": c['name'],
                "level": format_xp(c),
                "class": faction_order[c['faction_code']] + format_faction(c),
                "quantity": "x%s" % str(qty) if qty > 1 else "",
                "subname": format_sub_text_short(c)
                }
    text = "%(class)s %(name)s%(subname)s %(level)s %(quantity)s" % formater
    return text


