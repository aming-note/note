
import requests,re
url = 'http://admin.yc02.com/d/export/member/'
str="200820e3227815ed1756a6b531e7e0d2"
data = {"AgentName":"",
        "UserName":"",
        "SureName":"",
        "Status":0,
        "RegisterStartTime":0,
        "RegisterEndTime":0,
        "LastLoginStartTime":0,
        "LastLoginEndTime":0,
        "LastDepositStartTime":0,
        "LastDepositEndTime":0,
        "Type":"Real",
        "PageNow":1,
        "IsVague":False,
        "Order":"RegisterTsDesc",
        "PageSize":20,
        "VipLevelId":0}

res = requests.post(url,data=data)

ss = res.text
print(ss)