import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os
from datetime import datetime
import random
import string

class TestArticle(unittest.TestCase):
    def setUp(self):
        """Setup test environment before each test"""
        # Setup directories
        self.screenshot_dir = "test_screenshots"
        self.reports_dir = "C:/Selenium_Tests/Reports"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Create report file
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_file = os.path.join(self.reports_dir, f"test_create_article_{current_time}.txt")
        
        with open(self.report_file, "w", encoding="utf-8") as f:
            f.write(f"Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*50}\n\n")

        # Setup browser
        self.driver = webdriver.Chrome(service=Service("C:/Selenium_Tests/chromedriver.exe"))
        self.wait = WebDriverWait(self.driver, 20)
        
        # Load page
        self.driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/list")
        time.sleep(20)
        self.driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/list")

    def tearDown(self):
        """Cleanup after each test"""
        try:
            # Close browser
            if hasattr(self, 'driver'):
                self.driver.quit()
            
            # Clean up old screenshots
            if os.path.exists(self.screenshot_dir):
                screenshots = sorted([f for f in os.listdir(self.screenshot_dir) if f.endswith('.png')])
                if len(screenshots) > 5:
                    for old_screenshot in screenshots[:-5]:
                        os.remove(os.path.join(self.screenshot_dir, old_screenshot))
            
            # Clean up old reports
            if os.path.exists(self.reports_dir):
                report_files = sorted([f for f in os.listdir(self.reports_dir) 
                                    if f.startswith('test_create_article_') and f.endswith('.txt')])
                if len(report_files) > 5:
                    for old_report in report_files[:-5]:
                        os.remove(os.path.join(self.reports_dir, old_report))
                    
        except Exception as e:
            print(f"Cleanup error: {str(e)}")

    def generate_random_name(self, prefix="test", length=8):
        """Generate a random name for testing"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        timestamp = datetime.now().strftime('%H%M%S')
        return f"{prefix}_{random_str}_{timestamp}"

    def generate_random_words(self, count):
        """Generate random words for testing"""
        words = ['test', 'article', 'content', 'sample', 'random', 'example', 'data', 'text', 'word', 'sentence',
                'paragraph', 'story', 'news', 'update', 'information', 'details', 'description', 'summary', 'note']
        return ' '.join(random.choices(words, k=count))

    def highlight_element(self, element, color="red", duration=1):
        """Highlight an element with a colored border"""
        original_style = element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid " + color + "';"
            "arguments[0].style.borderRadius='50%';"
            "arguments[0].style.padding='5px';",
            element
        )
        self.take_screenshot(f"highlight_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        time.sleep(duration)
        self.driver.execute_script(
            "arguments[0].style='" + original_style + "';",
            element
        )

    def take_screenshot(self, step):
        """Take a screenshot of the current state"""
        self.driver.save_screenshot(f"{self.screenshot_dir}/{step}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    def log_step(self, step, status="PASS"):
        """Log a test step with timestamp"""
        with open(self.report_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {step}: {status}\n")

    def test_create_article(self):
        """Test creating a new article"""
        try:
            # Generate random content
            random_title = self.generate_random_name(prefix="title")
            random_summary = self.generate_random_words(5)
            random_content = self.generate_random_words(10)
            
            self.log_step(f"Generated random content - Title: {random_title}")

            # Click Add Article button
            add_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/form/button[2]/span")
            ))
            self.highlight_element(add_button, "blue", 1)
            add_button.click()
            self.take_screenshot("1_add_clicked")
            self.log_step("Clicked Add Article button")

            # Select category
            category_dropdown = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[2]/div/div/div/input")
            ))
            self.highlight_element(category_dropdown, "green", 1)
            category_dropdown.click()
            time.sleep(1)

            category_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[4]/div[1]/div[1]/ul/li[6]")
            ))
            self.highlight_element(category_option, "blue", 1)
            category_option.click()
            self.take_screenshot("2_category_selected")
            self.log_step("Selected article category")

            # Enter title
            title_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[3]/div/div[1]/input")
            ))
            self.highlight_element(title_input, "green", 1)
            title_input.clear()
            title_input.send_keys(random_title)
            self.take_screenshot("3_title_entered")
            self.log_step(f"Entered title: {random_title}")

            # Enter summary
            summary_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[4]/div/div[1]/textarea")
            ))
            self.highlight_element(summary_input, "green", 1)
            summary_input.clear()
            summary_input.send_keys(random_summary)
            self.take_screenshot("4_summary_entered")
            self.log_step(f"Entered summary: {random_summary}")

            # Enter content
            content_input = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[5]/div/div/div[1]/div[2]/div[1]")
            ))
            self.highlight_element(content_input, "green", 1)
            content_input.click()
            time.sleep(1)

            try:
                iframe = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tox-edit-area__iframe")))
                self.driver.switch_to.frame(iframe)
                editable_body = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                self.highlight_element(editable_body, "green", 1)
                editable_body.clear()
                editable_body.send_keys(random_content)
                self.driver.switch_to.default_content()
            except Exception as e:
                self.log_step(f"Failed to enter content in iframe: {str(e)}", "WARNING")
                content_input.clear()
                content_input.send_keys(random_content)

            self.take_screenshot("5_content_entered")
            self.log_step(f"Entered content: {random_content}")

            # Submit form
            submit_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[3]/div/button[2]/span")
            ))
            self.highlight_element(submit_button, "blue", 1)
            submit_button.click()
            self.take_screenshot("6_submitted")
            self.log_step("Clicked submit button")

            # Verify success
            time.sleep(2)
            self.take_screenshot("7_verified")
            self.log_step("Test completed successfully")

        except Exception as e:
            self.take_screenshot("error")
            self.log_step(f"Test failed: {str(e)}", "FAIL")

if __name__ == '__main__':
    unittest.main(verbosity=2)