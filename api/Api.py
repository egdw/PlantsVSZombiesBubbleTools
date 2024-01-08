import time

import requests


# 发送多条弹幕
def send_multi_bubble(msgs):
    if msgs is not None and len(msgs) > 0:
        send_msg = []
        for msg in msgs:
            send_msg.append(msg)
            if len(send_msg) == 3:
                sends = ""
                for send in send_msg:
                    sends = sends + send + " "
                print(sends)
                send_bubble(sends)
                time.sleep(1)  # 延时发送
                send_msg.clear()
        sends = ""
        for send in send_msg:
            sends = sends + send + " "
        send_bubble(sends)
        time.sleep(1)
        send_msg.clear()


# 发送单条弹幕
def send_bubble(msg):
    url = 'https://api.live.bilibili.com/msg/send'  # 这个是B站的弹幕，发送API接口

    header = {  # 构造请求头,这里只放一个cookie就可以了
        'Cookie': "buvid3=216C0907-54DE-6FF1-D137-C19D07C3BA8179209infoc; b_nut=1693902579; _uuid=D17C667B-1668-11A3-4727-1D2FBD47AAD179804infoc; buvid4=53D6418E-4D6E-7472-FE18-F48E6942BE3179926-023090516-Rg%2BsQUYYo8R7ZS3yMvXE4g%3D%3D; rpdid=|(umRRlRR~~R0J'uYmJm|kl)|; header_theme_version=CLOSE; hit-new-style-dyn=1; hit-dyn-v2=1; buvid_fp_plain=undefined; DedeUserID=170510265; DedeUserID__ckMd5=838788686ef1243b; enable_web_push=DISABLE; CURRENT_FNVAL=4048; bp_article_offset_170510265=879385701963005956; CURRENT_QUALITY=0; fingerprint=f4b6b20057d68d466b3b99aadf73753c; buvid_fp=f4b6b20057d68d466b3b99aadf73753c; SESSDATA=2680a0da%2C1719975047%2Cac456%2A12CjBVX6VO1B9CQF2tZIZaim4DoeALchN2adxgkW4KHH0kM7mgMRXNrSGJ1okAF1-0aO0SVm5tLWdmWENTOUN2VVl3LUVwcTJTR29QVlRrZ3pFMmNDVDAtdllvZkZZMHFUX0ZJbXk5MWFvUEV4dkV3b003ZlNhelJYWXRsZElYMEVuYTlEN3RQNjlBIIEC; bili_jct=8a3b28c7c53b8790cbcfbcf17bcf3d5c; sid=8uthohmr; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDQ2ODIyNTksImlhdCI6MTcwNDQyMjk5OSwicGx0IjotMX0.guGDstvh4uBOBHCc6fPE5kQlaVuC_g6dwU3UOO1UL10; bili_ticket_expires=1704682199; home_feed_column=5; browser_resolution=3127-1110; bp_video_offset_170510265=883760929293991984; share_source_origin=bili_message; LIVE_BUVID=AUTO1917046073232684; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1704607335; bsource=search_google; b_lsid=983EDE59_18CE3114D49; PVID=2; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1704619147",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    data = {  # 构造请求数据
        'bubble': '0',
        'msg': msg,
        'color': '16777215',
        'mode': '1',
        'fontsize': '25',
        'rnd': '1704618670',
        'roomid': '2471895',
        'room_type': 0,
        'jumpfrom': 0,
        'reply_mid': 0,
        'reply_attr': 0,
        'replay_dmid': "",
        'csrf': '8a3b28c7c53b8790cbcfbcf17bcf3d5c',
        'csrf_token': '8a3b28c7c53b8790cbcfbcf17bcf3d5c'
    }

    result = requests.post(url=url, headers=header, data=data).text  # 发送弹幕
    if "\"code\":0" in result:
        # print("send ok")
        pass
    else:
        print("send fail", result)
