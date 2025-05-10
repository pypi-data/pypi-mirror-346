from typing import Union
from platformeb.types import element_type_literal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from platformeb.driver import DriverInterface
from platformeb.pages.abstract_page import ABCPageInterface
from platformeb.utils.logger import get_logger


class WebPage(ABCPageInterface):
    def __init__(self, driver_interface: DriverInterface, timeout: int = 10):
        super().__init__(driver_interface)
        self.driver: webdriver = driver_interface.driver
        self.timeout = timeout
        self._logger = get_logger(__name__)
        self.driver.implicitly_wait(timeout)

    def get_element_by_text(self, text: str = None, element_type: element_type_literal = "all", multiple: bool = False, placeholder: str = None) -> \
    Union[list[WebElement], WebElement, None]:
        elements = []
        try:
            if element_type == "all":
                # Retrieve all elements in a single request and filter them
                all_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
                elements.extend(all_elements)
            elif element_type == "span":
                elements = self.driver.find_elements(By.XPATH, f"//span[contains(text(), '{text}')]")
            elif element_type == "textarea":
                if placeholder:
                    elements = self.driver.find_elements(By.XPATH, f"//textarea[@placeholder='{placeholder}']")
                else:
                    elements = self.driver.find_elements(By.XPATH, f"//textarea[contains(text(), '{text}')]")
            elif element_type == "input":
                if placeholder:
                    elements = self.driver.find_elements(By.XPATH, f"//input[@placeholder='{placeholder}']")
                else:
                    elements = self.driver.find_elements(By.XPATH, f"//input[contains(@value, '{text}')]")
            elif element_type == "button":
                elements = self.driver.find_elements(By.XPATH, f"//button[contains(text(), '{text}')]")
            elif element_type == "div":
                elements = self.driver.find_elements(By.XPATH, f"//div[contains(text(), '{text}')]")
            elif element_type == "p":
                elements = self.driver.find_elements(By.XPATH, f"//p[contains(text(), '{text}')]")
            else:
                self._logger.warning(f"Unsupported element type: {element_type}")
                return None

            if multiple:
                return elements
            else:
                return elements[0] if elements else None
        except Exception as e:
            self._logger.error(f"Error finding element by text '{text}' and type '{element_type}': {e}")
            return None

    def get_element_by_type(self, element_type: element_type_literal, multiple: bool = False) -> Union[
        list[WebElement], WebElement, None]:
        elements = []
        try:
            if element_type == "span":
                elements = self.driver.find_elements(By.TAG_NAME, "span")
            elif element_type == "textarea":
                elements = self.driver.find_elements(By.TAG_NAME, "textarea")
            elif element_type == "input":
                elements = self.driver.find_elements(By.TAG_NAME, "input")
            elif element_type == "button":
                elements = self.driver.find_elements(By.TAG_NAME, "button")
            elif element_type == "div":
                elements = self.driver.find_elements(By.TAG_NAME, "div")
            elif element_type == "p":
                elements = self.driver.find_elements(By.TAG_NAME, "p")
            else:
                self._logger.warning(f"Unsupported element type: {element_type}")
                return None

            if multiple:
                return elements
            else:
                return elements[0] if elements else None
        except Exception as e:
            self._logger.error(f"Error finding elements by type '{element_type}': {e}")
            return None