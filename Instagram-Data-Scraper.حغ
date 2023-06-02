import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from bs4 import BeautifulSoup
import requests

def instagram_data_scraper(username, password, target_user):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("http://www.instagram.com")
    
    # Find username and password fields
    username_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    # Enter username and password
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)

    #Click login button
    login_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)
    try:
        not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Save Info")]'))).click()
        not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    except:
        not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

    # navigate to user's profile page
    driver.get('https://www.instagram.com/{}'.format(target_user))

    # get number of followers and following
    try:
        followers_count = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/{}/followers/"]'.format(target_user)))).text
        following_count = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/{}/following/"]'.format(target_user)))).text
    except:
        followers_count = "N/A"
        following_count = "N/A"

    # get number of posts
    try:
        posts_count = driver.find_element_by_xpath('//span[text()=" posts"]').find_element_by_xpath('..').text.replace(' posts', '')
    except:
        posts_count = "N/A"

    # scroll down to load all posts
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # get all post links
    post_links = []

    for a in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]'):
        href = a.get_attribute('href')
        if '/p/' in href and href not in post_links:
            post_links.append(href)

    # get number of likes and comments for each post
    posts_data = []
    for link in post_links:
        driver.get(link)

        # get number of likes
        try:
            likes_count = driver.find_elements(By.CSS_SELECTOR, 'span.sqdOP.yWX7d._8A5w5 > span')[0].text
        except:
            likes_count = "N/A"

        # get number of comments
        try:
            comments_count = driver.find_elements(By.CSS_SELECTOR, 'span.sqdOP.yWX7d._8A5w5 > span')[-1].text
        except:
            comments_count = "N/A"

        posts_data.append({
            'link': link,
            'likes': likes_count,
            'comments': comments_count
        })

    # create dictionary with all data
    data = {
        'username': target_user,
        'followers': followers_count,
        'following': following_count,
        'posts': posts_count,
        'post_data': posts_data
    }

    # save data to json file
    with open('{}.json'.format(target_user), 'w') as f:
        json.dump(data, f)

    # close the browser window
    driver.quit()
    
username = "your_username"
password = "your_password"

instagram_data_scraper(username, password, "target_username")
