import logging
import os
from time import sleep

import pyautogui
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException,
                                        InvalidElementStateException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

config = load_dotenv()

# config items
CITRIX_URL = os.getenv("URL")
EMAIL = os.getenv("CEC")
CEC_PASSWORD = os.getenv("CEC_PWD")
CITRIX_PASSWORD = os.getenv("CITRIX_PWD")


def get_logger(name, log_level="INFO"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(log_level))
    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    return logger


logger = get_logger("citrix_logging")


def open_webdriver(url):
    logger.info("open_webdriver(): initiating webdriver")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-default-apps")
    # dont allow browser closure
    options.add_experimental_option("detach", True)
    options.add_argument("--window-position=50,0")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    return driver


def wait_for_element_presence(driver, element_id):
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    return True


def is_element_clickable(driver, element_id):
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, element_id)))
    return True


def login():
    logger.info("main login():")
    driver = open_webdriver(url=CITRIX_URL)
    try:
        # wait till email textbox appears
        if wait_for_element_presence(driver, "userInput"):
            sleep(2)
            # add email to textbox
            email_area = driver.find_element(By.ID, "userInput")
            logger.info("Adding email to textbox")
            email_area.send_keys(EMAIL)
            logger.info("Sending enter")
            email_area.send_keys(Keys.ENTER)

        if wait_for_element_presence(driver, "passwordInput"):
            password_area = driver.find_element(By.ID, "passwordInput")
            logger.info("sending password")
            logger.info("Waiting for password elem to be interactable")
            sleep(3)
            password_area.send_keys(CEC_PASSWORD)
            password_area.send_keys(Keys.ENTER)
        
        logger.info("Please complete the SSO DUO Push, the script will pick up next steps automatically")
        # wait for SSO Duo push to complete
        # citrix gateway login
        if wait_for_element_presence(driver, "passwd"):
            pwd_area = driver.find_element(By.ID, "passwd")
            pwd_area.send_keys(CITRIX_PASSWORD)
            logon = driver.find_element(By.ID, "Log_On")
            logger.info("Clicking Log On")
            logon.click()

        # detecting receiver
        if is_element_clickable(driver, "protocolhandler-welcome-installButton"):
            detect_driver = driver.find_element(
                By.ID, "protocolhandler-welcome-installButton"
            )
            detect_driver.click()
            sleep(3)
            logger.info("clicking on cancel pop up")
            pyautogui.click(580, 260)
            sleep(2)
            logger.info("looking for already installed link")

        if wait_for_element_presence(
            driver, "protocolhandler-detect-alreadyInstalledLink"
        ):
            already_installed = driver.find_element(
                By.ID, "protocolhandler-detect-alreadyInstalledLink"
            )
            logger.info("clicking already installed")
            already_installed.click()

        if is_element_clickable(driver, "desktopsBtn"):
            desktop_tab = driver.find_element(By.ID, "desktopsBtn")
            logger.info("Clicking on desktop tabs")
            desktop_tab.click()

        logger.info("Waiting for CMS HSD image")

        WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[alt="CMS HSD"]'))
        )
        logger.info("looking for for CMS HSD image")
        cms_hsd = driver.find_element(By.CSS_SELECTOR, '[alt="CMS HSD"]')
        logger.info("clicking on CMS HSD desktop icon")
        cms_hsd.click()
        sleep(2)
        logger.info("Clicking on downloaded ICA file")
        pyautogui.click(150, 1090)
        logger.info("Logging successful. Check your Citrix workspace window!!!")
    except (
        TimeoutException,
        NoSuchElementException,
        ElementNotInteractableException,
        InvalidElementStateException,
    ) as se:
        logger.error("Selenium exception occured:", str(se))
    except Exception as e:
        logger.error("Exception occured: ", str(e))


if __name__ == "__main__":
    login()
