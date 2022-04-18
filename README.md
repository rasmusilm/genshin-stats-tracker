# Gensin stats tracker

Code I wrote for getting the state and stats for my two accounts, and automatically do the daily check-in and redeem giftcodes.

A lot of it is based on the [genshinstats module by thesadru](https://github.com/thesadru/genshinstats)

___

Output of the get_account_info.py code I get with my two accounts (Id details redacted)
~~~sh
Request time - 17:10

Account: **first account** | AR 45 | UID: *********
Days Active: 122 | Characters: 23 | Achievements: 191 | Spiral Abyss: 7-3 |
Current resin: 160/160 | 0 h 0 min
Expenditions: 4/5 | max: 5 | 259 min
Teapot: 592/1200
Daily commissions: 0/4, reward unclaimed



Account: **main account** | AR 56 | UID: *********
Days Active: 301 | Characters: 35 | Achievements: 387 | Spiral Abyss: 8-3 |
Current resin: 101/160 | 7 h 47 min
Expenditions: 5/5 | max: 5 |
Teapot: 1092/2200
Daily commissions: 0/4, reward unclaimed

~~~

Main use for me is to see the running state of the account:
- Resin
- Expedition progress
- Teapot coins
- Whether dailies are done

And do daily check-in and redeem any new giftcodes without having to think about it

I plan to also add an entry for your parametric transformer

___
### How to get it working
___
You will need to put YOUR OWN account credentials into the accounts file into the accounts list. The credentials there currently are invalid. <br/>
- Get uid either from ingame, the giftcode redemption page or from hoyolab
- Get credentials from hoyolab.com
    - go to hoyolab.com 
    - login to your account 
    - press F12 to open inspect mode (aka Developer Tools)
    - go to Application, Cookies, https://www.hoyolab.com. 
    - copy ltuid and ltoken 
    - put them into the Account instance constructor

- Get the cookie-token from Genshin code redemption page
  - go to genshin.hoyoverse.com/en/gift
  - Login to your account
  - press F12 to open inspect mode (aka Developer Tools)
  - go to Application, Cookies, https://genshin.hoyoverse.com
  - copy cookie_token
  - put it into the account constructor for the last value

Sometimes the code redemption page also has your UID among the cookies as account_id