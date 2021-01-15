import requests
from bs4 import BeautifulSoup
import telegram
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
# import schedule
# import time
# schedule = BackgroundScheduler()
# schedule = BlockingScheduler()

# telegram bot
api_key = '1542289192:AAFNEO1dwjaAGxZkUxkh2ePS9qCI-RGMTJM'
chat_id = 1496928127
bot = telegram.Bot(token = api_key)

def extract_item():
    # create soup from url
    url = 'https://shop.ihanstyle.com/product.do?cmd=getProductDetail&PROD_CD=HAD82CO502BKBK&ITHR_CD=HS12_01'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')

    # designer and name
    item_name = soup.find('div', {'class' : 'section1'})
    designer = item_name.find('div', {'class' : 'bn'}).find('p').string
    name = item_name.find('div', {'class' : 'pn'}).find('h3').string.strip()

    # jpg file
    pic = soup.find('div', {'class' : 'bigImg'})
    jpg = pic.find('li', {'class' : 'active'}).find('img')['src']

    #size 
    size_quantity = soup.find('div', {'class' : 'section2'})
    sizes = size_quantity.find('ul', {'class' : 'size_list'}).find_all('li')

    instock_list = []
    soldout_list = []
    for size in sizes:
        soldout = size.find('span', {'class' : 'soldout'})
        # in stock
        if soldout is None:
            instocks = size.find('button', {'type' : 'button'}).string
            instock_list.append(instocks)
        #  out of stock
        else:
            soldouts = soldout.string
            soldout_list.append(soldouts)

    #price
    price = item_name.find('p', {'class' : 'event_discount'}).string.strip('￦')

    # send stock message
    bot.sendMessage(chat_id = chat_id, text = url)
    bot.sendMessage(chat_id = chat_id, text = f'https:{jpg}')
    bot.sendMessage(chat_id = chat_id, text = f'{designer}, {name}')
    bot.sendMessage(chat_id = chat_id, text = f'Price : ￦{price}')

    for sizes in instock_list:
        bot.sendMessage(chat_id = chat_id, text = f'Size {sizes} in stock')

    for sizes in soldout_list:
        bot.sendMessage(chat_id = chat_id, text = f'Size {sizes} out of stock')

extract_item()
# schedule.every(10).seconds.do(extract_item)
# schedule.every().day.at("09:00").do(extract_item)

# while True:
#     schedule.run_pending()
    #time.sleep(5)

# schedule.add_job(extract_item, 'interval', seconds = 5)
# schedule.start()
# schedule.shutdown()


# way to run other python programs in parallel?
