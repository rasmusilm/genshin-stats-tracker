import requests
import re
from stats import recognize_server
from deprecation import deprecated


@deprecated(
    details="The formatting of new codes on the page is different from time to time, the function is too unreliable")
def update_codes():
    """
        A scraper for giftcodes from the Pockettactics article, that they update with new codes
    """
    page = requests.get("https://www.pockettactics.com/genshin-impact/codes").text

    stripped = re.sub('<[^<]+?>', '', page)
    stripped = re.sub(r" {2,}", '', stripped)
    codes_cleaned = []
    try:
        codes = stripped.split("codes:\n")[1].split("\nActive codes:")[0]

        for codeline in codes.split("\n"):
            for code in codeline.split("&ndash;"):
                code = code.strip()
                if code.upper() == code and len(code) > 0:
                    codes_cleaned.append(code)
    except:
        try:
            codes = stripped.split("Active codes:\n")[1].split("(this code works periodically)")[0]
            for codeline in codes.split("\n"):
                for code in codeline.split("&ndash;"):
                    code = code.strip()
                    if code.upper() == code and len(code) > 0:
                        codes_cleaned.append(code)
        except:
            pass
        print("no codes on the page")

    return codes_cleaned


def update_codes_html():
    """
        A scraper for giftcodes from the Pockettactics article, that they update with new codes
        Checks more thoroughly to minimize the possibility of missing new codes
    """
    page = requests.get("https://www.pockettactics.com/genshin-impact/codes").text
    if "<h2>Genshin Impact codes</h2>" in page:
        page = page.split("<h2>Genshin Impact codes</h2>")[1]
        page = page.split("<h2>How do I redeem Genshin Impact codes?</h2>")[0]
    pagelines = page.split("\n")
    possible_codes = []
    for line in pagelines:
        if "new" in line.lower() or "primogem" in line.lower() or "primogems" in line.lower():
            possible_codes.append(line)
    codes = find_from_possible_codes(possible_codes)
    return codes


def find_from_possible_codes(possible_codes):
    """
        Tries to read out the codes from the lines that were marked as possible codes
    """
    codes = []
    for line in possible_codes:
        # the codes are usually in <strong> tags, so removes the tags and splits the line at those tags
        text = line.split("strong>")[1]
        # cleans up the line from all the html remnants to be left with the code
        code = re.sub('<[^<]+?', '', text)
        codes.append(code)
    return codes


def redeem_code(code: str, uid: int, account_id: str, cookie_token: str):
    url = f"https://sg-hk4e-api.mihoyo.com/common/apicdkey/api/webExchangeCdkey?uid={uid}&region=os_euro&lang=en&cdkey={code}&game_biz=hk4e_global"
    payload = {}
    headers = {
        'Host': 'hk4e-api-os.mihoyo.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://genshin.mihoyo.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://genshin.mihoyo.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en,et;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'Cookie': f'_MHYUUID=cac753d0-06f1-474f-873f-67bffd1cae51; _ga_FZJK05VBBV=GS1.1.1635541647.1.1.1635541723.0; _ga_6ZT27XS0C9=GS1.1.1636234567.4.1.1636235665.0; UM_distinctid=17d0188a1f070b-0f334ca4e05565-561a1053-144000-17d0188a1f1a53; mi18nLang=en-us; _ga_88EC1VG6YY=GS1.1.1637539484.5.0.1637539484.0; _ga_54PBK3QDF4=GS1.1.1643727725.2.0.1643727732.0; _ga_E6T63X3GHE=GS1.1.1643922928.3.1.1643923045.0; _gaexp=GAX1.2.RCLud6nhTGOoinjzVuh60g.19105.0; _gcl_au=1.1.1661134152.1644069785; _gcl_aw=GCL.1644069785.Cj0KCQiA3fiPBhCCARIsAFQ8QzXTLuyYuXl1PATyoN3JebXUOqRigHFGN32wLspZg868hLzwJ4vPqTQaAn61EALw_wcB; _gid=GA1.2.1930718610.1644069785; _gac_UA-115635327-41=1.1644069785.Cj0KCQiA3fiPBhCCARIsAFQ8QzXTLuyYuXl1PATyoN3JebXUOqRigHFGN32wLspZg868hLzwJ4vPqTQaAn61EALw_wcB; _ga=GA1.2.206046817.1635541647; _ga_B9G6ZV6QNR=GS1.1.1644070952.11.1.1644071264.0; cookie_token_v2={cookie_token}; account_id_v2={account_id};'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def check_codes(codes):
    """
        Compares found codes to already known codes and decides, whether you should try to redeem them
        Updates the know codes file
    """
    answer = False

    try:
        with open("codes.txt", "r+") as codefile:
            newcodes = []
            oldcodes = [i.strip() for i in codefile]
            for code in codes:
                if code in oldcodes:
                    continue
                else:
                    answer = True
                    newcodes.append(code + "\n")

            codefile.writelines(newcodes)
    except:
        # update with the correct absolute path to the file, so you can run it from console in any folder
        with open("%homepath%/genshin_stats_track/gicheck/codes.txt", "r+") as codefile:
            newcodes = []
            oldcodes = [i.strip() for i in codefile]
            for code in codes:
                if code in oldcodes:
                    continue
                else:
                    answer = True
                    newcodes.append(code + "\n")

            codefile.writelines(newcodes)

    return answer


if __name__ == "__main__":
    res = check_codes(update_codes_html())
    print(res)
