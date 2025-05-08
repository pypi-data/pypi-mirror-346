from selenium import webdriver as selenium_webdriver

import time

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.core.os_manager import ChromeType

from appium import webdriver as appium_webdriver

# Note: Safari does not require a driver manager as it uses the built-in WebDriver
from platformeb.utils.logger import get_logger
import subprocess
from typing import Literal, Optional

platform_literal = Literal['android', 'ios', "web"]
browsers_literal = Literal['chrome', 'firefox', 'safari', 'edge', 'brave']


class DriverInterface:
    def __init__(self, platform: platform_literal, appium_server_url: Optional[str] = None,
                 selenium_server_url: Optional[str] = None, browser: Optional[browsers_literal] = None,
                 app_path: Optional[str] = None, desired_capabilities: Optional[dict] = None, debug: bool = False,
                 save_extension_url: bool = True):
        self._logger = get_logger(__name__)

        self.devices: list[str]
        self.platform: platform_literal = platform
        self._appium_server_url: Optional[str] = appium_server_url
        self._selenium_server_url: Optional[str] = selenium_server_url
        self._app_path: Optional[str] = app_path
        self._desired_capabilities: Optional[dict] = desired_capabilities
        self._debug: bool = debug
        self._save_extension_url: bool = save_extension_url
        self.extension_link: Optional[str] = None
        self.browser: Optional[browsers_literal] = browser
        self.driver: Optional[selenium_webdriver.Remote, appium_webdriver.Remote]
        self.extension_url: Optional[str] = None
        self._initialize_driver()

    def _get_adb_devices(self) -> list[Optional[str]]:
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')

            devices = []
            for line in lines[1:]:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) == 2 and parts[1] == 'device':
                        devices.append(parts[0])
            if self._debug:
                self._logger.debug(f"ADB devices found: {devices}")
            return devices
        except subprocess.CalledProcessError as e:
            raise Exception(f"{e}\n\nError while getting ADB devices.\nCheck if adb is installed on your device")

    def _initialize_driver(self):
        if self.platform == 'android':
            self.devices = self._get_adb_devices()
            if not self.devices:
                raise ValueError("No Android devices found.")
            if self._debug:
                self._logger.debug(f"Using first device: {self.devices[0]} from {self.devices}")
            ...
        elif self.platform == 'ios':
            ...
        elif self.platform == 'web':
            if not self._selenium_server_url:
                if self._debug:
                    self._logger.debug("No Selenium server URL provided. Setting up local server.")
                if self.browser:
                    try:
                        self.driver = self._create_browser()

                        if self._save_extension_url:
                            self.save_extension_id(driver=self.driver)
                            if self._debug:
                                self._logger.debug("Loaded extension with url: " + str(self.extension_url))
                    except Exception as e:
                        raise ValueError(
                            f"{e}\n\nFailed to create browser\nMake sure it's installed on your device or follow instructions to enable remote controlling")
            else:
                if self._debug:
                    self._logger.debug(f"Using Selenium server URL: {self._selenium_server_url}")



    def _create_browser(self):
        match self.browser:
            case 'chrome':
                chrome_options = ChromeOptions()
                if self._app_path:
                    chrome_options.add_argument(f"--load-extension={self._app_path}")

                driver = selenium_webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=chrome_options
                )
                return driver

            case 'firefox':
                firefox_options = FirefoxOptions()
                if self._app_path:
                    firefox_options.add_argument(f"-load-extension={self._app_path}")

                return selenium_webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=firefox_options
                )

            case 'safari':
                safari_options = SafariOptions()
                # Safari does not support extensions via WebDriver directly
                return selenium_webdriver.Safari(
                    service=SafariService(),
                    options=safari_options
                )

            case 'edge':
                edge_options = EdgeOptions()
                if self._app_path:
                    edge_options.add_extension(self._app_path)

                return selenium_webdriver.Edge(
                    service=EdgeService(EdgeChromiumDriverManager().install()),
                    options=edge_options
                )

            case 'brave':
                brave_options = ChromeOptions()
                if self._app_path:
                    brave_options.add_extension(self._app_path)

                return selenium_webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
                    options=brave_options
                )

            case 'opera':
                opera_options = ChromeOptions()
                if self._app_path:
                    opera_options.add_extension(self._app_path)

                return selenium_webdriver.Chrome(
                    service=ChromeService(OperaDriverManager().install()),
                    options=opera_options
                )

    def _connect_to_remote_webdriver(self):
       if self._selenium_server_url:
           match self.browser:
               case 'chrome':
                   options = ChromeOptions()
                   if self._app_path:
                       options.add_argument(f"--load-extension={self._app_path}")
                   return selenium_webdriver.Remote(
                       command_executor=self._selenium_server_url,
                       options=options
                   )
               case 'firefox':
                   options = FirefoxOptions()
                   if self._app_path:
                       options.add_argument(f"-load-extension={self._app_path}")
                   return selenium_webdriver.Remote(
                       command_executor=self._selenium_server_url,
                       options=options
                   )
               case 'safari':
                   options = SafariOptions()
                   return selenium_webdriver.Remote(
                       command_executor=self._selenium_server_url,
                       options=options
                   )
               case 'edge':
                   options = EdgeOptions()
                   if self._app_path:
                       options.add_extension(self._app_path)
                   return selenium_webdriver.Remote(
                       command_executor=self._selenium_server_url,
                       options=options
                   )
               case 'brave':
                   options = ChromeOptions()
                   if self._app_path:
                       options.add_extension(self._app_path)
                   return selenium_webdriver.Remote(
                       command_executor=self._selenium_server_url,
                       options=options
                   )
               case 'opera':
                   options = ChromeOptions()
                   if self._app_path:
                       options.add_extension(self._app_path)
                   return selenium_webdriver.Remote(
                       command_executor=self._selenium_server_url,
                       options=options
                   )
               case _:
                   raise ValueError(f"Unsupported browser: {self.browser}")

    def save_extension_id(self, driver, timeout: int = 40):

        url_prefix = "chrome-extension://"
        start_time = time.time()

        while time.time() - start_time < timeout:
            targets = driver.execute_cdp_cmd("Target.getTargets", {})
            for target in targets.get("targetInfos", []):
                url = target.get("url", "")
                if url.startswith(url_prefix):
                    ext_url = url_prefix + url.split("/")[2]
                    self.extension_url = ext_url
                    self._logger.debug("Loaded extension url:" + str(self.extension_url))
                    return
            time.sleep(1)  # Wait for 0.5 seconds before retrying

        self._logger.error("Failed to retrieve extension URL within the timeout period.")

    def __str__(self):
        return f"Driver(platform={self.platform}, browser={self.browser}, debug={self._debug}, appium_server_url={self._appium_server_url})"
