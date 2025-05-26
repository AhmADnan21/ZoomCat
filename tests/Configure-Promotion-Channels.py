"""
Selenium Test Automation for Promotion Channels Configuration
This script automates the process of:
1. Login
2. Add New Source
3. Add New Link
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
from cookies import cookies
import time
from datetime import datetime
import random

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
    test_dir = os.path.join(report_dir, f"Configure-Promotion-Channelstest_run_{timestamp}")
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

# ===== Name Generation Functions =====
def generate_source_name():
    """Generates a unique source name using current timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"MY-S-{timestamp}"

def generate_channel_name():
    """Generates a unique channel name using current timestamp"""
    timestamp = datetime.now().strftime("%d%H%M%S")
    return f"MY{timestamp}"

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

def add_new_source(report_dir):
    """Handles the process of adding a new source"""
    try:
        print("\n=== Starting add_new_source test ===")
        driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/promoting-short-link/customer-source")
        print(f"Current URL: {driver.current_url}")
        take_screenshot(driver, "07_initial_page", report_dir)
        
        source_name = generate_source_name()
        print(f"Generated source name: {source_name}")
        
        # Step 1: Click Add New Source button
        try:
            print("\n--- Step 1: Clicking Add New Source Button ---")
            add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='添加新来源']/..")))
            print("Found add button")
            interact_with_element(driver, add_button, "click", "08_add_button", report_dir)
            time.sleep(4)
        except Exception as e:
            print(f"ERROR: Failed to click add button: {str(e)}")
            raise
        
        # Step 2: Wait for popup
        try:
            print("\n--- Step 2: Waiting for Popup ---")
            popup = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]')))
            print("Found popup")
            time.sleep(2)
            take_screenshot(driver, "09_popup", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to find popup: {str(e)}")
            raise
        
        # Step 3: Enter source name
        try:
            print("\n--- Step 3: Entering Source Name ---")
            print("Entering source name directly")
            actions = webdriver.ActionChains(driver)
            actions.send_keys(source_name)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            time.sleep(2)
            take_screenshot(driver, "10_name_input", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to enter source name: {str(e)}")
            raise
        
        # Step 4: Wait for success message
        try:
            print("\n--- Step 4: Waiting for Success Message ---")
            quick_wait = WebDriverWait(driver, 1)
            message_found = False
            
            try:
                print("Checking for success message...")
                success_message = quick_wait.until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[5]'))
                )
                message_found = True
                print("Success message found")
                take_screenshot(driver, "11_success_message", report_dir)
                
            except Exception as e:
                print(f"Could not catch success message: {str(e)}")
                try:
                    success_message = quick_wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'el-message__content'))
                    )
                    print("Success message found with alternative selector")
                    message_found = True
                    take_screenshot(driver, "11_success_message_alt", report_dir)
                except Exception as e:
                    print(f"Alternative selector also failed: {str(e)}")
                    raise
            
            if message_found:
                print("TEST PASSED: Success message was found and verified")
                time.sleep(1)
                take_screenshot(driver, "final_success", report_dir)
            else:
                raise Exception("TEST FAILED: Could not find success message")
            
        except Exception as e:
            print(f"Failed to verify success message: {str(e)}")
            raise
            
    except Exception as e:
        print(f"\n=== Test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

def add_new_link(report_dir):
    """Handles the process of adding a new link"""
    try:
        print("\n=== Starting add_new_link test ===")
        driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/promoting-short-link/channel")
        print(f"Current URL: {driver.current_url}")
        take_screenshot(driver, "12_initial_page", report_dir)
        
        channel_name = generate_channel_name()
        print(f"Generated channel name: {channel_name}")
        
        # Step 1: Click Add New Link button
        try:
            print("\n--- Step 1: Clicking Add New Link Button ---")
            add_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/form/button[2]/span')))
            print("Found add button")
            interact_with_element(driver, add_button, "click", "13_add_button", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click add button: {str(e)}")
            raise
        
        # Step 2: Wait for popup
        try:
            print("\n--- Step 2: Waiting for Popup ---")
            popup = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[1]')))
            print("Found popup")
            take_screenshot(driver, "14_popup", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to find popup: {str(e)}")
            raise
        
        # Step 3: Enter channel name
        try:
            print("\n--- Step 3: Entering Channel Name ---")
            name_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[2]/form/div[1]/div/div[1]/input')
            print("Found name input")
            interact_with_element(driver, name_input, "send_keys", "15_name_input", report_dir, keys=channel_name)
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to enter channel name: {str(e)}")
            raise
        
        # Step 4: Select customer source
        try:
            print("\n--- Step 4: Selecting Customer Source ---")
            source_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[2]/form/div[3]/div/div/div[1]/input')
            print("Found source input")
            interact_with_element(driver, source_input, "click", "16_source_input", report_dir)
            time.sleep(1)
            
            print("Navigating to source using arrow keys...")
            for _ in range(20):
                fast_key_press(driver, source_input, Keys.ARROW_DOWN)
            
            fast_key_press(driver, source_input, Keys.ENTER)
            time.sleep(1)
            print("Selected source")
            take_screenshot(driver, "17_source_selected", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to select source: {str(e)}")
            raise
        
        # Step 5: Submit form and verify
        try:
            print("\n--- Step 5: Submit Form ---")
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[3]/div/button[2]/span')))
            print("Found submit button")
            submit_button.click()
            print("Clicked submit button")
            time.sleep(1)
            
            # Wait for success message
            try:
                quick_wait = WebDriverWait(driver, 1)
                message_found = False
                
                try:
                    print("Checking for success message...")
                    success_message = quick_wait.until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[5]'))
                    )
                    message_found = True
                    print("Success message found")
                    take_screenshot(driver, "18_success_message", report_dir)
                    
                except Exception as e:
                    print(f"Could not catch success message: {str(e)}")
                    try:
                        success_message = quick_wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'el-message__content'))
                        )
                        print("Success message found with alternative selector")
                        message_found = True
                        take_screenshot(driver, "18_success_message_alt", report_dir)
                    except Exception as e:
                        print(f"Alternative selector also failed: {str(e)}")
                        raise
                
                if message_found:
                    print("TEST PASSED: Success message was found and verified")
                    time.sleep(1)
                    take_screenshot(driver, "final_success", report_dir)
                else:
                    raise Exception("TEST FAILED: Could not find success message")
                
            except Exception as e:
                print(f"Failed to verify success message: {str(e)}")
                raise
            
        except Exception as e:
            print(f"ERROR: Failed to verify new link: {str(e)}")
            raise
            
    except Exception as e:
        print(f"\n=== Test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

# ===== Main Test Function =====
def main():
    """Main function to run the complete test flow"""
    try:
        # Create a single report directory for the entire test run
        report_dir = create_report_dir()
        print(f"\n=== Starting test run with report directory: {report_dir} ===")
        
        # Run all operations with the same report directory
        login(report_dir)  # First login
        add_new_source(report_dir)  # Then add new source
        add_new_link(report_dir)  # Finally add new link
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
    print(driver.current_url) 