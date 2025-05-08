from abc import ABC, abstractmethod
from platformeb.driver import DriverInterface
from platformeb.utils.logger import logger
from typing import Union
from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.webelement import WebElement

class ABCPageInterface(ABC):
    def __init__(self, driver_interface: DriverInterface, timeout: int = 10, url: str = None):
        self.driver = driver_interface.driver
        self.timeout = timeout
        self.url = url
        self._logger: logger

    @abstractmethod
    def get_element_by_text(self, text: str, element_type, multiple: bool = False) -> Union[WebElement]:
        pass

    @abstractmethod
    def get_element_by_type(self, element_type: str, multiple: bool = False) -> Union[str, object]:
        pass
