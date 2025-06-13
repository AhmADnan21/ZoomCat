"""
Selenium Test Automation for Full Flow Testing
This script automates the complete flow of:
1. Login
2. Create Article Category
3. Create Article
4. View Complaints
"""

# ===== Imports =====
from pathlib import Path
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.webdriver import WebDriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import pytest # type: ignore
import os
import base64
from unittest import mock
from conftest import pytest_runtest_makereport
from typing import Any
import time
from datetime import datetime
import random
import string

# ===== Global Configuration =====
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# ===== Utility Functions =====
def create_report_dir():
    """Creates a timestamped directory for test reports"""
    report_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_dir = os.path.join(report_dir, f"Full-Flow-test_run_{timestamp}")
    os.makedirs(test_dir)
    return test_dir

def take_screenshot(driver, step_name, report_dir):
    """Takes and saves a screenshot with the given step name"""
    screenshot_path = os.path.join(report_dir, f"{step_name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def highlight_and_wait(driver, element, wait_time=1):
    """Highlights an element with a red border and waits"""
    driver.execute_script("arguments[0].style.border='3px solid red'", element)
    time.sleep(wait_time)

def interact_with_element(driver, element, action, step_name, report_dir, wait_time=1, **kwargs):
    """Handles element interaction with screenshots and highlighting"""
    try:
        driver.execute_script("arguments[0].style.border='3px solid red'", element)
        time.sleep(1)
        
        if action == "click":
            element.click()
        elif action == "send_keys":
            element.send_keys(kwargs.get('keys', ''))
        elif action == "clear":
            element.clear()
        elif action == "submit":
            element.submit()
        
        time.sleep(wait_time)
        take_screenshot(driver, step_name, report_dir)
        
    except Exception as e:
        raise Exception(f"Failed to {action} element: {str(e)}")

def fast_key_press(driver, element, key, wait_time=0.1):
    """Fast version of key press without screenshots and minimal delays"""
    element.send_keys(key)
    time.sleep(wait_time)

# ===== Content Generation Functions =====
def generate_category_name():
    """Generates a unique category name using current timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}_{timestamp}"

def generate_article_title():
    """Generates a unique article title using current timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"title_{random_str}_{timestamp}"

def generate_random_words(count):
    """Generate random words for testing"""
    words = ['test', 'article', 'content', 'sample', 'random', 'example', 'data', 'text', 'word', 'sentence',
            'paragraph', 'story', 'news', 'update', 'information', 'details', 'description', 'summary', 'note']
    return ' '.join(random.choices(words, k=count))

# ===== Test Step Functions =====
def login(report_dir):
    """Handles the login process"""
    try:
        print("\n=== Starting login process ===")
        driver.get("https://sso.xiaoxitech.com/login?project=lwlu63w1&cb=https%3A%2F%2Ftest-admin-ipipgo.cd.xiaoxigroup.net%2Fapp-manager%2F")
        print("Navigated to login page")
        take_screenshot(driver, "01_login_page", report_dir)
        
        # Step 1: Click initial button
        try:
            print("\n--- Step 1: Clicking initial button ---")
            initial_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/form/div[2]/div/div/button/span')))
            print("Found initial button")
            interact_with_element(driver, initial_button, "click", "02_initial_button", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click initial button: {str(e)}")
            raise
        
        # Step 2: Wait for login form
        try:
            print("\n--- Step 2: Waiting for login form ---")
            login_form = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/form/div[4]/div/button/span')))
            print("Login form appeared")
            take_screenshot(driver, "03_login_form", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to find login form: {str(e)}")
            raise
        
        # Step 3: Enter username
        try:
            print("\n--- Step 3: Entering username ---")
            username_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/form/div[1]/div/div[1]/input')
            print("Found username input")
            interact_with_element(driver, username_input, "send_keys", "04_username_input", report_dir, keys="abdullahahmad")
        except Exception as e:
            print(f"ERROR: Failed to enter username: {str(e)}")
            raise
        
        # Step 4: Enter password
        try:
            print("\n--- Step 4: Entering password ---")
            password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/form/div[2]/div/div/input')
            print("Found password input")
            interact_with_element(driver, password_input, "send_keys", "05_password_input", report_dir, keys="Ahmad21@21@")
        except Exception as e:
            print(f"ERROR: Failed to enter password: {str(e)}")
            raise
        
        # Step 5: Wait for manual CAPTCHA
        print("\n--- Step 5: Waiting for manual CAPTCHA and login ---")
        print("Please complete the CAPTCHA and click the login button manually")
        input("Press Enter after you have completed the CAPTCHA and clicked login...")
        
        # Step 6: Verify login success
        try:
            print("\n--- Step 6: Verifying login success ---")
            wait.until(EC.url_contains("test-admin-ipipgo.cd.xiaoxigroup.net/app-manager"))
            print("Login successful")
            take_screenshot(driver, "06_login_success", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to verify login: {str(e)}")
            raise
            
    except Exception as e:
        print(f"\n=== Login failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

def add_article_category(report_dir):
    """Handles the process of adding a new article category"""
    try:
        print("\n=== Starting add_article_category test ===")
        driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/categorization")
        print(f"Current URL: {driver.current_url}")
        take_screenshot(driver, "07_category_initial_page", report_dir)
        
        category_name = generate_category_name()
        print(f"Generated category name: {category_name}")
        
        # Step 1: Click Add button
        try:
            print("\n--- Step 1: Clicking Add Button ---")
            add_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/form/button[2]/span")
            ))
            print("Found add button")
            interact_with_element(driver, add_button, "click", "08_category_add_button", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click add button: {str(e)}")
            raise
        
        # Step 2: Enter category name
        try:
            print("\n--- Step 2: Entering Category Name ---")
            name_input = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[2]/div/div[1]/input")
            ))
            print("Found name input")
            interact_with_element(driver, name_input, "send_keys", "09_category_name_input", report_dir, keys=category_name)
        except Exception as e:
            print(f"ERROR: Failed to enter category name: {str(e)}")
            raise
        
        # Step 3: Enter sorting number
        try:
            print("\n--- Step 3: Entering Sorting Number ---")
            sort_input = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[3]/div/div/input")
            ))
            print("Found sort input")
            interact_with_element(driver, sort_input, "send_keys", "10_category_sort_input", report_dir, keys="1")
        except Exception as e:
            print(f"ERROR: Failed to enter sorting number: {str(e)}")
            raise
        
        # Step 4: Click confirm
        try:
            print("\n--- Step 4: Clicking Confirm Button ---")
            confirm_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[3]/div/button[2]/span")
            ))
            print("Found confirm button")
            interact_with_element(driver, confirm_button, "click", "11_category_confirm_button", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click confirm button: {str(e)}")
            raise
        
        # Step 5: Verify success
        try:
            print("\n--- Step 5: Verifying Success ---")
            quick_wait = WebDriverWait(driver, 1)
            message_found = False
            
            try:
                print("Checking for success message...")
                success_message = quick_wait.until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[3]'))
                )
                message_found = True
                print("Success message found")
                take_screenshot(driver, "12_category_success_message", report_dir)
                
            except Exception as e:
                print(f"Could not catch success message: {str(e)}")
                try:
                    success_message = quick_wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'el-message__content'))
                    )
                    print("Success message found with alternative selector")
                    message_found = True
                    take_screenshot(driver, "12_category_success_message_alt", report_dir)
                except Exception as e:
                    print(f"Alternative selector also failed: {str(e)}")
                    raise
            
            if message_found:
                print("TEST PASSED: Category created successfully")
                time.sleep(1)
                take_screenshot(driver, "13_category_final_success", report_dir)
            else:
                raise Exception("TEST FAILED: Could not find success message")
            
        except Exception as e:
            print(f"ERROR: Failed to verify success: {str(e)}")
            raise
            
    except Exception as e:
        print(f"\n=== Category creation failed with error: {str(e)} ===")
        take_screenshot(driver, "category_final_error", report_dir)
        raise

def create_article(report_dir):
    """Handles the process of creating a new article"""
    try:
        print("\n=== Starting create_article test ===")
        driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/list")
        print(f"Current URL: {driver.current_url}")
        take_screenshot(driver, "14_article_initial_page", report_dir)
        
        # Generate random content
        article_title = generate_article_title()
        article_summary = generate_random_words(5)
        article_content = generate_random_words(10)
        print(f"Generated article title: {article_title}")
        
        # Step 1: Click Add Article button
        try:
            print("\n--- Step 1: Clicking Add Article Button ---")
            add_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/form/button[2]/span")
            ))
            print("Found add button")
            interact_with_element(driver, add_button, "click", "15_article_add_button", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click add button: {str(e)}")
            raise
        
        # Step 2: Select category
        try:
            print("\n--- Step 2: Selecting Category ---")
            category_dropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[2]/div/div/div/input")
            ))
            print("Found category dropdown")
            interact_with_element(driver, category_dropdown, "click", "16_article_category_dropdown", report_dir)
            time.sleep(1)
            
            category_option = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[4]/div[1]/div[1]/ul/li[6]")
            ))
            print("Found category option")
            interact_with_element(driver, category_option, "click", "17_article_category_selected", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to select category: {str(e)}")
            raise
        
        # Step 3: Enter title
        try:
            print("\n--- Step 3: Entering Title ---")
            title_input = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[3]/div/div[1]/input")
            ))
            print("Found title input")
            interact_with_element(driver, title_input, "send_keys", "18_article_title_input", report_dir, keys=article_title)
        except Exception as e:
            print(f"ERROR: Failed to enter title: {str(e)}")
            raise
        
        # Step 4: Enter summary
        try:
            print("\n--- Step 4: Entering Summary ---")
            summary_input = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[4]/div/div[1]/textarea")
            ))
            print("Found summary input")
            interact_with_element(driver, summary_input, "send_keys", "19_article_summary_input", report_dir, keys=article_summary)
        except Exception as e:
            print(f"ERROR: Failed to enter summary: {str(e)}")
            raise
        
        # Step 5: Enter content
        try:
            print("\n--- Step 5: Entering Content ---")
            content_input = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[5]/div/div/div[1]/div[2]/div[1]")
            ))
            print("Found content input")
            interact_with_element(driver, content_input, "click", "20_article_content_input", report_dir)
            time.sleep(1)
            
            try:
                iframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tox-edit-area__iframe")))
                driver.switch_to.frame(iframe)
                editable_body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                print("Found editable body in iframe")
                interact_with_element(driver, editable_body, "send_keys", "21_article_content_entered", report_dir, keys=article_content)
                driver.switch_to.default_content()
            except Exception as e:
                print(f"WARNING: Failed to enter content in iframe: {str(e)}")
                interact_with_element(driver, content_input, "send_keys", "21_article_content_entered_alt", report_dir, keys=article_content)
        except Exception as e:
            print(f"ERROR: Failed to enter content: {str(e)}")
            raise
        
        # Step 6: Submit form
        try:
            print("\n--- Step 6: Submitting Form ---")
            submit_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[3]/div/button[2]/span")
            ))
            print("Found submit button")
            interact_with_element(driver, submit_button, "click", "22_article_submit_button", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to submit form: {str(e)}")
            raise
        
        # Step 7: Verify success
        try:
            print("\n--- Step 7: Verifying Success ---")
            quick_wait = WebDriverWait(driver, 1)
            message_found = False
            
            try:
                print("Checking for success message...")
                success_message = quick_wait.until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[3]'))
                )
                message_found = True
                print("Success message found")
                take_screenshot(driver, "23_article_success_message", report_dir)
                
            except Exception as e:
                print(f"Could not catch success message: {str(e)}")
                try:
                    success_message = quick_wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'el-message__content'))
                    )
                    print("Success message found with alternative selector")
                    message_found = True
                    take_screenshot(driver, "23_article_success_message_alt", report_dir)
                except Exception as e:
                    print(f"Alternative selector also failed: {str(e)}")
                    raise
            
            if message_found:
                print("TEST PASSED: Article created successfully")
                time.sleep(1)
                take_screenshot(driver, "24_article_final_success", report_dir)
            else:
                raise Exception("TEST FAILED: Could not find success message")
            
        except Exception as e:
            print(f"ERROR: Failed to verify success: {str(e)}")
            raise
            
    except Exception as e:
        print(f"\n=== Article creation failed with error: {str(e)} ===")
        take_screenshot(driver, "article_final_error", report_dir)
        raise

def view_complaints(report_dir):
    """Handles the process of viewing complaints"""
    try:
        print("\n=== Starting view_complaints test ===")
        driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/complain")
        print(f"Current URL: {driver.current_url}")
        take_screenshot(driver, "25_complaints_initial_page", report_dir)
        
        # Step 1: Wait for complaints table
        try:
            print("\n--- Step 1: Waiting for Complaints Table ---")
            complaints_table = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'el-table')]")
            ))
            print("Found complaints table")
            interact_with_element(driver, complaints_table, "click", "26_complaints_table", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to find complaints table: {str(e)}")
            raise
        
        # Step 2: Verify table headers
        try:
            print("\n--- Step 2: Verifying Table Headers ---")
            headers = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/section/section/div/div/div/div[1]/div[2]/table/thead/tr/th")
            print("Found table headers")
            take_screenshot(driver, "27_complaints_headers_found", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to find table headers: {str(e)}")
            raise
            
    except Exception as e:
        print(f"\n=== Complaints view failed with error: {str(e)} ===")
        take_screenshot(driver, "complaints_final_error", report_dir)
        raise

# ===== Main Test Function =====
def main():
    """Main function to run the complete test flow"""
    try:
        # Create a single report directory for the entire test run
        report_dir = create_report_dir()
        print(f"\n=== Starting full flow test run with report directory: {report_dir} ===")
        
        # Run all operations in sequence
        login(report_dir)  # First login
        add_article_category(report_dir)  # Then create category
        create_article(report_dir)  # Then create article
        view_complaints(report_dir)  # Finally view complaints
        
        print("\n=== Full flow test completed successfully ===")
        take_screenshot(driver, "final_success", report_dir)
        
    except Exception as e:
        print(f"\n=== Full flow test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 