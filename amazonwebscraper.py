from bs4 import BeautifulSoup
import requests
import pandas as pd

csv_header = ['title', 'price', 'rating', 'no. of reviews', 'product URL', 'brand name', 'special features']

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36","Accept-Encoding": "gzip, deflate","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

# searching for...
# enter product inside ''
query = ''

# format search
search = query.replace(' ', '+')

# URL with our search
URL = (f'https://www.amazon.com/s?k={search}')

for page in range(1,2):
    webpage = requests.get(URL + f'&page={page}', headers=headers)

    soup_messy = BeautifulSoup(webpage.content, 'html.parser')
    soup = BeautifulSoup(soup_messy.prettify(), 'html.parser')

    # the elements we need are in this HTML class
    results = soup.find_all('div', {'data-component-type':'s-search-result'})

    for result in results:
        title = result.find('a', {'class': 'a-text-normal'}).get_text().strip()
        price = result.find('span', {'class':'a-offscreen'}).get_text().strip()
        try:
            rating = result.find('span', {'a-icon-alt'}).get_text().strip()
            no_reviews = result.find('span', {'class':'a-size-base'}).get_text().strip()
        except AttributeError:
            continue
            
        link = result.find('a', {'class': 'a-text-normal'})
        product_url = 'https://www.amazon.com' + link.get('href')

#         print(title)
    #     print(price)
    #     print(rating)
    #     print(no_reviews)
#         print(product_url)
    
        # webscraping each product's webpage to get brand name 
        product_webpage = requests.get(product_url, headers=headers)
        product_soup = BeautifulSoup(product_webpage.content, 'html.parser')
        
        product_results = product_soup.find_all('table', {'class':'prodDetTable'})
        for pr in product_results:
            product_resultss = pr.find_all('tr')
            
            for product in product_resultss:
                thh = product.find_all('th', {'class': 'prodDetSectionEntry'})
                for th in thh:
                    if th.text.strip() == 'Manufacturer':
                        brand_name = product.find('td', {'class': 'prodDetAttrValue'}).text.strip()
#                         print(brand_name)
                    if th.text.strip() == 'Special Features':
                        special_features = product.find('td', {'class': 'prodDetAttrValue'}).text.strip()
#                         print(special_features)
         
                    # csv_data = [title, price, rating, no_reviews, product_url, brand_name, special_features]

                    # product_data = pd.DataFrame([csv_data], columns=csv_header)
                    # product_data.to_csv('product.csv',index=False)
