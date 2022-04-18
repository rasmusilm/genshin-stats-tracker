from giftcode_scraper import *
from stats import *
import time
from accounts import accounts

"""
    This is a console app to call all the different functions and format the data from those nicely
    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    this code does not run until you update the accounts file with correct credentials
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
"""


def calculate_expeditions(expeditions):
    """
    Extracts expedition info and calculates the and time of all expeditions
    """
    finished = 0
    ongoing = 0
    total = len(expeditions)
    ongoing_time = [0]
    for expedition in expeditions:
        if expedition["status"] == 'Ongoing':
            ongoing += 1
            ongoing_time.append(int(expedition['remained_time']))
        else:
            finished += 1
    return {"finished": finished, "ongoing": ongoing, "total": total, "end": max(ongoing_time)}


def calculate_tasks(note_info):
    fin = note_info['finished_task_num']
    total = note_info['total_task_num']
    claim = note_info['is_extra_task_reward_received']
    return {fin, total, claim}

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#   !!!!!!!!!!!!!!!!!!!!!!!!!!!!
#    !!!!!!!!!!!!!!!!!!!!!!!!!!
#     !!!!!!!!!!!!!!!!!!!!!!!!
#      !!!!!!!!!!!!!!!!!!!!!!
#       !!!!!!!!!!!!!!!!!!!!
#        !!!!!!!!!!!!!!!!!!
#         !!!!!!!!!!!!!!!!
#          !!!!!!!!!!!!!!
#           !!!!!!!!!!!!
#            !!!!!!!!!!
#             !!!!!!!!
#              !!!!!!
#               !!!!
#                !!
# this code does not run until you update the accounts file with correct credentials
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if __name__ == "__main__":

    t = time.localtime(time.time())

    print(f"Request time - {t.tm_hour:02}:{t.tm_min:02}\n")

    codes = update_codes_html()

    redeem = check_codes(codes)

    for account in accounts:
        # get basic account info
        record = get_card(account.ltuid, account.ltoken, account.cookie_token)
        print(f"Account: {record['nickname']} | AR {record['level']} | UID: {record['game_role_id']}")
        other = ""
        data = record['data']
        for info in data:
            other += info['name']
            other += ": "
            other += info['value']
            other += " | "
        # days active, number of characters, completed achievement count, current spiral abyss level
        print(other)
        notes = get_notes(account.uid, account.ltuid, account.ltoken)
        expedition_inf = calculate_expeditions(notes["expeditions"])
        timer = int(int(notes['resin_recovery_time']) / 60)
        print(f"Current resin: {notes['current_resin']}/{notes['max_resin']} | {timer // 60} h {timer % 60} min")
        print(
            # expeditions - finished expeditions out of sent out expeditions | maximum expeditions that can be sent out
            f"Expenditions: {expedition_inf['finished']}/{expedition_inf['total']} | max: {notes['max_expedition_num']} | "
            # amount of time till all epeditions have finished
            f"{expedition_inf['end'] // 60 if expedition_inf['finished'] - expedition_inf['total'] < 0 else ''} "
            f"{'min' if expedition_inf['finished'] - expedition_inf['total'] < 0 else ''}")
        # coins in your teapot
        print(f"Teapot: {notes['current_home_coin']}/{notes['max_home_coin']}")

        # Show how many daily commissions you have done and whether you have claimed the reward
        if not notes['is_extra_task_reward_received']:
            print(f'Daily commissions: {notes["finished_task_num"]}/{notes["total_task_num"]}, reward unclaimed')
        else:
            print("Dailies done!")

        # do Hoyolab daily check-in, if already claimed, do nothing
        reward = daily_check_in(account.ltuid, account.ltoken, account.cookie_token)
        if reward is not None:
            print(f"Claimed daily reward - {reward['cnt']}x {reward['name']}")

        if accounts.index(account) != len(accounts) - 1:
            print("\n\n")

    # redeem any new codes found, for all accounts
    if redeem:
        print(f"found {len(codes)} new codes, redeeming for {len(codes) * 5 + 5} seconds")
        for account in accounts:
            for code in codes:
                result = redeem_code(code, account.uid, account.ltuid, account.cookie_token)
                if result['data'] is not None:
                    print(f"Redeemed {code}")
            time.sleep(5.1)
    # press enter to end the program
    # the point of that is for running the program in a separate window, so it doesn't close it when it finishes
    input("")
