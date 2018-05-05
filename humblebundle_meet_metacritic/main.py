from requests.cookies import cookiejar_from_dict

import humblebundle

import humblebundle_meet_metacritic.humble_metacritic as hm
from humblebundle_meet_metacritic.metacritic_scrapper import Metacritic, MetacriticInfo
from humblebundle_meet_metacritic import html_table_manager as table
from humblebundle_meet_metacritic.models.game_data import GameData


def main(cookie):
    # Humble login with username/password was removed since the captcha was not worth bypassing
    client = humblebundle.HumbleApi()
    cookies = {c.split('=')[0]: c.split('=')[1] for c in cookie.split(';')}
    client.session.cookies = cookiejar_from_dict(cookies)
    game_list = hm.fetch_humble_gameslist(client)
    with open('gamelist.html', 'w') as output, open('game_output.txt', 'w') as game_out, \
            open('gamelist2.html', 'w') as out2:
        header_items = hm.get_game_header_for_print()
        output.write(table.generate_table_header(header_items))
        # fetch metadata for each game from metacritic and write out to file as we go
        mc = Metacritic()
        for game in game_list:
            print(game.human_name, "...")
            if game.purchase_type == 'soundtrack':
                metacritic_model = MetacriticInfo()
            else:
                metacritic_model = hm.fetch_metacritic_info(game, mc)

            if 'toy odyssey'.lower() in game.human_name.lower():
                pass
            game_data = GameData(game, metacritic_model)
            print(game_data, file=game_out)
            print(game_data.create_html(), file=out2)
            # print out game to file
            game.url = "<a href='{0}'>{0}</a>".format(game.url)
            game.icon = "<img src='{}' />".format(game.icon)

            detailed_items = hm.get_game_detail_for_print(game, metacritic_model)
            # print detailItems
            output.write(table.generate_table_row(detailed_items))
            if metacritic_model:
                output.write(table.generate_table_row_sumamry(metacritic_model.summary))

        # print out html footer
        output.write(table.generate_table_footer())


if __name__ == '__main__':
    COOKIE = r'Put cookie here'
    main(COOKIE)
