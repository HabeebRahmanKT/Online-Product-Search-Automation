import requests
import datetime
import smtplib
import gspread
import csv
import ssl
from bs4 import BeautifulSoup


URLs = ['https://www.flipkart.com/asus-vivobook-k15-oled-2022-ryzen-5-hexa-core-5500u-16-gb-512-gb-ssd-windows-11'
        '-home-km513ua-l511ws-thin-light-laptop/p/itma65cbe0f34166?pid=COMGB6DZ87UFQXMM&lid=LSTCOMGB6DZ87UFQXMMI6QQYG'
        '&marketplace=FLIPKART&q=vivobook+k15+oled+ryzen+5+5500u+16gb+ram&store=6bo%2Fb5g&srno=s_1_8&otracker=search'
        '&otracker1=search&fm=organic&iid=110e45dc-4b27-43db-a9fb-46490627b38e.COMGB6DZ87UFQXMM.SEARCH&ppt=hp&ppn'
        '=homepage&ssid=zgxe6hgtz40000001660230873312&qH=69b567434e86e4d2 ',
        'https://www.flipkart.com/acer-aspire-5-ryzen-hexa-core-5500u-8-gb-512-gb-ssd-windows-11-home-a515-45-thin'
        '-light-laptop/p/itm16666d7c2b0e7?pid=COMG8ZYE6WST2GCU&lid=LSTCOMG8ZYE6WST2GCUEBJACV&marketplace=FLIPKART&q'
        '=acer+aspire+5+a515+45&store=6bo%2Fb5g&srno=s_1_2&otracker=AS_QueryStore_OrganicAutoSuggest_1_14_na_pm_ps'
        '&otracker1=AS_QueryStore_OrganicAutoSuggest_1_14_na_pm_ps&fm=Search&iid=7a7c2657-7da9-4e81-aaf2-a3f5a54a5592'
        '.COMG8ZYE6WST2GCU.SEARCH&ppt=sp&ppn=sp&ssid=dqzfah339c0000001660231014110&qH=2d3789ed2d48c062 ',
        'https://www.flipkart.com/acer-aspire-5-ryzen-hexa-core-amd-5-5500u-hexa-core-8-gb-512-gb-ssd-windows-10-home'
        '-a515-45-thin-light-laptop/p/itm5af53ffa1b2a3?pid=COMG56TFUUJ874XG&lid=LSTCOMG56TFUUJ874XGMQ0ZMZ&marketplace'
        '=FLIPKART&q=acer+aspire+5+a515+45&store=6bo%2Fb5g&srno=s_1_1&otracker'
        '=AS_QueryStore_OrganicAutoSuggest_1_14_na_pm_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_14_na_pm_ps&fm'
        '=Search&iid=7a7c2657-7da9-4e81-aaf2-a3f5a54a5592.COMG56TFUUJ874XG.SEARCH&ppt=sp&ppn=sp&ssid'
        '=dqzfah339c0000001660231014110&qH=2d3789ed2d48c062 ',
        'https://www.flipkart.com/acer-aspire-5-ryzen-hexa-core-5500u-8-gb-512-gb-ssd-windows-10-home-a515-45-r0hb'
        '-thin-light-laptop/p/itmfbe565258f74e?pid=COMGFQ4AY3PEXJNA&lid=LSTCOMGFQ4AY3PEXJNADQLDYO&marketplace'
        '=FLIPKART&q=acer+aspire+5+a515+45&store=6bo%2Fb5g&srno=s_1_5&otracker'
        '=AS_QueryStore_OrganicAutoSuggest_1_14_na_pm_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_14_na_pm_ps&fm'
        '=Search&iid=7a7c2657-7da9-4e81-aaf2-a3f5a54a5592.COMGFQ4AY3PEXJNA.SEARCH&ppt=sp&ppn=sp&ssid'
        '=dqzfah339c0000001660231014110&qH=2d3789ed2d48c062 ',
        'https://www.flipkart.com/acer-aspire-7-ryzen-5-hexa-core-5500u-8-gb-512-gb-ssd-windows-10-home-4-graphics'
        '-nvidia-geforce-gtx-1650-a715-42g-gaming-laptop/p/itm69a247c4ad300?pid=COMGYCG8ZBXWPYUU&lid'
        '=LSTCOMGYCG8ZBXWPYUUJT3OIF&marketplace=FLIPKART&q=acer+aspire+7+ryzen+5+5500u+hexacore&store=6bo%2Fb5g&srno'
        '=s_1_1&otracker=AS_Query_HistoryAutoSuggest_4_0&otracker1=AS_Query_HistoryAutoSuggest_4_0&fm=organic&iid'
        '=0d589643-a97a-4046-9883-4a6f55b2a29e.COMGYCG8ZBXWPYUU.SEARCH&ppt=hp&ppn=homepage&ssid'
        '=mw9l4u2x1c0000001660261790107&qH=57d4ba04e824bb80 ',
        'https://www.flipkart.com/lenovo-ideapad-gaming-3-ryzen-5-hexa-core-5600h-8-gb-512-gb-ssd-windows-11-home-4'
        '-graphics-nvidia-geforce-gtx-1650-120-hz-15ach6-15ach6d1-gaming3-15ach6d1-laptop/p/itmeb72bf79e6eb4?pid'
        '=COMG8ZHDWJXZRHBW&lid=LSTCOMG8ZHDWJXZRHBWRJPFSD&marketplace=FLIPKART&q=lenovo+ideapad+gaming+3+ryzen+5+5600h'
        '&store=6bo%2Fb5g&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_24_na_na_ps&otracker1'
        '=AS_QueryStore_OrganicAutoSuggest_1_24_na_na_ps&fm=Search&iid=5eab757f-6012-48dc-a1f4-60acb517a8fa'
        '.COMG8ZHDWJXZRHBW.SEARCH&ppt=sp&ppn=sp&ssid=7wf090b7hs0000001660261959170&qH=c1bdbefd25a30e41 ',
        'https://www.flipkart.com/hp-pavilion-ryzen-5-hexa-core-5600h-8-gb-512-gb-ssd-windows-10-4-graphics-nvidia'
        '-geforce-gtx-1650-144-hz-15-ec2004ax-gaming-laptop/p/itm98c94bbf9bc20?pid=COMG5GZXPWMGTNWS&lid'
        '=LSTCOMG5GZXPWMGTNWSQE9WVW&marketplace=FLIPKART&q=hp+pavilion+15+ryzen+5+8gb%2F512gb+ssd&store=6bo%2Fb5g'
        '&spotlightTagId=BestsellerId_6bo%2Fb5g&srno=s_1_1&otracker=AS_QueryStore_HistoryAutoSuggest_1_3_na_na_na'
        '&otracker1=AS_QueryStore_HistoryAutoSuggest_1_3_na_na_na&fm=search-autosuggest&iid=d40a3b57-0993-479b-a581'
        '-b28c0540ea16.COMG5GZXPWMGTNWS.SEARCH&ppt=sp&ppn=sp&ssid=47r29czqgg0000001660263767334&qH=961f10f1a6aaf2e5 ',
        'https://www.flipkart.com/hp-pavilion-ryzen-5-hexa-core-5500u-8-gb-512-gb-ssd-windows-10-home-14-ec0035au'
        '-thin-light-laptop/p/itmf7055ef4f789e?pid=COMG67BXZCXUTPG2&lid=LSTCOMG67BXZCXUTPG2USMKZU&marketplace'
        '=FLIPKART&q=hp+pavilion+15+ryzen+5+8gb%2F512gb+ssd&store=6bo%2Fb5g&srno=s_1_2&otracker'
        '=AS_QueryStore_HistoryAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_HistoryAutoSuggest_1_3_na_na_na&fm'
        '=organic&iid=d40a3b57-0993-479b-a581-b28c0540ea16.COMG67BXZCXUTPG2.SEARCH&ppt=hp&ppn=homepage&ssid'
        '=47r29czqgg0000001660263767334&qH=961f10f1a6aaf2e5 '
        ]


# def send_email(message):
#     port = 465  # For SSL
#     smtp_server = "smtp.gmail.com"
#     sender_email = "hrkt.developmet@gmail.com"
#     password = input("Enter your password : ")
#     receiver_email = "habeeb.123.786.cff@gmail.com"
#
#     context = ssl.create_default_context()
#
#     with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)


def format_message(laptop_details):
    _formatted_message = f"Product : {laptop_details[1]}\n" \
                         f"Price : {laptop_details[2]}\n" \
                         f"Available : {laptop_details[3]}\n" \
                         f"Quantity Left : {laptop_details[4]}\n\n"

    return _formatted_message


def save_details_to_gspread(_details):
    service_account = gspread.service_account("credentials.json")
    sheets = service_account.open('laptop_price')
    worksheet = sheets.get_worksheet(0)

    print(str(worksheet.row_count()), str(worksheet.col_count))


def save_to_text_file(text):
    print(text)
    with open("laptop_details.txt", "a") as text_file:
        text_file.write(text)


def save_details_in_csv(_details, _file_name):
    try:
        with open(_file_name, 'r') as laptop_price:
            csv.reader(laptop_price)

    except FileNotFoundError:
        with open(_file_name, 'a') as laptop_price:
            csv_writer = csv.writer(laptop_price)
            csv_writer.writerow(['UPDATED TIME', 'TITLE', 'PRICE', 'AVAILABILITY', 'QUANTITY LEFT'])

    finally:
        with open(_file_name, 'a') as laptop_price:
            csv_writer = csv.writer(laptop_price)
            csv_writer.writerow(_details)


def get_details(_parse_tree):
    # \u20b9 => rupees symbol
    # By default the data has rupee symbol and throwing an UnicodeEncodeError
    updated_time = datetime.datetime.now()
    title = _parse_tree.title.text[0:100]
    price = _parse_tree.find('div', class_='_30jeq3 _16Jk6d')
    if price is not None:
        price = price.text.lstrip('\u20b9').replace(',', "")
    quantity_left = 'NOT SPECIFIED'
    product_available = True

    sold_out_text_box = _parse_tree.find('div', class_='_16FRp0')

    if sold_out_text_box is not None:
        product_available = False
        quantity_left = 'OUT OF STOCK'

    # quantity_left_box => quantity of product left with the seller
    if product_available:
        quantity_left_box = _parse_tree.find('div', class_='_2JC05C')

        if quantity_left_box is not None and quantity_left != 'NOT SPECIFIED':
            print(quantity_left)
            quantity_left = int(quantity_left_box.text.lstrip('Hurry, Only ').rstrip(' left!'))

    return [updated_time, title, price, product_available, quantity_left]


def make_request(_url):
    _get_request = requests.get(_url)
    return _get_request


if __name__ == '__main__':

    email_message = f"Date & Time : {str(datetime.datetime.now())}\n\n"
    #
    for index, url in enumerate(URLs):
        request_response = make_request(url)

        if request_response.status_code == 200:
            parse_tree = BeautifulSoup(request_response.content, 'html.parser')
            details = get_details(parse_tree)

    #          save_details_to_gspread(details)
    #
    #         file_name = f'{details[1][0:20]}_{index + 1}.csv'
    #         save_details_in_csv(details, file_name)
    #
            formatted_message = format_message(details)
            email_message += formatted_message
    #
    #     else:
    #         print(request_response)
    #
    #     send_email(email_message)

    email_message += "\n\n"
    save_to_text_file(email_message)
