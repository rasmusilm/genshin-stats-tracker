class Account:

    def __init__(self, uid, ltuid, ltoken, cookie_token):
        self.uid = uid
        self.ltoken = ltoken
        self.ltuid = ltuid
        self.cookie_token = cookie_token

# dummy account credentials, these do not work.
# comprised of your uid (in game), ltuid (get from browser in hoyolab), ltoken (get from browser in hoyolab),
# cookie_token (get from browser in code redemption page)
# for every account you want the code to run on, add an instance of the Account with correct credentials
accounts = [
    # replace this with your account(s) credentials
    Account(
        732277485,
        "172348992",
        "g6J7xlIdgfgrTGHdfsdCvSrUau7WD06fQ7SvQeMYZF",
        "EsdjhskFGDGRsdfsdsmiQN78O0aLhfcxsQIF8m"
    ),
]
