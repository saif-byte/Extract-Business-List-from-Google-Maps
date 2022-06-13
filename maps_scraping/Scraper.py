from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium. webdriver. common. keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time,csv, os , sys
import maps_scraping.constants as const

class Scraper(webdriver.Chrome):
    def __init__(self , driver_path='C:\\SeleniumDrivers\\chromedriver.exe', teardown = False):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option( 'excludeSwitches' , ['enable-logging'])
        self.driver_path = driver_path
        self.teardown = teardown
        super(Scraper , self).__init__(options = options ,executable_path=self.driver_path)
        self.delete_all_cookies()

        self.implicitly_wait(50)
        self.maximize_window()

    def __exit__(self, *args):
        if self.teardown:
            self.quit()
    
    def land_on_page(self):
        self.get(const.BASE_URL)

    

    def scroll(self):        
        last_review = self.find_elements_by_css_selector('div[jstcache="206"]')
        self.execute_script('arguments[0].scrollIntoView(true);', last_review[6])
        time.sleep(7)
        last_review = self.find_elements_by_css_selector('div[jstcache="206"]')
        self.execute_script('arguments[0].scrollIntoView(true);', last_review[9])
        time.sleep(7)
        last_review = self.find_elements_by_css_selector('div[jstcache="206"]')
        self.execute_script('arguments[0].scrollIntoView(true);', last_review[12])
        time.sleep(7)
        last_review = self.find_elements_by_css_selector('div[jstcache="206"]')
        self.execute_script('arguments[0].scrollIntoView(true);', last_review[15])
        time.sleep(7)
        last_review = self.find_elements_by_css_selector('div[jstcache="206"]')
        self.execute_script('arguments[0].scrollIntoView(true);', last_review[18])

    

    def __pull_business_boxes(self):
        #self.scroll()
        #self.execute_script("window.scrollTo(0, 1080)") 
        return self.find_elements_by_css_selector('div[jstcache="206"]')
        

    def __scroll_pop_up(self):
        elements = self.find_elements_by_css_selector(
            'div[class="RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L"]')
        self.execute_script('arguments[0].scrollIntoView(true);', elements[-1])

    def __get_name(self):
        try:        
            name_box = self.find_element_by_css_selector('div[class="tAiQdd"]')
            name = name_box.find_element_by_xpath('./div/div//h1//span').get_attribute(
                'innerHTML'
            )
        except Exception as e:
            name = None
        return name
    
    def __get_image(self):
        try:
            image_box = self.find_element_by_css_selector('div[class="ZKCDEc"]')
            image = image_box.find_element_by_xpath('./div//button//img').get_attribute('src')
        except Exception as e:
            image = None
        return image

    def __get_address(self):
        try:
            address_box = self.find_element_by_css_selector('div[class="rogA2c"]')
            address = address_box.find_element_by_xpath('./div').text
        except Exception as e:
            address = None
        return address

    def __get_timings(self):
        try:
            timing_box = self.find_element_by_css_selector('div[class="MkV9"]')
            timing_drop = timing_box.find_element_by_css_selector('span[aria-label="Show open hours for the week"]')
            timing_drop.click()
            time.sleep(2)
            timings = {}
            table = self.find_element_by_css_selector('table[class="eK4R0e fontBodyMedium"]')
            table_timings = self.find_elements_by_css_selector('tr[class="y0skZc"]')
            for day in table_timings:
                timings[day.find_element_by_xpath('.//td/div').text] = day.find_element_by_css_selector(
                    'li[class="G8aQO"]').text
        
            timing_drop.click()
        except Exception as e:
            timings = None
        return timings


    def __get_website(self):
        try:
            website_box = self.find_element_by_css_selector('button[data-tooltip="Open website"]')
            website = website_box.find_element_by_css_selector(
                'div[class="rogA2c ITvuef"]').find_element_by_xpath('./div').text
        except Exception as e:
            website = None
        return website

    def __get_phone(self):
        try:    
            phone_box = self.find_element_by_css_selector('button[data-tooltip="Copy phone number"]')
            phone = phone_box.find_element_by_css_selector(
                'div[class="rogA2c"]'
            ).find_element_by_xpath('./div').text
        except Exception as e:
            phone = None
        return phone

    def __get_rating(self):
        try:
            review_box = self.find_element_by_css_selector('div[class="PPCwl"]')
            review_box_2 = review_box.find_element_by_css_selector('div[class="jANrlb"]')
            rating = review_box_2.find_element_by_xpath('./div').text
            no_of_reviews = review_box_2.find_element_by_xpath('.//button').text
        except Exception as e:
            rating = None
            no_of_reviews = None
        return rating , no_of_reviews

    def __get_reviews(self):
        try:
            reviews = []
            text_reviews = self.find_elements_by_css_selector('div[class="tBizfc fontBodyMedium"]')
            for r in text_reviews:
                original_review = r.find_element_by_css_selector(
                    'div[role="button"]').find_element_by_xpath('./div')
                original_review_text = original_review.text
                reviews.append(original_review_text)
        except Exception as e:
            reviews = None
        return reviews

    def click_to_open(self):
        elements = self.__pull_business_boxes()
        csv_file = open(os.path.join(sys.path[0], "business_att.csv") , 'a',encoding='UTF-8')
        csv_writer = csv.writer(csv_file)
        
        for element in elements:
            element.click()
            time.sleep(3)
            image = self.__get_image()
            name = self.__get_name()
            address = self.__get_address()
            timings = self.__get_timings()
          
            self.__scroll_pop_up()
            website = self.__get_website()
            phone = self.__get_phone()
            rating , no_of_reviews = self.__get_rating()
            reviews = self.__get_reviews()
            
            
            csv_writer.writerow([name ,address , timings,website,phone,rating,no_of_reviews,reviews,image])
            
            time.sleep(2)


    def click_on_next_page(self):
        next_box = self.find_element_by_css_selector('div[class="punXpd"]')
        next_button = next_box.find_element_by_css_selector('button[jsaction="pane.paginationSection.nextPage"]')
        next_button.click()
        time.sleep(5)
    


