import json

from marshmallow import Schema, fields, post_load
from humblebundle_meet_metacritic.metacritic_scrapper import MetacriticInfo
from humblebundle_meet_metacritic.models.humble_game import HumbleGame


class GameData(object):
    def __init__(self, humble_game: HumbleGame, metacritic_info: MetacriticInfo):
        self.human_name = humble_game.human_name
        self.machine_name = humble_game.machine_name
        self.bundle_name = humble_game.bundle_name
        self.purchase_type = humble_game.purchase_type
        self.icon = humble_game.icon
        self.url = humble_game.url

        self.metacritic_id = metacritic_info.id if metacritic_info else None
        self.title = metacritic_info.title if metacritic_info else None
        self.type = metacritic_info.type if metacritic_info else None
        self.link = metacritic_info.link if metacritic_info else None
        self.boxart = metacritic_info.boxart if metacritic_info else None
        self.system = metacritic_info.system if metacritic_info else None
        self.publisher = metacritic_info.publisher if metacritic_info else None
        self.publisher_link = metacritic_info.publisher_link if metacritic_info else None
        self.release_date = metacritic_info.release_date if metacritic_info else None
        self.metascore = metacritic_info.metascore if metacritic_info else None
        self.metascore_count = metacritic_info.metascore_count if metacritic_info else None
        self.metascore_desc = metacritic_info.metascore_desc if metacritic_info else None
        self.user_score = metacritic_info.user_score if metacritic_info else None
        self.user_count = metacritic_info.user_count if metacritic_info else None
        self.user_score_desc = metacritic_info.user_score_desc if metacritic_info else None
        self.summary = metacritic_info.summary if metacritic_info else None
        self.esrb = metacritic_info.esrb if metacritic_info else None
        self.official_site = metacritic_info.official_site if metacritic_info else None
        self.developer = metacritic_info.developer if metacritic_info else None
        self.genres = metacritic_info.genres if metacritic_info else None
        self.num_players = metacritic_info.num_players if metacritic_info else None
        self.esrb_reason = metacritic_info.esrb_reason if metacritic_info else None
        self.sound = metacritic_info.sound if metacritic_info else None
        self.connectivity = metacritic_info.connectivity if metacritic_info else None
        self.resolution = metacritic_info.resolution if metacritic_info else None
        self.num_online = metacritic_info.num_online if metacritic_info else None
        self.customization = metacritic_info.customization if metacritic_info else None

    def __repr__(self):
        return json.dumps({
            'human_name': self.human_name,
            'machine_name': self.machine_name,
            'bundle_name': self.bundle_name,
            'purchase_type': self.purchase_type,
            'icon': self.icon,
            'url': self.url,
            'metacritic_id': self.metacritic_id,
            'title': self.title,
            'type': self.type,
            'link': self.link,
            'boxart': self.boxart,
            'system': self.system,
            'publisher': self.publisher,
            'publisher_link': self.publisher_link,
            'release_date': self.release_date,
            'metascore': self.metascore,
            'metascore_count': self.metascore_count,
            'metascore_desc': self.metascore_desc,
            'user_score': self.user_score,
            'user_count': self.user_count,
            'user_score_desc': self.user_score_desc,
            'summary': self.summary,
            'esrb': self.esrb,
            'official_site': self.official_site,
            'developer': self.developer,
            'genres': self.genres,
            'num_players': self.num_players,
            'esrb_reason': self.esrb_reason,
            'sound': self.sound,
            'connectivity': self.connectivity,
            'resolution': self.resolution,
            'num_online': self.num_online,
            'customization': self.customization
        })

    def create_html(self):
        html = '''
        <div class="row">
            <div class="col col-md-2 offset-md-1">
                <h4>{human_name}</h4>
                <a href='{game_link}'>
                    <img src='{icon}'/>
                </a>
            </div>
            <div class="col col-md-1">
                <h4>Genre</h4>{genres}
            </div>
            <div class="col col-md-1">
                <h4>Numbers</h4>
                <a href="{meta_link}">MetaScore</a>: <span style="color:#328A{metascore}">{metascore}</span>
                <br>
                <span class="font-weight-bold">Userscore:</span> {user_score}
                <br>
                <span class="font-weight-bold">#Players:</span> {num_players}
            </div>
            <div class="col col-5">
                <h4>Summary</h4>
                {summary}
            </div>
        </div>
        '''.format(
            human_name=self.human_name,
            icon=self.icon,
            genres=self.genres,
            game_link=self.url,
            meta_link=self.link,
            metascore=self.metascore,
            user_score=self.user_score,
            num_players=self.num_players,
            summary=self.summary,

        )
        return html



class GameDataSchema(Schema):
    human_name = fields.Str()
    machine_name = fields.Str()
    bundle_name = fields.Str()
    purchase_type = fields.Str()
    icon = fields.Str()
    url = fields.Str()
    metacritic_id = fields.Int()
    title = fields.Str()
    type = fields.Str()
    link = fields.Str()
    boxart = fields.Str()
    system = fields.Str()
    publisher = fields.Str()
    publisher_link = fields.Str()
    release_date = fields.Str()
    metascore = fields.Int()
    metascore_count = fields.Int()
    metascore_desc = fields.Str()
    user_score = fields.Int()
    user_count = fields.Int()
    user_score_desc = fields.Str()
    summary = fields.Str()
    esrb = fields.Str()
    official_site = fields.Str()
    developer = fields.Str()
    genres = fields.Str()
    num_players = fields.Int()
    esrb_reason = fields.Str()
    sound = fields.Str()
    connectivity = fields.Str()
    resolution = fields.Str()
    num_online = fields.Str()
    customization = fields.Str()

    @post_load
    def make_user(self, data):
        return GameData(**data)