from selenium import webdriver,common
import time
import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.request

def login(username,password):
    print("Spider started")
    urlusername=urllib.request.quote(username) 
    driver.get("http://tieba.baidu.com/home/main?un="+urlusername+"&fr=home")
    driver.find_element_by_class_name("u_login").click()
    time.sleep(0.5)
    driver.find_element_by_id("TANGRAM__PSP_10__userName").send_keys(username)
    driver.find_element_by_id("TANGRAM__PSP_10__password").send_keys(password)
    driver.find_element_by_id("TANGRAM__PSP_10__submit").click()
    time.sleep(3)

def my_tie_collector():  
    driver.get("http://tieba.baidu.com/i/i/my_tie")
    listOfLinks=list()
    listOfElements=driver.find_elements_by_class_name("thread_title")
    for i in range(0,len(listOfElements)-1):
        listOfLinks.append(listOfElements[i].get_attribute("href"))

    driver.get("http://tieba.baidu.com/i/i/my_tie?&pn=2")  #注意每天限制30贴，所以最多前两页就足够了
    listOfElements=driver.find_elements_by_class_name("thread_title")
    for i in range(0,len(listOfElements)-1):
        listOfLinks.append(listOfElements[i].get_attribute("href"))

    print("Links of Tie Collected")
    return listOfLinks

def my_reply_collector():
    driver.get("http://tieba.baidu.com/i/i/my_reply")
    listOfLinks=list()
    listOfElements=driver.find_elements_by_class_name("for_reply_context")
    for i in range(0,len(listOfElements)-1):
        listOfLinks.append(listOfElements[i].get_attribute("href"))

    driver.get("http://tieba.baidu.com/i/i/my_reply?&pn=2")  #同上
    listOfElements=driver.find_elements_by_class_name("for_reply_context")
    for i in range(0,len(listOfElements)-1):
        listOfLinks.append(listOfElements[i].get_attribute("href"))

    print("Links of Reply Collected")
    return listOfLinks

def deleter(listOfLinks):
    print("Now Deleting")
    for i in range(0,len(listOfLinks)-1):
        try:
            driver.get(listOfLinks[i])
            element=driver.find_element_by_class_name("p_post_del_my")
            driver.execute_script("arguments[0].scrollIntoView(false);", element)
            element.click()
            time.sleep(0.1)                  
            driver.find_element_by_class_name("dialogJanswers").find_element_by_tag_name("input").click()
            print("Deleted")
        except common.exceptions.NoSuchElementException:
            print("Fail to find the element") #古老版本匿名,或者隐藏帖子没有删除按钮

def Start_with_Chrome():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2} #不加载图片
    chrome_options.add_experimental_option("prefs",prefs)
    driver=webdriver.Chrome(chrome_options=chrome_options)
    return driver

driver=Start_with_Chrome()
login("Here is your username","Here is your password")
deleter(my_reply_collector()) #Or my_tie_collector()