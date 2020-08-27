from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


unix_to_google = {
    "zh": "zh-CN"
}

wait_time = 10


class Translator:
    """
    Usage:

    >>> t = Translator()
    >>> t.translate('Hello world!', 'en', 'ru')
    >>> # where 'en' and 'ru' --- Unix locales
    """

    def __init__(self):
        self.from_locale = None
        self.to_locale = None

        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, wait_time)

    def __choose_locale__(self, state, locale):
        self.driver.find_element_by_class_name(f'{state}-more').click()

        search_box = self.driver.find_element_by_id(f'{state}_list-search-box')

        search_box.click()
        search_box.send_keys(Keys.ARROW_DOWN)

        locale_start_position_in_html_element = 54

        while not (
            self
            .__active_element__()
            .get_attribute('class')
            .startswith(locale, locale_start_position_in_html_element)
        ):
            self.__active_element__().send_keys(Keys.ARROW_DOWN)

        self.__active_element__().click()

    def __choose_to_locale__(self, to_locale):
        self.to_locale = to_locale
        self.__choose_locale__('tl', to_locale)

    def __choose_from_locale__(self, from_locale):
        self.from_locale = from_locale
        self.__choose_locale__('sl', from_locale)

    def __active_element__(self):
        return self.driver.switch_to.__active_element__

    def __raise_error__(self):
        message = 'You have not chosen'

        message += '' if self.from_locale else ' from_locale'

        if not self.from_locale and not self.to_locale:
            message += ' and'

        message += '' if self.to_locale else ' to_locale'

        raise RuntimeError(message)

    def translate(self, text, from_locale=None, to_locale=None):
        """
        Translates 'text' from 'from_locale' language to 'to_locale' language.

        It does not select locales if they already were selected.
        """

        self.driver.get("https://translate.google.com/")

        if from_locale and self.from_locale != from_locale:
            self.__choose_from_locale__(from_locale)

        if to_locale and self.to_locale != to_locale:
            self.__choose_to_locale__(to_locale)

        if not self.from_locale or not self.to_locale:
            self.__raise_error__()

        input_field = self.driver.find_element_by_id('source')
        input_field.send_keys(text)

        output_field = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tlid-translation'))
        )

        return output_field.text

    def __del__(self):
        self.driver.quit()
