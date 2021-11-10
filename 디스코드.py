from discord_hooks import Webhook
''' --------------------------------- INPUT YOUR CONFIG --------------------------------- '''
MONITOR_DELAY = 5  # second, if your input 10, monitor interval 10 second
discord_webhook = 'https://discord.com/api/webhooks/802849403324989440/XsPGI-I48u9ZNonQ9GUcb0grL6tLHIVFsptic6R2O1993vVlcmTYVJQfY_aIWhr_fUTu'

''' ------------------------------------------------------------------------------------- '''

def send_embed(site, product_name, price, img_link, product_link, size):
    # Create embed to send to webhook
    embed = Webhook(discord_webhook, color=123123)

    # Set author info
    embed.set_author(name=site, icon='https://static-breeze.nike.co.kr/kr/ko_kr/cmsstatic/theme/52/android-icon-36x36.png')

    #embed.set_desc("NEW: " + test)
    embed.add_field(name="Name", value='[{}]({})'.format(product_name, product_link))#링크다는것
    link = driver.find_element_by_xpath('//*[@id="main-area"]/div[4]/table/tbody/tr[{}]/td[1]/div[2]/div/a[1]'.format(i)).get_attribute("href")
    embed.add_field(name="Price", value=price)
    embed.add_field(name="Size", value=size)
    embed.set_thumbnail(img_link)

    # Set footer
    embed.set_footer(text='@DevHong', icon='https://static-breeze.nike.co.kr/kr/ko_kr/cmsstatic/theme/52/android-icon-36x36.png', ts=True)

    # Send Discord alert
    embed.post()

# 제조사명, 타이틀, 가격, 이미지링크, 상품링크, 사이즈
send_embed("Nike", '타이틀', '가격',
           'https://static-breeze.nike.co.kr/kr/launch/cmsstatic/product/CT1983-700/977fd3bd-c15b-4188-a30c-78bb16af9db2_primary.jpg?gallery',
           'https://static-breeze.nike.co.kr/kr/launch/cmsstatic/product/CT1983-700/977fd3bd-c15b-4188-a30c-78bb16af9db2_primary.jpg?gallery',
           '사이즈')