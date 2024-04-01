from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


reviews_pd=pd.DataFrame(columns=['Season','Stars','Review'])
reviews_number=500
number_of_seasons=8


for j in range(number_of_seasons):

    season_url='https://www.rottentomatoes.com/tv/game_of_thrones/s0'+str(j+1)+'/reviews?type=user'
    browser=webdriver.Firefox()
    browser.get(season_url)
    reviews_list=[]
    reviews_to_retrieve=reviews_number

    while reviews_number>len(browser.find_elements(By.CLASS_NAME, 'audience-review-row')):
        load_button=browser.find_element(By.XPATH, '//*[@id="reviews"]/div[2]/rt-button')
        try:
            load_button.click()
        except:
            reviews_to_retrieve=len(browser.find_elements(By.CLASS_NAME, 'audience-review-row'))
            break
        time.sleep(2)
    print('moving outside loading loop')

    print(reviews_to_retrieve)
    for i in range(reviews_to_retrieve):
        stars=0.0
        stars_path='//*[@id="reviews"]/div[1]/div['+str(i+1)+']/div[2]/div[1]/span[1]/span'
        review_path='//*[@id="reviews"]/div[1]/div['+str(i+1)+']/div[2]/drawer-more/p'
        review_stars=browser.find_element(By.XPATH,stars_path)
        stars+=len(review_stars.find_elements(By.CLASS_NAME,'star-display__filled '))
        if review_stars.find_elements(By.CLASS_NAME, 'star-display__half '):
            stars+=0.5
        review_item=browser.find_element(By.XPATH,review_path)
        reviews_list.append((j+1,stars,review_item.text))
    reviews_pd=pd.concat([reviews_pd,pd.DataFrame(reviews_list, columns=['Season','Stars','Review'])],ignore_index=True)

    browser.quit()

reviews_pd.to_csv('E:Downloads/Game of Thrones reviews.csv', sep=',',encoding='utf-8', index=False)
