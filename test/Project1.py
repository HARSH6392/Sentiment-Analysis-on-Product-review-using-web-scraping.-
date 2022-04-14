from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def start(product_link = "https://www.amazon.in/Vivo-Y33s-Storage-Additional-Exchange/dp/B08ZJR6BMV/ref=sr_1_1_sspa?keywords=mobiles&qid=1644125639&sprefix=mobil%2Caps%2C319&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzVldHMUxHVVAzRlhQJmVuY3J5cHRlZElkPUEwMDc5NTY0MzBGRUk4Rko0RkY3TCZlbmNyeXB0ZWRBZElkPUEwNzAwMzgwMzQxR1FPSFZZT0daMiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU="):
    driver=webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(product_link)
    review_page_link = driver.find_element(by='id',value="reviews-medley-footer").find_element_by_css_selector('a.a-link-emphasis').get_attribute('href')
    return driver,review_page_link

def extract(driver,link,page = 1):    
    review_next_link=f'{link}&pageNumber={page}'
    driver.get(review_next_link)
    review_area = driver.find_element_by_css_selector('#cm_cr-review_list')
    review_list = review_area.find_elements_by_css_selector('.review')
    if review_list:
        print(len(review_list))
    else:
        print('crap')

    data=[]
    for item in review_list:
        try:
            title=item.find_element_by_css_selector('span.a-profile-name').text
        except:
            title=""
        try:
            date=item.find_element_by_css_selector('span.a-size-base.a-color-secondary.review-date').text
        except:
            date=""
        
        try:
            content=item.find_element_by_css_selector('span.a-size-base.review-text.review-text-content').text
        except:
            content=""
        try:
            verified_pro=item.find_element_by_css_selector('span.a-size-mini.a-color-state.a-text-bold').text
        except:
            verified_pro=""
        try:
            rating=item.find_elements_by_css_selector('i.a-icon-star')[-1]
            rating=rating.get_attribute('class')
            if "5" in rating:
                rating=5
            elif "4" in rating:
                rating=4
            elif "3" in rating:
                rating=3
            elif "2" in rating:
                rating=2
            elif "1" in rating:
                rating=1
        except:
            rating=""
        data.append({
            'title':title,
            'date':date,
            'content':content,
            'verified_product':verified_pro,
            'rating':rating
        })
    return data

def save(reviews,filename='product_review.csv'):
    pd.DataFrame(reviews).to_csv(filename,index=None)

if __name__ == "__main__":
    driver, link = start()
    page = 1
    review_list = []
    while True:
        try:
            data = extract(driver,link,page)
            if len(data)>0:
                review_list.extend(data)
                page+=1
            else:
                print("no data")
                break
        except Exception as e:
            print(e)
            break 
        
    driver.close()
    if len(review_list)>0:
        save(review_list,'vivo_reviews2.csv')
    else:
        print("no reviews")