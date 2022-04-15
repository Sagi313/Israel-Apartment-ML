from time import sleep
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv



driver = uc.Chrome(use_subprocess=True)
driver.get('https://www.yad2.co.il/')
actions = ActionChains(driver)

first_page = 1
last_page = 2
url = 'https://www.yad2.co.il/realestate/rent?page='

header = ['City', 'Neighborhood','Size', 'Number of rooms', 'Floor number','Taxes' ,'Price']

with open('raw_yad2_data.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for page_num in range(first_page,last_page):
        driver.get(url + str(page_num))

        # Open all the posts JS
        posts_colapsed = driver.find_elements(By.CLASS_NAME, "subtitle")
        for post_colapsed in posts_colapsed:
            actions.click(post_colapsed)
            actions.perform()
            driver.implicitly_wait(5)

        html_dom = driver.page_source
        soup = BeautifulSoup(html_dom)

        # Search each post
        posts = soup.find_all('div', attrs = {'class':'feeditem table'})
        for post in posts:

            # Get city and neighborhood
            location_dom = post.find('span', attrs = {'class':'subtitle'})


            # Get the price
            price_dom = post.find('div', attrs = {'data-test-id':'item_price'})
            price = ''.join([n for n in price_dom.text if n.isdigit()])
            print(price)

            # Get features
            features = post.find_all('div', attrs = {'class':'info_feature'})
            features_dict = {'Air conditioner': 0, 'Room mates':0, 'Elevator':0, 'Bars':0, 'Boiler': 0, 'Shelter': 0, 'Storeroom': 0, 'Renovated': 0, 'Pets allowed': 0, 'Furniture': 0}
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

            # Get size and taxes
            info_items = post.find_all('div', attrs = {'class':'info_item'})
            size, taxes = None, None
            for info_item in info_items:
                if 'מ"ר' in info_item.text:
                    size = ''.join([n for n in info_item.text if n.isdigit()])
                elif 'ארנונה' in info_item.text:
                    taxes = ''.join([n for n in info_item.text if n.isdigit()])


            data_row = []
            writer.writerow(header)


        break