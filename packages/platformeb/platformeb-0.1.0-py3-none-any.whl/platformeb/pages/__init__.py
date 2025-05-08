from platformeb.pages.web_page import WebPage
from platformeb.driver import DriverInterface
from platformeb.pages.page import PageInterface


class Page:
    def __init__(self, driver_interface: DriverInterface, timeout: int = 10, url: str = None):
        self.interface: PageInterface
        if driver_interface.platform == "web":
            self.interface = WebPage(driver_interface, timeout, url)