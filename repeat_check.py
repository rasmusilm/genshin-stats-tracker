from giftcode_scraper import *
from accounts import accounts
from stats import daily_check_in

"""
    Code for when you want to run daily-checkin and code redemption on startup
"""
if __name__ == '__main__':
    codes = update_codes_html()
    need_redeeming = check_codes(codes)

    for account in accounts:
        if need_redeeming:
            for code in codes:
                redeem_code(code, account.uid, account.ltuid, account.cookie_token)

        reward = daily_check_in(account.ltuid, account.ltoken, account.cookie_token)
