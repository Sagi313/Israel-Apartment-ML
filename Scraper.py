import requests
from bs4 import BeautifulSoup
import csv

### Already Covered
### 670019 - 685800
###
###

# TODO
# Add strip() on all text values

start_page_num = 665019
end_page_num = 670019

total_successful_records = 0

feature_names = ['Room mates', 'Furniture', 'Elevator', 'Air conditioner', 'Parking', 'Balcony', 'Bars', 'Shelter',
                 'Storeroom', 'Renovated', 'Boiler', 'Pets allowed']
header = ['Page number', 'City', 'Neighborhood', 'Size', 'Number of rooms', 'Floor number', 'Taxes',
          'Price'] + feature_names

with open('raw_homeless_data.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # writer.writerow(header)

    for page_num in range(start_page_num, end_page_num):
        try:
            url = f'https://www.homeless.co.il/rent/viewad,{page_num}.aspx'
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html5lib')

            # Validate apartment rental
            post_title = soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('li')
            if post_title[0].text != 'דירה להשכרה':
                continue

            # Get the price
            price = soup.find('div', attrs={'class': 'price'})
            price = ''.join([n for n in price.text if n.isdigit()])

            # Get floor
            data_ele = soup.find_all('div', attrs={'style': 'float:right; width:150px;'})
            floor = None
            for data in data_ele:
                if 'קומה' in data.text:
                    if 'קרקע' in data.text:
                        floor = 0
                    elif 'מרתף' in data.text:
                        floor = -1
                    elif data.text[6].isdigit():
                        floor = int(data.text[6:7])

            # Get size in square meter
            data_ele = soup.find_all('div', attrs={'style': 'float:right; width:130px;'})
            size = None
            for data in data_ele:
                if 'מ"ר' in data.text:
                    size = ''.join([n for n in data.text if n.isdigit()])

            # Get taxes
            data_ele = soup.find_all('div', attrs={'style': 'float:right; width:140px;'})
            taxes = None
            for data in data_ele:
                if 'ארנונה' in data.text:
                    taxes = ''.join([n for n in data.text if n.isdigit()])

            # Get features
            features_dict = {}
            features = soup.find_all('div', attrs={'style': 'float:right; width:130px;'})

            for index, feature in enumerate(features):
                try:
                    image_src = feature.img['src']
                    if 'uncheked' in image_src:
                        features_dict[feature_names[index]] = 0
                    else:
                        features_dict[feature_names[index]] = 1
                except TypeError:
                    break

            # Get city and neighborhood
            post_title = soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('li')
            city = post_title[1].text[13:]
            neighborhood = post_title[2].text

            # Get number of rooms
            # TODO: allow float numbers
            rooms = ''.join([n for n in post_title[3].text if n.isdigit() or n is "."])

            data_row = [page_num, city, neighborhood, size, rooms, floor, taxes, price, features_dict['Room mates'],
                        features_dict['Furniture'], features_dict['Elevator'], features_dict['Air conditioner'],
                        features_dict['Parking'], features_dict['Balcony'], features_dict['Bars'],
                        features_dict['Shelter'], features_dict['Storeroom'], features_dict['Renovated'],
                        features_dict['Boiler'], features_dict['Pets allowed']]
            feature_names = ['Room mates', 'Furniture', 'Elevator', 'Air conditioner', 'Parking', 'Balcony', 'Bars',
                             'Shelter', 'Storeroom', 'Renovated', 'Boiler', 'Pets allowed']

            writer.writerow(data_row)

            total_successful_records += 1
            print(f'Total stats: {page_num - start_page_num}\{total_successful_records}')

        except:
            continue
