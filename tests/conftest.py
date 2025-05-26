import pytest # type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
import os
import time
import base64

@pytest.fixture(scope="session")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(r'--user-data-dir=C:\Users\ahmad\AppData\Local\Google\Chrome\User Data')
    chrome_options.add_argument('--profile-directory=Default')  # Or 'Profile 1', etc.
    service = Service('chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver is not None:
            screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(screenshot_path)

    # Attach screenshot to pytest-html report
    if 'pytest_html' in item.config.pluginmanager.list_name_plugin():
        pytest_html = item.config.pluginmanager.getplugin('html')
        if pytest_html:
            with open(screenshot_path, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode("utf-8")
            extra = getattr(rep, "extra", [])
            extra.append(pytest_html.extras.image(img_base64, mime_type="image/png"))
            rep.extra = extra
            rep.html = f'<div><img src="data:image/png;base64,{img_base64}" alt="Screenshot" style="width: 100%; height: auto;"></div>'
            rep.description = f'<div><img src="data:image/png;base64,{img_base64}" alt="Screenshot" style="width: 100%; height: auto;"></div>'

# To generate the report, run the following command in your terminal:
# pytest --html=reports/report.html --self-contained-html