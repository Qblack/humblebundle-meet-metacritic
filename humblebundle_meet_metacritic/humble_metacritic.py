"""
Small script to retrieve all humblebundle games purchased and add metadata from metacritic
Generates an .html file as output
"""
from humblebundle_meet_metacritic.models.humble_game import HumbleGame
from humblebundle_meet_metacritic.metacritic_scrapper import MetacriticInfo

__author__ = "Dean Oemcke"


def get_game_header_for_print():
    fields = [
        "Icon",
        "Game",
        "Bundle",
        "Type",
        "Link",
        "MC Title",
        "Platform",
        "# Players",
        "Genre",
        "Metascore",
        "Metascore desc",
        "Metascore reviews",
        "Userscore",
        "Userscore desc",
        "Userscore reviews",
        "Summary",
        "Release Date",
        "Rating",
        "Developer",
        "Publisher",
        "Publisher Link",
        "Official Site",
        "Game Link",
    ]
    return fields


def get_game_detail_for_print(hb, metacritic_model):
    hb_fields = [
        hb.icon, hb.human_name, hb.bundle_name, hb.purchase_type, hb.url,
    ]
    if isinstance(metacritic_model, MetacriticInfo):
        metacritic_fields = [
            metacritic_model.title,
            metacritic_model.system,
            metacritic_model.num_players,
            metacritic_model.genres,
            metacritic_model.metascore,
            metacritic_model.metascore_desc,
            metacritic_model.metascore_count,
            metacritic_model.user_score,
            metacritic_model.user_score_desc,
            metacritic_model.user_count,
            metacritic_model.summary,
            metacritic_model.release_date,
            metacritic_model.esrb,
            metacritic_model.developer,
            metacritic_model.publisher,
            metacritic_model.publisher_link,
            metacritic_model.official_site,
            metacritic_model.link,
            metacritic_model.id,
        ]
    else:
        metacritic_fields = ["-"] * 19

    return hb_fields + metacritic_fields


def calculate_purchase_type(machine_name):
    if "_soundtrack" in machine_name:
        return 'soundtrack'
    elif "_android" in machine_name:
        return 'mobile'
    else:
        return 'pc'


def fetch_humble_gameslist(humble_client):
    order_list = humble_client.order_list()
    for order in order_list:
        if not order.subproducts:
            humble_model = HumbleGame(
                order.product.human_name,
                order.product.machine_name,
                order.product.human_name,
                calculate_purchase_type(order.product.machine_name),
                "",
                ""
            )
            yield humble_model
        else:
            for game in order.subproducts:
                humble_model = HumbleGame(
                    game.human_name,
                    game.machine_name,
                    order.product.human_name,
                    calculate_purchase_type(game.machine_name),
                    game.icon,
                    game.url
                )
                yield humble_model
    return


def fetch_metacritic_info(game, mc):
    metacritic_model = MetacriticInfo()
    try:
        results = mc.search(game.human_name, "game")
        match = False
        game_id = False

        # find first match that has a metascore (regardless of platform)
        # if no metascore then just use first result
        if len(results) > 0:
            for result in results:
                if result.metascore and not match:
                    match = result
            if not match:
                match = results[0]
            game_id = match.id

        # once we have a game id look it up in metacritc
        if game_id:
            metacritic_model = mc.get_info(game_id)

    except:
        print('error scraping info for: ', game.human_name)

    return metacritic_model
