from hashlib import md5
import string
from time import time
from random import choices
import requests as req

"""
These functions are direct copies of functions in thesadru genshinstats.
"""


def generate_ds() -> str:
    """Creates a new ds for authentication."""
    salt = "6cqshh5dhw73bzxn20oexa9k516chk7s"
    t = int(time())  # current seconds
    r = "".join(choices(string.ascii_letters, k=6))  # 6 random chars
    h = md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest()  # hash and get hex
    return f"{t},{r},{h}"


def recognize_server(uid: int) -> str:
    """Recognizes which server a UID is from."""
    server = {
        "1": "cn_gf01",
        "2": "cn_gf01",
        "5": "cn_qd01",
        "6": "os_usa",
        "7": "os_euro",
        "8": "os_asia",
        "9": "os_cht",
    }.get(str(uid)[0])
    if server:
        return server


"""
========================================================================================
"""

"""
These are reverse engineered from thesaru genshinstats or from the request your browser makes during certain actions.
It is ultimately probably better to use his library, but I wanted to know exactly, what was going on with those requests
and getting the requests actually laid out like this improves the transparency
"""


def get_notes(uid, ltuid, ltoken):
    """
    Function to get the Hoyolab daily notes

    :param uid:
    :param ltuid:
    :param ltoken:
    :return: dictionary: notes data
    """
    USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    headers = {
        # required headers
        "x-rpc-app_version": "1.5.0",
        "x-rpc-client_type": "4",
        "x-rpc-language": "en-us",
        # authentications headers
        "ds": generate_ds(),
        # recommended headers
        "user-agent": USER_AGENT
    }

    url = 'https://bbs-api-os.mihoyo.com/game_record/genshin/api/dailyNote'

    resp = req.get(
        url,
        params=dict(server=recognize_server(uid), role_id=uid),
        headers=headers,
        cookies={'ltuid': ltuid,
                 'ltoken': ltoken})

    return resp.json()["data"]


def get_card(ltuid, ltoken, cookie):
    """
    Get the player card, that displays basic account info

    :param ltuid:
    :param ltoken:
    :param cookie:
    :return:
    """
    url = f"https://bbs-api-os.mihoyo.com/game_record/card/wapi/getGameRecordCard?uid={ltuid}&gids=2"

    headers = {
        'ds': generate_ds(),
        'x-rpc-app_version': '1.5.0',
        'x-rpc-client_type': '4',
        "x-rpc-language": "en-us",
        'Cookie': f'account_id={ltuid}; '
                  f'cookie_token={cookie}; '
                  f'ltoken={ltoken}; '
                  f'ltuid={ltuid};'
    }

    response = req.request("GET", url, headers=headers)

    return response.json()["data"]["list"][0]


def daily_check_in(ltuid, ltoken, cookie):
    """
    Do the daily check in, get rewards
    I was too dumb, to understand how to use thesaru genshinstats equivalent of this, so I made my own.

    :param ltuid:
    :param ltoken:
    :param cookie:
    :return:
    """
    url = f"https://hk4e-api-os.mihoyo.com/event/sol/sign?act_id=e202102251931481"

    headers = {
        'ds': generate_ds(),
        'x-rpc-app_version': '1.5.0',
        'x-rpc-client_type': '4',
        "x-rpc-language": "en-us",
        'Cookie': f'cookie_token={cookie}; '
                  f'ltoken={ltoken}; '
                  f'ltuid={ltuid};'
    }

    status = req.request("POST", url, headers=headers).json()

    url = f"https://hk4e-api-os.mihoyo.com/event/sol/info?act_id=e202102251931481"

    info = req.request("GET", url, headers=headers)

    if info.json()["data"]["is_sign"]:
        return None

    day = info.json()["data"]["total_sign_day"]

    url = f"https://hk4e-api-os.mihoyo.com/event/sol/home?act_id=e202102251931481&lang=en-us"

    reward = req.request("GET", url, headers=headers)

    return reward.json()["data"]["awards"][day]
