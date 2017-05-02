#from ItChat import itchat
import itchat
#from Common.downloader import Downloader
#import requests
#import certifi

@itchat.msg_register(itchat.content.CARD)
def get_friend(msg):
    if msg['ToUserName'] != 'filehelper': return
    friendStatus = get_friend_status(msg["RecommendInfo"])
    itchat.send(friendStatus['NickName'], 'filehelper')

@itchat.msg_register(itchat.content.TEXT)
def print_contect(msg):
    print(msg.text)
    return msg.text

#D = Downloader()
#results = D('https://login.weixin.qq.com/')
#r = requests.get('https://login.weixin.qq.com/', verify=False)
#r = requests.get('https://amazon.com/', verify=False)
#print(r.status_code)
itchat.auto_login(hotReload=True)
itchat.send("Hello filehelper", toUserName='filehelper')
friends_list = itchat.get_friends()

print(friends_list)
itchat.run()