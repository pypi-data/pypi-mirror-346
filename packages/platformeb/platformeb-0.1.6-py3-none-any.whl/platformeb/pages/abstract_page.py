from abc import ABC, abstractmethod

from platformeb.types import element_type_literal
from platformeb.driver import DriverInterface
from platformeb.utils.logger import logger
from typing import Union
from appium.webdriver.webelement import WebElement

class ABCPageInterface(ABC):
    def __init__(self, driver_interface: DriverInterface, timeout: int = 10):
        self.driver = driver_interface.driver
        self.timeout = timeout
        self._logger: logger

    @abstractmethod
    def get_element_by_text(self, text: str, element_type: element_type_literal, multiple: bool = False) -> Union[list[WebElement], WebElement]:
        pass

    @abstractmethod
    def get_element_by_type(self, element_type: element_type_literal, multiple: bool = False) -> Union[list[WebElement], WebElement]:
        pass
