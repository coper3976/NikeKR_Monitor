import requests
from bs4 import BeautifulSoup
import time
import json
from discord_hooks import Webhook
''' --------------------------------- INPUT YOUR CONFIG --------------------------------- '''
MONITOR_DELAY = 5  # second, if your input 10, monitor interval 10 second
discord_webhook = 'https://discord.com/api/webhooks/807895520453853195/CZRNzHeKqeMpCAkP4YNCXX-D5aZ-MEP2VDHPR1VhHfq0_jFaLcqLuzUjhuBExiAU_Kmn'

''' ------------------------------------------------------------------------------------- '''

def send_embed(site, product_name, price, img_link, product_link, size):
    # Create embed to send to webhook
    embed = Webhook(discord_webhook, color=123123)

    # Set author info
    embed.set_author(name=site, icon='https://static-breeze.nike.co.kr/kr/ko_kr/cmsstatic/theme/52/android-icon-36x36.png')

    #embed.set_desc("NEW: " + test)
    embed.add_field(name="Name", value='[{}]({})'.format(product_name, product_link))
    embed.add_field(name="Price", value=price)
    embed.add_field(name="Size", value=size)
    embed.set_thumbnail(img_link)

    # Set footer
    embed.set_footer(text='@hyunwoong', icon='https://static-breeze.nike.co.kr/kr/ko_kr/cmsstatic/theme/52/android-icon-36x36.png', ts=True)

    # Send Discord alert
    embed.post()

def get_link():
    url_list = []
    myheaders = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    resp = requests.get('https://www.nike.com/kr/launch/?type=in-stock&activeDate=date-filter:BEFORE'
                        ,headers=myheaders)
    resp.encoding = ''

    bs = BeautifulSoup(resp.text, 'lxml')
    baseurl = 'https://www.nike.com'

    lis = bs.find_all('li', class_='launch-list-item item-imgwrap instockItem')
    for li in lis:
        url_list.append(baseurl + li.find('a')['href'])
    return url_list


# def get_product_detail(product_url):
#     myheaders = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
#     }
#     resp = requests.get(product_url, headers=myheaders)
#     resp.encoding = ''
#     bs = BeautifulSoup(resp.text, 'lxml')
#     name = bs.find('h1', class_='txt-subtitle').text.strip()
#     price = bs.find('div', class_='price').text.strip()
#     id = bs.find('div', class_='btn-box').div.div['data-product-id']
#     ts = int(time.time()*1000)
#     size_str =  get_size('https://www.nike.com/kr/launch/productSkuInventory?productId={}&_={}'.format(id, ts))
#     img_link = bs.find('ul', id='product-gallery').img['src']
#     return name, price, size_str,img_link


# def get_size(size_url):
#     size_str = ""
#     myheaders = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
#         'x-requested-with': 'XMLHttpRequest',
#         'referer': 'https://www.nike.com/kr/launch/t/women/fw/nike-sportswear/CT1983-700/iizk25/nike-waffle-racer-crater'
#     }
#     resp = requests.get('https://www.nike.com/kr/launch/productSkuInventory?productId=10000036516&_=1612684305760', headers=myheaders)
#     resp.encoding = ''

#     json_data = json.loads(resp.text)
#     for product in json_data['skuPricing']:
#         id = product['externalId'].strip().split(' ')[-1]
#         quantity = product['quantity']
#         if quantity>0 :
#             size_str += "{}({})\n".format(id, quantity)

#     return size_str


# if __name__ == '__main__':

#     # 처음 DB 만들기
#     print(">>> 기존 URL 파싱중...")
#     previous_url_list = get_link()

#     # 5초쉬고
#     print(">>> 모니터링 시작")
#     while True:
#         time.sleep(3)

#         # 변한거 모니터링
#         now_url_list = get_link()
#         now_url_list.append('https://www.nike.com/kr/launch/t/women/fw/nike-sportswear/CT1983-700/iizk25/nike-waffle-racer-crater')

#         for url in now_url_list:
#             if url not in previous_url_list:
#                 print('\t[NEW] : 새롭게 생긴거', url)
#                 previous_url_list.append(url)
#                 # 새로운 상품의 정보 파싱
#                 name, price, size, img_link = get_product_detail(url)
#                 send_embed("Nike", name, price,
#                            img_link, url, size)
#                 print('\t', name, price)
#                 print(size)
