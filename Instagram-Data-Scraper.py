import json
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def scroll_to_bottom(driver, pause_time=2):
    """
        Scroll to the bottom of the web page.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        

def get_liked_users(post_link, driver, username):
    """
        This function takes a link of an Instagram post and returns a list of usernames who have liked the post.
    """
    user_likes = []
    user_links_dict = {}
    pattern = r'^^https:\/\/www\.instagram\.com\/(.*)$'
    block_link = (
    "https://www.instagram.com/",
    "https://www.instagram.com/explore/",
    "https://www.instagram.com/reels/",
    "https://www.instagram.com/direct/inbox/",
    f"https://www.instagram.com/{username}/",
    "https://www.instagram.com/about/jobs/",
    "https://www.instagram.com/legal/privacy/",
    "https://www.instagram.com/legal/terms/",
    "https://www.instagram.com/explore/locations/",
    )

    for a in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/"]'):
        href = a.get_attribute('href')
        result = re.match(pattern, href)
        if href not in block_link and result:
            if href not in user_links_dict:
                user_links_dict[href] = True
                user_likes.append(f"https://www.instagram.com/{result.group(1)}") 
                
    return user_likes
def scrape_instagram_data(username, password, target_user):
    """
        Scrape data from an Instagram profile.
    """
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

    # Click login button and handle Save Info dialog
    try:
        button_login = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        button_login.click()

        save_info_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Save Info")]')))
        save_info_button.click()
        
        not_now_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]')))
        not_now_button.click()
    except:
        pass

    # Navigate to the target user's profile

    driver.get(f"https://www.instagram.com/{target_user}/")

    # Get number of followers and following
    try:
        followers_count = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href="/{target_user}/followers/"]'))
        ).text
    except:
        followers_count = "N/A"

    try:
        following_count = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href="/{target_user}/following/"]'))
        ).text
    except:
        following_count = "N/A"

    # Get number of posts
    try:
        posts_count = driver.find_element(By.XPATH, 'span[text()=" posts"]').find_element(By.XPATH, '..').text.replace(' posts', '')
    except:
        posts_count = "N/A"

    # Scroll down to load all posts
    scroll_to_bottom(driver)

    # Get all post links
    post_links = []
    for a in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]'):
        href = a.get_attribute("href")
        if "/p/" in href and href not in post_links:
            post_links.append(href)

    # Get number of likes and comments for each post
    posts_data = []
    for link in post_links:
        driver.get(link)
        try:
            likes_count = driver.find_element(By.CSS_SELECTOR, 'span[style="line-height: 18px;"]').text
        except:
            likes_count = "N/A"

        try:
            date_posted = driver.find_element(By.CSS_SELECTOR, 'span[style="line-height: var(--base-line-clamp-line-height); --base-line-clamp-line-height: 12px;"]')
        except:
            date_posted = "N/A"

        posts_data.append({
            'link': link,
            'likes': likes_count,
            'date_posted': date_posted,
        })

    # Get list of users who have liked the first post
    if post_links:
        users_who_liked_post = get_liked_users(post_links[0], driver, target_user)
    else:
        users_who_liked_post = []

    # Create dictionary with all data
    data = {
        'username': target_user,
        'followers': followers_count,
        'following': following_count,
        'posts': posts_count,
        'users_who_liked_first_post': users_who_liked_post,
        'post_data': posts_data
    }

    # Save data to json file
    output_filename = f"{target_user}.json"
    with open(output_filename, 'w') as f:
        json.dump(data, f)

    print(f"Data has been successfully scraped and saved to {output_filename}")



username = "your_username"
password = "your_password"
target_user = "target_username"

scrape_instagram_data(username, password, target_user)
