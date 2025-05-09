import smtplib
import logging
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import os
from os.path import basename

import pyreadr
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

import psutil
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import requests
from .config import get_config

# Define COMMASPACE explicitly
COMMASPACE = ", "
config = get_config()
logger = logging.getLogger(__name__)


def readRDS(filename):
    data = pyreadr.read_r(filename)
    if data:
        return data[None]


def saveRDS(pd_file, path):
    with localconverter(ro.default_converter + pandas2ri.converter):
        r_from_pd_df = ro.conversion.py2rpy(pd_file)
    ro.r["saveRDS"](r_from_pd_df, path, version=2)


def send_mail(send_from, send_to, password, subject, text, files=None, is_html=False):
    if not isinstance(send_to, list):
        raise TypeError(f"Expected 'send_to' to be a list, got {type(send_to).__name__}")

    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = COMMASPACE.join(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    if is_html:
        msg.attach(MIMEText(text, "html"))  # Set the content type to HTML
    else:
        # Set the content type to plain text
        msg.attach(MIMEText(text, "plain"))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(send_from, password)
    server.sendmail(send_from, send_to, msg.as_string())
    server.close()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}


def get_session_or_driver(
    url_to_test,
    get_session=True,
    headless=False,
    desktop_session=4,
    proxy_source=None,
    api_key=None,
    proxy_user=None,
    proxy_password=None,
    country_code=None,
):
    """
    Use Selenium with Firefox to fetch cookies and headers from the website, then return the WebDriver.
    """

    def setup_driver_with_proxy_auth(proxy=None, proxy_user=None, proxy_pass=None):
        proxy_ip = None
        proxy_port = None
        if proxy:
            proxy_ip, proxy_port = proxy.split(":")

        # Configure Firefox options
        options = Options()
        options.set_preference("network.proxy.type", 1)  # Manual proxy config
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36",
        )

        if proxy_ip is not None and proxy_port is not None:
            options.set_preference("network.proxy.type", 1)  # Manual proxy config
            options.set_preference("network.proxy.http", proxy_ip)
            options.set_preference("network.proxy.http_port", int(proxy_port))
            options.set_preference("network.proxy.ssl", proxy_ip)
            options.set_preference("network.proxy.ssl_port", int(proxy_port))
            options.set_preference("network.proxy.no_proxies_on", "")  # No exclusions
            options.set_preference("media.peerconnection.enabled", False)  # Disable WebRTC to prevent IP leaks
        if proxy_user is not None and proxy_pass is not None:
            # Add proxy authentication
            options.set_preference("network.proxy.username", proxy_user)
            options.set_preference("network.proxy.password", proxy_pass)
        if headless:
            options.add_argument("--headless")
        else:
            os.environ["DISPLAY"] = f":{str(desktop_session)}"

        # Set up the WebDriver
        service = Service(config.get("driver_path"))
        driver = webdriver.Firefox(service=service, options=options)
        # Inject headers using JavaScript (if needed)
        for key, value in headers.items():
            driver.execute_script(f"Object.defineProperty(navigator, '{key}', {{get: () => '{value}'}});")
        return driver

    def setup_session_with_proxy_auth(
        proxy,
        proxy_user=None,
        proxy_password=None,
    ):
        if proxy_user and proxy_password:
            proxy_url = f"http://{proxy_user}:{proxy_password}@{proxy}"
            proxies = {"http": proxy_url, "https": proxy_url}
        elif proxy_source:
            proxy_url = f"http://{proxy}"
            proxies = {"http": proxy_url, "https": proxy_url}
        else:
            proxies = None
        s = requests.Session()
        if proxies:
            s.proxies.update(proxies)
        s.headers.update(headers)
        driver = setup_driver_with_proxy_auth(proxy, proxy_user, proxy_password)
        try:
            driver.get(url_to_test)  # Navigate to the target URL
            cookies = driver.get_cookies()
            for cookie in cookies:
                s.cookies.set(cookie["name"], cookie["value"], domain=cookie.get("domain"))
        finally:
            driver.quit()  # Ensure the WebDriver is closed
        return s

    def test_proxies(
        proxies,
        proxy_user=None,
        proxy_password=None,
        get_session=True,
        test_url="https://httpbin.org/ip",
    ):
        """
        Test a proxy with both WebDriver and requests.
        """

        # Test with WebDriver
        def test_with_webdriver(proxy, proxy_user, proxy_password):
            driver = setup_driver_with_proxy_auth(proxy, proxy_user, proxy_password)
            try:
                driver.get(test_url)
                return driver
            except Exception as e:
                print(f"WebDriver test failed: {e}")
                return None

        # Test with requests
        def test_with_requests(proxy, proxy_user, proxy_password):
            s = setup_session_with_proxy_auth(proxy, proxy_user, proxy_password)
            response = s.get(test_url)
            if response.status_code == 200:
                return s
            else:
                return None

        # Run both tests
        for proxy in proxies:
            if not get_session:
                out = test_with_webdriver(proxy, proxy_user, proxy_password)
            else:
                out = test_with_requests(proxy, proxy_user, proxy_password)
            if out:
                return out

    def get_proxy_country(ip_address):
        """
        Validate the actual country of a proxy using a third-party service.
        """
        try:
            # Use a third-party service like ipinfo.io or ip-api.com
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("countryCode")  # Returns the country code (e.g., "IN")
            else:
                logger.error(f"Failed to fetch country for IP {ip_address}. Status code: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error while fetching country for IP {ip_address}: {e}")
            return None

    def get_random_webshare_proxy(country_code=None, mode="direct"):
        if country_code:
            url = f"https://proxy.webshare.io/api/v2/proxy/list/?mode={mode}&page=1&page_size=100&country_code={country_code}"
        else:
            url = f"https://proxy.webshare.io/api/v2/proxy/list/?mode={mode}&page=1&page_size=100"

        proxies = []
        response = requests.get(url, headers={"Authorization": api_key})
        if response.status_code == 200:
            data = response.json()
            for proxy in data["results"]:
                if proxy["valid"]:
                    proxy_address = f"{proxy['proxy_address']}:{proxy['port']}"
                    # Validate the proxy's actual country
                    actual_country = get_proxy_country(proxy["proxy_address"])
                    if actual_country == country_code:
                        proxies.append(proxy_address)
        else:
            logger.error(f"Failed to retrieve proxies. Status code: {response.status_code}")
        return proxies

    def get_free_proxy(
        country_code=None,
    ):
        def kill_firefox_processes():
            for process in psutil.process_iter():
                try:
                    if process.name().lower() in ["firefox", "geckodriver"]:
                        process.kill()
                except psutil.NoSuchProcess:
                    continue

        def fetch_proxies(country_code=None):
            """Fetch proxies from sslproxies.org using Selenium."""
            options = Options()
            options.add_argument("--headless")
            service = Service(config.get("driver_path"))
            driver = webdriver.Firefox(service=service, options=options)

            try:
                logger.info("Fetching proxies from sslproxies.org...")
                driver.get("https://sslproxies.org")

                # Wait for the proxy table to load
                table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
                rows = table.find_elements(By.XPATH, ".//tbody/tr")

                # Parse the proxies
                proxies = []
                for row in rows:
                    columns = row.find_elements(By.TAG_NAME, "td")
                    if country_code is None or (
                        country_code is not None and get_proxy_country(columns[0].text.strip()) == country_code
                    ):
                        proxy = f"{columns[0].text.strip()}:{columns[1].text.strip()}"
                        proxies.append(proxy)
                return proxies

            except Exception as e:
                logger.info(f"Error fetching proxies: {e}")
                return []

            finally:
                driver.quit()
                kill_firefox_processes()

        """Get a list of proxies from sslproxies.org"""
        proxies = fetch_proxies(country_code)
        return proxies

    if proxy_source.lower() == "webshare":
        proxies = get_random_webshare_proxy(country_code=country_code)
    elif proxy_source.lower() == "sslhosts":
        proxies = get_free_proxy(country_code=country_code)
    else:
        proxies = None
    return test_proxies(proxies, proxy_user, proxy_password, get_session, url_to_test)
