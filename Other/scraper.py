from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import os

driver = webdriver.Chrome('chromedriver.exe')

def get_flowers(driver):

    driver.get("https://garden.org/plants/group/")

    table = driver.find_element_by_xpath("//table[@class='table table-striped table-bordered table-hover caption-top pretty-table']")
    rows = table.find_elements_by_xpath(".//tr")

    flowers = {}

    for row in rows:
      if len(row.find_elements_by_tag_name("td")) == 0:
        pass
      else:
        col = row.find_elements_by_tag_name("td")
        if col[2].text == "--":
          pass
        elif int(col[2].text.replace(",", "")) > 1499:
          fl = col[0].text
          u = col[0].find_elements_by_xpath("a[@href]")[0].get_attribute("href")
          flowers[fl] = u
    
    return flowers

def get_image_page(driver):
    flowers = get_flowers(driver)
    print(len(flowers))
    for fl in flowers:
      driver.get(flowers[fl])
      image_page_url = driver.find_elements(by=By.XPATH, value="//div[@class='card-body']/a[@href]")
      if image_page_url[1].text.startswith("» Browse the full list of"):
        image_page_url = image_page_url[1].get_attribute("href")
        flowers[fl] = image_page_url

    return flowers

def is_valid_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return True

def download_images(driver):
    flowers = get_image_page(driver)
    parent_dir = 'D:/Studies/College/Coursework/Petal/Other/images/'
    for fl in flowers:
      os.mkdir(path=parent_dir + fl.lower())
      offset = '?offset='
      offset_num = 0
      image_count = 0
      forbiden = ['loading.gif', 'logo.png', 'plants.png', 'btn_newsletter.png']
      while image_count < 1501:
        driver.get(flowers[fl] + offset + str(offset_num))
        images = driver.find_elements_by_tag_name('img')
        for image in images:
          if is_valid_url(image.get_attribute('src')):
            # save image to folder
            url = image.get_attribute('src')
            filename = 'images/' + fl.lower() + '/' + fl.lower() + str(image_count)
            if url.rsplit('/', 1)[-1] in forbiden:
              pass
            else: 
              try:
                urllib.request.urlretrieve(url, filename + '.jpg')
              except:
                pass
            image_count += 1
        offset_num += 20

download_images(driver)

driver.close()