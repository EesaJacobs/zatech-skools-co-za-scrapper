from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.chrome.options import Options
import pandas as pd

class LambdaFunction:
    
    def __init__(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.page_urls: List[str] = []
        self.browser = webdriver.Chrome(service=Service(executable_path="./chromedriver"), options=chrome_options)
        self.loading_indicator = None
        self.loadmore_button = None
        
    def handle_event(self, event, context):
        # print("handle_event start")

        self.browser.get('https://skools.co.za/')
        self.loading_indicator = self.browser.find_element(By.CLASS_NAME, "jet-listing-grid__loader-text")
        self.loadmore_button = self.browser.find_element(By.ID, "loadmore")

        self.load_more_indefinitely(page_number=1)
        self.generate_page_urls()

        pd.DataFrame(self.page_urls).to_csv('page_urls.csv', index=False, header=False)

        # print("handle_event end")


    def load_more_indefinitely(self, page_number = 1):
        # scroll to the bottom of the page
        # to the button's expected location
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        if(self.loadmore_button is not None and self.loadmore_button.is_displayed() and self.loadmore_button.is_enabled() and page_number < 10):
            print(f"About to click `Load More..` on Page #{page_number}")
            try:
                self.loadmore_button.click()
            except Exception as e:
                print("Error occured while trying to move and click the load more button")
                raise e
            self.wait_for_invisibility_of_loading_indicator()

            # try and load more
            self.load_more_indefinitely(page_number=(page_number + 1))


    def wait_for_invisibility_of_loading_indicator(self):
        try:
            # self.browser.get_screenshot_as_file("wait_for_invisibility_of_loading_indicator.png")
            # loading_indicator_text = self.browser.find_element(By.CLASS_NAME, "jet-listing-grid__loader-text")
            if(self.loading_indicator is not None and self.loading_indicator.is_displayed()):
                WebDriverWait(self.browser, 120).until(
                    ExpectedConditions.invisibility_of_element_located(self.loading_indicator)
                )
        except Exception as e:
            print("Error occurred while waiting for loading indicator to become invisibile.")
            raise e


    def generate_page_urls(self):
        print("about to generate page urls")
        self.page_urls = []

        listing_elements = self.browser.find_elements(By.CLASS_NAME, "jet-listing-grid__item")

        for listing_element in listing_elements:
            wrapper_element = listing_element.find_element(By.XPATH, "./div[1]")
            page_url = wrapper_element.get_attribute("data-url")
            self.page_urls.append(page_url)

def lambda_handler(event, context):
    try:
        LambdaFunction().handle_event(event=event, context=context)
        return None
    except Exception as exception:
        print(exception)
        return None