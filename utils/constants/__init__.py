from dotenv import load_dotenv
from os import environ

class Bot:
    load_dotenv() # TODO: Trouver comment éviter cette duplication
    name = environ.get("BOTTE_NAME")
    version = environ.get("BOTTE_VERSION")
    token = environ.get("BOTTE_TOKEN")
    prefix = environ.get("BOTTE_PREFIX")

class Guild:
    load_dotenv() # TODO: Trouver comment éviter cette duplication
    id: int = int(environ.get("GUILD_ID"))

class Spotify:
    load_dotenv() # TODO: Trouver comment éviter cette duplication
    client_id = environ.get("SPOTIFY_CLIENT_ID")
    client_secret = environ.get("SPOTIFY_CLIENT_SECRET")

class Lavalink:
    load_dotenv() # TODO: Trouver comment éviter cette duplication
    host = environ.get("LAVALINK_HOST")
    port = int(environ.get("LAVALINK_PORT"))
    password = environ.get("LAVALINK_PASSWORD")
    https = False

class Colors:
    info = 0x00ccb2
    error = 0xf23f42
    warning = 0xffaa00

class Emojis:
    boxing_glove = "\U0001F94A"
    cross_mark = "\u274C"
    game_die = "\U0001F3B2"
    sunny = "\u2600\ufe0f"
    star = "\u2B50"
    christmas_tree = "\U0001F384"
    check = "\u2611"
    envelope = "\U0001F4E8"
    gear = ":gear:"
    trashcan = "<:dustbin:949602736633167882>"
    ok_hand = ":ok_hand:"
    hand_raised = "\U0001F64B"
    upload = "\U0001f4dd"
    snekbox = "\U0001f40d"
    member_join = "<:member_join:942985122846752798>"
    repeat = '🔁'
    warning = '\u26A0\uFE0F'

    # Giveaway
    tada = "\U0001f389"
    # animated_tada = "<a:tada2:869981784610336790>"
    animated_tada = "<a:tada2:968745311327649793>"

    # topgg
    topggemoji = "<:topgg:971639606099464264>"

    number_emojis = {
        1: "\u0031\ufe0f\u20e3",
        2: "\u0032\ufe0f\u20e3",
        3: "\u0033\ufe0f\u20e3",
        4: "\u0034\ufe0f\u20e3",
        5: "\u0035\ufe0f\u20e3",
        6: "\u0036\ufe0f\u20e3",
        7: "\u0037\ufe0f\u20e3",
        8: "\u0038\ufe0f\u20e3",
        9: "\u0039\ufe0f\u20e3",
    }

    confirmation = "\u2705"
    decline = "\u274c"

    x = "\U0001f1fd"
    o = "\U0001f1f4"

    resume = "<:emoji_1:900445170103889980>"
    pause = "<:emoji_2:900445202899140648>"
    loop = "<:emoji_7:900445329982369802>"
    closeConnection = "<a:closeimout:848156958834032650>"

    mute = "<:muted:978168504882716702>"
    halfvolume = "<:halfvolume:978168377069674526>"
    fullvolume = "<:fullvolume:978168177005576283>"
    shuffle = "<:shuffle:978188396755320862>"

    list_emoji = "📜"

    FIRST_EMOJI = "\u23EE"  # [:track_previous:]
    LEFT_EMOJI = "\u2B05"  # [:arrow_left:]
    RIGHT_EMOJI = "\u27A1"  # [:arrow_right:]
    LAST_EMOJI = "\u23ED"  # [:track_next:]

    EMOJI_CODES = {
        "green": {
            "a": "<:a_green:952504070709575710>",
            "b": "<:b_green:952504071737184276>",
            "c": "<:c_green:952504072823521290>",
            "d": "<:d_green:952504073016475709>",
            "e": "<:e_green:952504073842749511>",
            "f": "<:f_green:952504075277205514>",
            "g": "<:g_green:952504077407903744>",
            "h": "<:h_green:952504078011871245>",
            "i": "<:i_green:952504079479894046>",
            "j": "<:j_green:952504080171950120>",
            "k": "<:k_green:952504084571783188>",
            "l": "<:l_green:952504081912582184>",
            "m": "<:m_green:952504086396276787>",
            "n": "<:n_green:952504084408193044>",
            "o": "<:o_green:952504085465141268>",
            "p": "<:p_green:952504085507080213>",
            "q": "<:q_green:952504087272890378>",
            "r": "<:r_green:952504087851728966>",
            "s": "<:s_green:952504311798169600>",
            "t": "<:t_green:952504312498651137>",
            "u": "<:u_green:952504312922255380>",
            "v": "<:v_green:952504313761107988>",
            "w": "<:w_green:952504314843250698>",
            "x": "<:x_green:952504315799543859>",
            "y": "<:y_green:952504316839755816>",
            "z": "<:z_green:952504317770883132>",
        },
        "yellow": {
            "a": "<:a_yellow:952504348628377650>",
            "b": "<:b_yellow:952504349962170378>",
            "c": "<:c_yellow:952504351002341376>",
            "d": "<:d_yellow:952504351421775872>",
            "e": "<:e_yellow:952504352239669308>",
            "f": "<:f_yellow:952504352575209513>",
            "g": "<:g_yellow:952504355418955776>",
            "h": "<:h_yellow:952504357121830912>",
            "i": "<:i_yellow:952504358048759808>",
            "j": "<:j_yellow:952504363253899294>",
            "k": "<:k_yellow:952504363220348938>",
            "l": "<:l_yellow:952504359835541504>",
            "m": "<:m_yellow:952504366668087336>",
            "n": "<:n_yellow:952504363937579028>",
            "o": "<:o_yellow:952504365028085840>",
            "p": "<:p_yellow:952504365996974120>",
            "q": "<:q_yellow:952504368240922635>",
            "r": "<:r_yellow:952504368853319710>",
            "s": "<:s_yellow:952504369453080576>",
            "t": "<:t_yellow:952504370107396096>",
            "u": "<:u_yellow:952504370753318983>",
            "v": "<:v_yellow:952504371327946802>",
            "w": "<:w_yellow:952504372460408853>",
            "x": "<:x_yellow:952504373785813052>",
            "y": "<:y_yellow:952504374876332102>",
            "z": "<:z_yellow:952504375203491842>",
        },
        "gray": {
            "a": "<:a_grey:952503991336574976>",
            "b": "<:b_grey:952503992385175572>",
            "c": "<:c_grey:952503993110777876>",
            "d": "<:d_grey:952503993752498176>",
            "e": "<:e_grey:952503994205495306>",
            "f": "<:f_grey:952503994582966312>",
            "g": "<:g_grey:952503997011492904>",
            "h": "<:h_grey:952503998940860436>",
            "i": "<:i_grey:952504000002031658>",
            "j": "<:j_grey:952504000824090688>",
            "k": "<:k_grey:952504006217986108>",
            "l": "<:l_grey:952504003080650832>",
            "m": "<:m_grey:952504004896784455>",
            "n": "<:n_grey:952504005978906644>",
            "o": "<:o_grey:952504006612250674>",
            "p": "<:p_grey:952504007547564082>",
            "q": "<:q_grey:952504008860377178>",
            "r": "<:r_grey:952504009653108806>",
            "s": "<:s_grey:952504009799917570>",
            "t": "<:t_grey:952504010626195487>",
            "u": "<:u_grey:952504011196616714>",
            "v": "<:v_grey:952504011779616768>",
            "w": "<:w_grey:952504012358451243>",
            "x": "<:x_grey:952504012954013697>",
            "y": "<:y_grey:952504013474123816>",
            "z": "<:z_grey:952504013742571530>",
        },
    }

    # Social
    discord = "<:discord:942984508586725417>"
    youtube = "<:youtube:942984508976795669>"
    github = "<:github:942984509673066568>"
