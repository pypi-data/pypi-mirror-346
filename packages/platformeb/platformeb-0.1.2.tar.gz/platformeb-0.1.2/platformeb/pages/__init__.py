from platformeb.pages.web_page import WebPage
from platformeb.driver import DriverInterface
from platformeb.pages.abstract_page import ABCPageInterface


def get_interface(driver_interface: DriverInterface, timeout: int = 10, url: str = None) -> ABCPageInterface:
    """
    Factory function to get the appropriate page interface based on the driver type.
    """
    if driver_interface.platform == "web":
        return WebPage(driver_interface, timeout, url)
    else:
        raise ValueError(f"Unsupported platform: {driver_interface.platform}")