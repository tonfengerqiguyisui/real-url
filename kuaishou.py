# 获取快手直播的真实流媒体地址，默认输出最高画质

import json
import re
import requests


class KuaiShou:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 '
                          '(KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'cookie': 'did=web_'}
        with requests.Session() as s:
            res = s.get('https://m.gifshow.com/fw/live/{}'.format(self.rid), headers=headers)
            livestream = re.search(r'liveStream":(.*),"obfuseData', res.text)
            if livestream:
                livestream = json.loads(livestream.group(1))
                *_, hlsplayurls = livestream['multiResolutionHlsPlayUrls']
                urls, = hlsplayurls['urls']
                url = urls['url']
                return url
            else:
                raise Exception('直播间不存在或未开播')


def get_real_url(rid):
    try:
        ks = KuaiShou(rid)
        return ks.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入快手直播房间地址：\n')
    print(get_real_url(r))
