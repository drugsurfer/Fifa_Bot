from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
from multipledispatch import dispatch
from selenium.common.exceptions import NoSuchElementException

class Browser:
    def __init__(self):
        self.time_action = 2
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.browser = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver', options=options)

    def getInfo(self, url):
        self.browser.get(url)
        self.randomDelay()

    def getHTML(self):
        return self.browser.page_source

    @dispatch(webdriver.remote.webelement.WebElement)
    def clickButton(self, element):
        self.randomDelay()
        element.click()
        self.randomDelay()

    @dispatch(str)
    def clickButton(self, xpath):
        self.randomDelay()
        element = self.browser.find_element(By.XPATH, xpath)
        #element.location_once_scrolled_into_view
        element.click()
        self.randomDelay()

    def clickHiddenButton(self, xpath_child, xpath_parent):
        if xpath_child != '' and xpath_parent != '':
            self.randomDelay()
            WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_parent))).click()
            self.randomDelay()
            element = self.browser.find_element(By.XPATH, xpath_child)
            # element.location_once_scrolled_into_view
            element.click()
            self.randomDelay()

    def clickAutorizationButton(self, xpath): # доделать потому что данные могут быть ошибочные
        flag = True
        while flag:
            self.randomDelay()
            element = self.browser.find_element(By.XPATH, xpath)
            # element.location_once_scrolled_into_view
            element.click()
            WebDriverWait(driver=self.browser, timeout=10).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
            error_message = ['Email address is invalid', '    Your credentials are incorrect or have expired. Please try again or reset your password.']
            errors = self.browser.find_elements(By.CLASS_NAME, 'otkinput-errormsg')
            if len(errors) == 0:
                break
            for err in errors:
                if err.text in error_message:
                    flag = True
                else:
                    flag = False


    def inputForm(self, xpath, text):
        self.randomDelay()
        self.browser.find_element(By.XPATH, xpath).click()
        self.randomDelay()
        self.browser.find_element(By.XPATH, xpath).send_keys(text)

    def onClickableElement(self, xpath):
        return self.browser.find_element(By.XPATH, xpath).is_enabled()

    def randomDelay(self):
        sleep(random.uniform(1.0, random.uniform(1.0, self.time_action)))

    def parseResultByClass(self, className):
        return self.browser.find_elements(By.CLASS_NAME, className)

    def search_attention(self, name):# проверяет наличие ошибки которая может вылезти при покупке карты
        try:
            element = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, name))
            )
            return False
        except Exception: # /html/body/div[5]/div
            return True
