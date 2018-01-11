from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

class Translator(object):

    def __init__(self):
        options = Options()
        options.add_argument("-headless")
        self.driver = webdriver.Firefox(executable_path='./bin/geckodriver', firefox_options=options)
        self.went_to_home = False

    def _translate_from_home(self, text, to):
        self.went_to_home = True
        self.driver.get("https://www.google.com.br/")
        elem = self.driver.find_element_by_name('q')
        elem.clear()
        elem.send_keys("tradução {}".format(to))
        elem.send_keys(Keys.RETURN)
        sleep(2)

        return self._translate_from_search(text)

    def _translate_from_search(self, text, to=None):
        if to:
            search_elem = self.driver.find_element_by_name('q')
            search_elem.clear()
            search_elem.send_keys("tradução {}".format(to))
            search_elem.send_keys(Keys.RETURN)
            sleep(2)

        elem = self.driver.find_element_by_css_selector("textarea#tw-source-text-ta")
        elem.clear()
        elem.send_keys(text)
        sleep(2)
        return self._get_text_translation()

    def _get_text_translation(self):
        elem_bigger = self.driver.find_element_by_css_selector("#tw-target-text span")
        elem_smaller = self.driver.find_element_by_css_selector("#tw-target-rmn span")
        lang = elem_bigger.get_attribute("lang")

        if elem_smaller.text:
            return {
                "lang" : lang,
                "ideogram": elem_bigger.text,
                "latin" : elem_smaller.text
            }

        return {
            "lang" : lang,
            "latin": elem_bigger.text
        }

    def translate(self, text, to=None):
       if not self.went_to_home:
           return self._translate_from_home(text,to)

       return self._translate_from_search(text,to)

    def close(self):
        self.driver.quit()
       # Go to google home page, if it is first time 

    #driver.get('https://translate.google.com/m/translate?hl=pt-BR')
    #elem = driver.find_element_by_id('source')
    #elem.send_keys("Mas que belo dia, não é mesmo?")



