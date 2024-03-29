import logging
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

DRIVERS = os.path.expanduser('~/WebDriver')
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
                    filename='info.log')


def pytest_addoption(parser):
    parser.addoption("--executor", action="store", default="192.168.1.34")
    parser.addoption("--maximized", action='store_true', default=False)
    parser.addoption("--headless", action='store_true', default=False)
    parser.addoption("--browser", action='store', choices=["chrome", "firefox", "MicrosoftEdge"], default='chrome')
    parser.addoption("--ver", action="store", default="107.0")
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--videos", action="store_true", default=False)
    parser.addoption("--url", action='store', default="https://demo.opencart.com/", help="destination url")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    ver = request.config.getoption("--ver")
    headless = request.config.getoption("--headless")
    maximized = request.config.getoption("--maximized")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    videos = request.config.getoption("--videos")
    logger = logging.getLogger('browseLogger')
    test_name = request.node.name
    url = request.config.getoption("--url")

    logger.info(f"===> Test {test_name} started")

    if executor == "local":
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            options.headless = headless
            driver = webdriver.Chrome(options=options)
        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            options.headless = headless
            options.binary_location = r'/usr/bin/firefox'
            driver = webdriver.Firefox(options=options)
        elif browser == 'MicrosoftEdge':
            options = webdriver.EdgeOptions()
            options.binary_location = r'/usr/bin/microsoft-edge'
            driver = webdriver.ChromiumEdge(options=options)


        else:
            raise ValueError('driver not supported: {}'.format(browser))

        if maximized:
            driver.maximize_window()

        driver = EventFiringWebDriver(driver, MyListener())

        def fin():
            driver.quit()
            logger.info(f"===> Test {test_name} finished")

        request.addfinalizer(fin)
        driver.url = url
        return driver

    else:
        exe_url = f"http://{executor}:4444/wd/hub"

        caps = {
            "browserName": browser,
            "browserVersion": ver,
            "screenResolution": "1280x720",
            "name": "Anton",
            "selenoid:options": {
                "enableVNC": vnc,
                "enableVideo": videos,
                "enableLog": logs
            },
            'acceptSslCerts': True,
            'acceptInsecureCerts': True,
            'timeZone': 'Europe/Moscow',
            'goog:chromeOptions': {}
        }

        driver = webdriver.Remote(
            command_executor=exe_url,
            desired_capabilities=caps
        )

        if maximized:
            driver.maximize_window()
        driver.url = url

    driver = EventFiringWebDriver(driver, MyListener())

    def end():
        driver.quit()
        logger.info(f"===> Test {test_name} finished")

    request.addfinalizer(end)
    return driver


class MyListener(AbstractEventListener):
    def on_exception(self, exception, driver):
        logging.error(f'I got: {exception}')
        allure.attach(
            name=driver.session_id,
            body=driver.get_screenshot_as_png(),
            attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope="session", autouse=True)
def get_environment(pytestconfig):
    browser_name = pytestconfig.getoption("--browser")
    browser_ver = pytestconfig.getoption("--ver")
    props = {
        'Browser': f'{browser_name} {browser_ver}',
        'Stand': os.name

    }

    tests_root = pytestconfig.rootdir
    with open(f'{tests_root}/allure-results/environment.properties', 'w') as f:
        for k, v in props.items():
            f.write(f'{k}={v}\n')
