from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_media(media_url, folder_path="media"):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filename = os.path.join(folder_path, os.path.basename(urlparse(media_url).path))
    response = requests.get(media_url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    print(f"Downloaded: {filename}")

def extract_images_and_videos_from_link(url, main_user):
    driver = webdriver.Chrome()  
    driver.get(url)
    time.sleep(5)
    page_source = driver.page_source
    if main_user not in page_source:
        print(f"The page does not belong to the main user '{main_user}'. Exiting.")
        driver.quit()
        return
    main_user_section = driver.find_element(By.XPATH, f"//*[contains(text(), '{main_user}')]/ancestor::article")
    media_elements = main_user_section.find_elements(By.XPATH, './/img[@srcset] | .//video[@src]')
    for element in media_elements:
        media_url = element.get_attribute('src') or element.get_attribute('srcset').split(' ')[0]
        download_media(media_url, folder_path="media")
    driver.quit()
instagram_link = input("Enter the Instagram post link: ")
main_user = input("Enter the main user's username: ")
extract_images_and_videos_from_link(instagram_link, main_user)
