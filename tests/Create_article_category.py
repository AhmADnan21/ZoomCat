# Import required libraries
import unittest  # For creating test cases
from selenium import webdriver  # For browser automation
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.support.ui import WebDriverWait  # For explicit waits
from selenium.webdriver.support import expected_conditions as EC  # For expected conditions
from selenium.webdriver.chrome.service import Service  # For Chrome driver service
from selenium.webdriver.support.ui import Select  # For handling dropdown menus
from selenium.common.exceptions import TimeoutException  # For handling timeout exceptions
import time  # For adding delays and timestamps
import os
from datetime import datetime
import random
import string

class TestArticleCategory(unittest.TestCase):
    def setUp(self):
        """
        Setup test environment before each test
        This method runs before each test case
        """
        # Setup directories and report
        self.screenshot_dir = "test_screenshots"
        self.reports_dir = "C:/Selenium_Tests/Reports"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Create report file with new naming format
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_file = os.path.join(self.reports_dir, f"test_create_article_category_{current_time}.txt")
        
        with open(self.report_file, "w", encoding="utf-8") as f:
            f.write(f"Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*50}\n\n")

        # Setup browser
        self.driver = webdriver.Chrome(service=Service("C:/Selenium_Tests/chromedriver.exe"))
        self.wait = WebDriverWait(self.driver, 20)
        
        # Initial page load
        self.driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/categorization")
        time.sleep(20)
        self.driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/categorization")

    def generate_random_name(self, prefix="test", length=8):
        """
        Generate a random name for testing
        Format: prefix_randomstring_timestamp
        """
        # Generate random string
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        # Add timestamp to ensure uniqueness
        timestamp = datetime.now().strftime('%H%M%S')
        return f"{prefix}_{random_str}_{timestamp}"

    def tearDown(self):
        """
        Cleanup after each test
        """
        try:
            # Close the browser
            if hasattr(self, 'driver'):
                self.driver.quit()
            
            # Clean up old screenshots (keep only last 5 test runs)
            if os.path.exists(self.screenshot_dir):
                screenshots = sorted([f for f in os.listdir(self.screenshot_dir) if f.endswith('.png')])
                if len(screenshots) > 5:
                    for old_screenshot in screenshots[:-5]:
                        os.remove(os.path.join(self.screenshot_dir, old_screenshot))
            
            # Clean up old report files (keep only last 5 reports)
            if os.path.exists(self.reports_dir):
                report_files = sorted([f for f in os.listdir(self.reports_dir) 
                                    if f.startswith('test_create_article_category_') and f.endswith('.txt')])
                if len(report_files) > 5:
                    for old_report in report_files[:-5]:
                        os.remove(os.path.join(self.reports_dir, old_report))
                    
        except Exception as e:
            print(f"Cleanup error: {str(e)}")

    def highlight_element(self, element, color="red", duration=1):
        """
        Highlights an element with a colored border
        """
        # Store original style
        original_style = element.get_attribute("style")
        
        # Apply highlight style
        self.driver.execute_script(
            "arguments[0].style.border='3px solid " + color + "';"
            "arguments[0].style.borderRadius='50%';"
            "arguments[0].style.padding='5px';",
            element
        )
        
        # Take screenshot
        self.take_screenshot(f"highlight_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Wait for specified duration
        time.sleep(duration)
        
        # Restore original style
        self.driver.execute_script(
            "arguments[0].style='" + original_style + "';",
            element
        )

    def take_screenshot(self, step):
        self.driver.save_screenshot(f"{self.screenshot_dir}/{step}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    def log_step(self, step, status="PASS"):
        with open(self.report_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {step}: {status}\n")

    def test_add_article_category(self):
        """
        Test adding a new article category
        """
        try:
            # Generate random test name
            test_name = self.generate_random_name()
            self.log_step(f"Generated test name: {test_name}")

            # Click add button
            add_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/form/button[2]/span")
            ))
            self.highlight_element(add_button, "blue", 1)
            add_button.click()
            self.take_screenshot("1_add_clicked")
            self.log_step("Clicked Add button")

            # Enter category name
            name_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[2]/div/div[1]/input")
            ))
            self.highlight_element(name_input, "green", 1)
            name_input.clear()
            name_input.send_keys(test_name)
            self.take_screenshot("2_name_entered")
            self.log_step(f"Entered category name: {test_name}")

            # Enter sorting number
            sort_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[3]/div/div/input")
            ))
            self.highlight_element(sort_input, "green", 1)
            sort_input.clear()
            sort_input.send_keys("1")
            self.take_screenshot("3_sort_entered")
            self.log_step("Entered sorting number")

            # Click confirm
            confirm_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[3]/div/button[2]/span")
            ))
            self.highlight_element(confirm_button, "blue", 1)
            confirm_button.click()
            self.take_screenshot("4_confirmed")
            self.log_step("Clicked confirm")

            # Verify success
            table = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[1]/div[3]/table")
            ))
            self.highlight_element(table, "yellow", 1)
            self.take_screenshot("5_verified")
            self.log_step("Test completed successfully")

        except Exception as e:
            self.take_screenshot("error")
            self.log_step(f"Test failed: {str(e)}", "FAIL")

if __name__ == '__main__':
    unittest.main(verbosity=2)  # verbosity=2 provides detailed test output 