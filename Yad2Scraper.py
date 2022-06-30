import csv
from time import sleep
from bs4 import BeautifulSoup
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException


def close_ads(driver):
    ads = driver.find_elements(By.ID, "slot-close-button")  # Both bottom banners
    ads += driver.find_elements(By.CSS_SELECTOR, "button[class='widget-floating__button widget-floating__button--close'")  # Chat box, "Do you have a question?"
    ads += driver.find_elements(By.ID, "XMLID_54_")  # The Doron popup

    if ads:
        print(f'Found {len(ads)} ads. Start closing them...')
    for ad in ads:
        try:
            actions.click(ad)
            actions.perform()
            print('One ad was closed')
        except:
            print("Couldn't close ad")


total_posts = 0
successful_posts = 0

driver = uc.Chrome(use_subprocess=True)
actions = ActionChains(driver)

first_page = 0
last_page = 760
url = 'https://www.yad2.co.il/realestate/rent?page='

header = ['Post link', 'City', 'Neighborhood', 'Size', 'Number of rooms', 'Floor number', 'Taxes', 'Price',
          'Room mates', 'Furniture', 'Elevator', 'Air conditioner', 'Parking', 'Balcony', 'Bars', 'Shelter',
          'Storeroom', 'Renovated', 'Boiler', 'Pets allowed']

with open('raw_yad2_data.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for page_num in range(first_page, last_page):
        print('Going over page', page_num)
        driver.get(url + str(page_num))
        sleep(10)

        # Open all the posts JS
        posts_collapsed = driver.find_elements(By.CLASS_NAME, "date")
        for post_collapsed in posts_collapsed:
            close_ads(driver)
            try:
                post_collapsed.click()
            except ElementClickInterceptedException as e:
                print(e)
            sleep(2)
        html_dom = driver.page_source
        soup = BeautifulSoup(html_dom, 'html5lib')

        # Search each post
        posts = soup.find_all('div', attrs={'class': 'feeditem table'})
        print(f'Going over {len(posts)} posts out of {len(posts_collapsed)} posts in that page')
        for post in posts:
            total_posts += 1
            try:
                # Get city and neighborhood
                location_dom = post.find('span', attrs={'class': 'subtitle'})

                # Get the price
                price_dom = post.find('div', attrs={'data-test-id': 'item_price'})
                price = ''.join([n for n in price_dom.text if n.isdigit()])

                # Get features
                features = post.find_all('div', attrs={'class': 'info_feature'})
                features_dict = {'Air conditioner': 0, 'Room mates': 0, 'Elevator': 0, 'Bars': 0, 'Boiler': 0,
                                 'Shelter': 0, 'Storeroom': 0, 'Renovated': 0, 'Pets allowed': 0, 'Furniture': 0}
                for feature in features:
                    if 'מיזוג' in feature.text or 'מזגן' in feature.text:
                        features_dict['Air conditioner'] = 1
                    elif 'לשותפים' in feature.text:
                        features_dict['Room mates'] = 1
                    elif 'סורגים' in feature.text:
                        features_dict['Bars'] = 1
                    elif 'דוד שמש' in feature.text:
                        features_dict['Boiler'] = 1
                    elif 'מעלית' in feature.text:
                        features_dict['Elevator'] = 1
                    elif 'משופצת' in feature.text:
                        features_dict['Renovated'] = 1
                    elif 'מחסן' in feature.text:
                        features_dict['Storeroom'] = 1
                    elif 'ריהוט' in feature.text:
                        features_dict['Furniture'] = 1
                    elif 'ממ"ד' in feature.text:
                        features_dict['Shelter'] = 1
                    elif 'חיות' in feature.text:
                        features_dict['Pets allowed'] = 1

                # Get size and taxes and parking
                info_items = post.find_all('dl', attrs={'class': 'info_item'})
                size, taxes, parking, balcony = None, None, None, None
                for info_item in info_items:
                    if 'מ"ר' in info_item.text:
                        size = ''.join([n for n in info_item.text if n.isdigit()])
                    elif 'ארנונה' in info_item.text:
                        taxes = ''.join([n for n in info_item.text if n.isdigit()])
                    elif 'חניות' in info_item.text:
                        parking = 0
                        parking_num = ''.join([n for n in info_item.text if n.isdigit()])
                        if parking_num:
                            parking = 1
                    elif 'מרפסות' in info_item.text:
                        balcony = ''.join([n for n in info_item.text if n.isdigit()])

                # Get city
                title_dom = post.find('span', attrs={'class': 'subtitle'})
                title = title_dom.text.split(',')
                if 'דירה' not in title[0]:
                    continue
                neighborhood = title[1].strip()
                city = title[2].strip()

                # Get number of rooms
                rooms_dom = post.find('div', attrs={'class': 'data rooms-item'})
                rooms = ''.join([n for n in rooms_dom.text if n.isdigit() or n == '.'])

                # Get floor number
                floor_dom = post.find('div', attrs={'class': 'data floor-item'})
                floor = ''.join([n for n in floor_dom.text if n.isdigit()])

                # Get tab link for the post. This is to differ different posts
                a_link = None
                try:
                    link_dom = post.find('a', attrs={'title': 'טאב חדש'})
                    a_link = link_dom['href'][22:]
                except:
                    continue

                data_row = [a_link, city, neighborhood, size, rooms, floor, taxes, price, features_dict['Room mates'],
                            features_dict['Furniture'], features_dict['Elevator'], features_dict['Air conditioner'],
                            parking, balcony, features_dict['Bars'], features_dict['Shelter'],
                            features_dict['Storeroom'], features_dict['Renovated'], features_dict['Boiler'],
                            features_dict['Pets allowed']]
                writer.writerow(data_row)

                successful_posts += 1
                print(f'Total stats: {total_posts}\{successful_posts}')
            except Exception as e:
                print(e)
                continue
