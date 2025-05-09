from typing import Literal, Union

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

    def get_element_by_text(self, text: str, element_type: Literal["all", "span", "textarea", "input"] = "all", multiple: bool = False) -> list[WebElement]:
        elements = []
        try:
            if element_type in ["all", "span"]:
                span_elements = self.driver.find_elements(By.XPATH, f"//span[contains(text(), '{text}')]")
                elements.extend(span_elements)

            if element_type in ["all", "textarea"]:
                textarea_elements = self.driver.find_elements(By.XPATH, f"//textarea[contains(text(), '{text}')]")
                elements.extend(textarea_elements)

            if element_type in ["all", "input"]:
                input_elements = self.driver.find_elements(By.XPATH, f"//input[contains(@value, '{text}')]")
                elements.extend(input_elements)

            if multiple:
                return elements
            else:
                return elements[0] if elements else []
        except Exception as e:
            self._logger.error(f"Error finding element by text '{text}' and type '{element_type}': {e}")
            return []

    def get_element_by_type(self, element_type: Literal["span", "textarea", "input"], multiple: bool = False) -> list[WebElement]:
        elements = []
        try:
            if element_type == "span":
                elements = self.driver.find_elements(By.TAG_NAME, "span")
            elif element_type == "textarea":
                elements = self.driver.find_elements(By.TAG_NAME, "textarea")
            elif element_type == "input":
                elements = self.driver.find_elements(By.TAG_NAME, "input")

            if multiple:
                return elements
            else:
                return elements[0] if elements else []
        except Exception as e:
            self._logger.error(f"Error finding elements by type '{element_type}': {e}")
            return []