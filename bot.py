#-*-encoding:utf8:-*-
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from discord_hooks import Webhook
import json
import urllib3
urllib3.disable_warnings()

# 디스코드 
def send_embed(site, product_name, price, img_link, product_link, size):
    # Create embed to send to webhook
    embed = Webhook(discord_webhook, color=123123)

    # Set author info
    embed.set_author(name=site, icon='https://static-breeze.nike.co.kr/kr/ko_kr/cmsstatic/theme/52/android-icon-36x36.png')

    #embed.set_desc("NEW: " + test)
    embed.add_field(name=" ", value='[{}]({})'.format(product_name, product_link))
    embed.add_field(name="가격", value=price)
    embed.add_field(name="사이즈", value=size)
    embed.set_thumbnail(img_link)

    # Set footer
    embed.set_footer(text='@hyun woong', icon='https://static-breeze.nike.co.kr/kr/ko_kr/cmsstatic/theme/52/android-icon-36x36.png', ts=True)

    # Send Discord alert
    embed.post()

def get_size(product_url):
    size_str = ''

    my_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': product_url
    }
    
    # Product ID랑 TS 제작
    resp = requests.get(product_url, headers=my_header)
    bs = BeautifulSoup(resp.text, 'lxml')
    div = bs.find('div', class_='info-wrap_product_n uk-width-medium-1-1 uk-width-large-2-5')
    pid = div['data-product-id'].strip()
    ts = int(time.time() * 1000)

    # 사이즈 따오기
    size_url = 'https://www.nike.com/kr/ko_kr/productSkuInventory?productId={}&_={}'.format(pid, ts)
    resp = requests.get (size_url, headers=my_header)
    resp.encoding = ''
    json_data = json.loads(resp.text)

    for data in json_data['skuPricing']:
        name = data['externalId'].split(' ')[-1]  
        qunatity = data['quantity']
        if qunatity>0 :
            size_str += "{}({})\n".format(name, qunatity)

    return size_str


if __name__ == "__main__":
    ''' --------------------------------- INPUT YOUR CONFIG --------------------------------- '''
    MONITOR_DELAY = 5  # second, if your input 10, monitor interval 10 second
    discord_webhook = ''

    ''' ------------------------------------------------------------------------------------- '''
    my_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }

    # 모니터링 전에 상품 DB 만들기
    print(">>> 초기 상품 리스트들을 불러오기")
    resp = requests.get('https://www.nike.com/kr/ko_kr/w/xg/xb/xc/new-releases', headers=my_header)
    resp.encoding = ''
    bs = BeautifulSoup(resp.text, 'lxml')
    divs = bs.find_all('div', class_='a-product')

    product_db = dict()
    for div in divs:
        title = div.find('span', class_='item-title').text.strip()
        secTitle = div.find('span', class_='text-color-secondary').text.strip()
        productLink = 'https://www.nike.com' + div.find('a', class_='a-product-image-link')['href']
        imgLink = div.find('div', class_='a-product-image-primary').img['src'].strip().replace('?browse', '')
        price = div.find('p', class_='product-display-price').text.strip()
        product_db[title+secTitle] = [title, secTitle, imgLink, productLink, price] 
        #print(title+secTitle)

    #일부러 하나뺴기

    product_db.pop('나이키 덩크 하이여성 신발 라이프스타일')

    # # 모니터링 시작 !
    print(">>> 모니터링시작 !!")
    for loopCnt in tqdm(range(int(1*60*60*24 / MONITOR_DELAY))):
        resp = requests.get('https://www.nike.com/kr/ko_kr/w/xg/xb/xc/new-releases', headers=my_header)
        resp.encoding = ''
        bs = BeautifulSoup(resp.text, 'lxml')
        divs = bs.find_all('div', class_='a-product')
        for div in divs:
            title = div.find('span', class_='item-title').text.strip()
            secTitle = div.find('span', class_='text-color-secondary').text.strip()
            productLink = 'https://www.nike.com' + div.find('a', class_='a-product-image-link')['href']
            imgLink = div.find('div', class_='a-product-image-primary').img['src'].strip().replace('?browse', '')
            price = div.find('p', class_='product-display-price').text.strip()
            if title+secTitle not in product_db.keys():
                size_str = get_size(productLink)
                product_db[title + secTitle] = [title, secTitle, imgLink, productLink, price]
                send_embed("Nike", title, price, imgLink, productLink, size_str)
        time.sleep(MONITOR_DELAY)
