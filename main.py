import re
import requests


base_url = "https://www.ximalaya.com/album/12914364"
page_num = 13


album_id = base_url.split('/')[4]
print(album_id)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

# media_url = 'https://aod.cos.tx.xmcdn.com/group77/M00/F0/98/wKgO1V5WO4ryTO5WABJ_8esjT9M987.m4a'


def download(media_url, media_name):
    """下载"""
    res = requests.get(url=media_url, headers=headers)

    with open('audio\\' + media_name + '.mp3', mode='wb') as f:
        f.write(res.content)


def media_api(track_id):
    """从网页中获取下载地址"""
    api_url = f'https://www.ximalaya.com/revision/play/v1/audio?id={track_id}&ptype=1'
    res = requests.get(url=api_url, headers=headers)
    src = res.json()['data']['src']
    return src


def get_total_page(page_url):
    res = requests.get(url=page_url, headers=headers)
    audio_info = re.findall('"trackId":(\d+),"isPaid":false,"tag":0,"title":"(.*?)"', res.text)
    print(audio_info)
    for audio_id, title in audio_info:
        url = media_api(audio_id)
        download(url, title)
        print(url, title)


for num in range(0, page_num):
    num += 1
    url = f'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={album_id}&pageNum={num}&sort=0'
    get_total_page(url)
