#from ItChat import itchat
import itchat
#from Common.downloader import Downloader
#import requests
#import certifi


@itchat.msg_register(itchat.content.TEXT)
def print_contect(msg):
    print(msg["Text"])

#D = Downloader()
#results = D('https://login.weixin.qq.com/')
#r = requests.get('https://login.weixin.qq.com/', verify=False)
#r = requests.get('https://amazon.com/', verify=False)
#print(r.status_code)
itchat.auto_login(hotReload=True)
itchat.send("Hello filehelper", toUserName='filehelper')
friends_list = itchat.search_friends()
print(friends_list)
itchat.run()