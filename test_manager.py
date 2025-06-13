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
from tests.conftest import pytest_runtest_makereport
from typing import Any
import time
from datetime import datetime
import random
from login_manager import LoginManager

# ===== Global Configuration =====
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
login_manager = LoginManager(driver, wait)
##test1## 
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

##test2## 
# ===== Utility Functions =====
def create_report_dir():
    """Creates a timestamped directory for test reports"""
    report_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_dir = os.path.join(report_dir, f"Create-Supplier_test_run_{timestamp}")
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
def generate_test_name():
    """Generates a unique test name using current timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"MY-SG-{timestamp}"

def generate_supplier_name():
    """Generates a unique supplier name using current timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"MY-S-{timestamp}"

def generate_random_ip():
    """Generates a random IP address with port"""
    ip_parts = [str(random.randint(0, 255)) for _ in range(4)]
    port = random.randint(1111, 9999)
    return f"{'.'.join(ip_parts)}:{port}"

# ===== Test Step Functions =====

def add_supplier(report_dir):
    """Handles the supplier creation process"""
    try:
        print("\n=== Starting add_supplier test ===")
        driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operation/provider")
        print(f"Current URL: {driver.current_url}")
        take_screenshot(driver, "07_initial_page", report_dir)
        
        supplier_name = generate_supplier_name()
        print(f"Generated supplier name: {supplier_name}")
        
        # Step 1: Click create supplier button
        try:
            print("\n--- Step 1: Clicking Create Supplier Button ---")
            create_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/form/button/span')))
            print("Found create supplier button")
            interact_with_element(driver, create_button, "click", "08_create_button", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click create button: {str(e)}")
            raise
        
        # Step 2: Wait for popup and enter supplier name
        try:
            print("\n--- Step 2: Entering Supplier Name ---")
            popup = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[1]/span')))
            print("Found popup")
            name_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[2]/form/div[1]/div/div/input')
            print("Found name input")
            interact_with_element(driver, name_input, "send_keys", "09_name_input", report_dir, keys=supplier_name)
        except Exception as e:
            print(f"ERROR: Failed to enter supplier name: {str(e)}")
            raise
        
        # Step 3: Submit form and verify
        try:
            print("\n--- Step 3: Submit Form ---")
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[3]/div/button[2]/span')))
            print("Found submit button")
            submit_button.click()
            print("Clicked submit button")
            
            # Wait for success message
            try:
                quick_wait = WebDriverWait(driver, 2)
                message_found = False
                
                try:
                    print("Waiting for success message...")
                    success_message = quick_wait.until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/p'))
                    )
                    take_screenshot(driver, "10_success_message", report_dir)
                    print("Success message found and screenshot taken")
                    message_found = True
                    
                except Exception as e:
                    print(f"Could not catch success message: {str(e)}")
                    try:
                        success_message = quick_wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'el-message__content'))
                        )
                        take_screenshot(driver, "10_success_message_alt", report_dir)
                        print("Success message found with alternative selector")
                        message_found = True
                    except Exception as e:
                        print(f"Alternative selector also failed: {str(e)}")
                        raise
                
                if message_found:
                    print("TEST PASSED: Success message was found and verified")
                else:
                    raise Exception("TEST FAILED: Could not find success message")
                
            except Exception as e:
                print(f"Failed to verify success message: {str(e)}")
                take_screenshot(driver, "error_success_message", report_dir)
                raise
            
        except Exception as e:
            print(f"ERROR: Failed to verify new supplier: {str(e)}")
            take_screenshot(driver, "final_error", report_dir)
            raise
            
    except Exception as e:
        print(f"\n=== Test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

def add_server_group(report_dir):
    """Handles the server group creation process"""
    try:
        print("\n=== Starting add_server_group test ===")
        driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operation/server-group")
        print(f"Current URL: {driver.current_url}")
        take_screenshot(driver, "11_initial_page", report_dir)
        
        test_name = generate_test_name()
        print(f"Generated test name: {test_name}")
        
        # Step 1: Click add server group button
        try:
            print("\n--- Step 1: Clicking Add Server Group Button ---")
            add_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/form/button/span')))
            print("Found add server group button")
            interact_with_element(driver, add_button, "click", "12_add_button", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click add button: {str(e)}")
            raise
        
        # Step 2: Enter server group name
        try:
            print("\n--- Step 2: Entering Server Group Name ---")
            dialog = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[1]')))
            print("Found dialog")
            name_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[2]/form/div[2]/div/div/input')
            print("Found name input")
            interact_with_element(driver, name_input, "send_keys", "13_name_input", report_dir, keys=test_name)
        except Exception as e:
            print(f"ERROR: Failed to enter name: {str(e)}")
            raise
        
        # Step 3: Select country
        try:
            print("\n--- Step 3: Country Selection ---")
            country_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[2]/form/div[3]/div/div/div[1]/div[1]/input')
            print("Found country input")
            
            interact_with_element(driver, country_input, "click", "14_country_input_click", report_dir)
            interact_with_element(driver, country_input, "send_keys", "15_country_dropdown", report_dir, keys=Keys.SPACE, wait_time=2)
            interact_with_element(driver, country_input, "send_keys", "16_country_select", report_dir, keys=Keys.ARROW_DOWN)
            interact_with_element(driver, country_input, "send_keys", "17_country_confirm", report_dir, keys=Keys.ENTER)
            
        except Exception as e:
            print(f"ERROR: Failed in country selection: {str(e)}")
            raise
        
        # Step 4: Select city
        try:
            print("\n--- Step 4: City Selection ---")
            city_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[2]/form/div[3]/div/div/div[2]/div[1]/input')
            print("Found city input")
            
            interact_with_element(driver, city_input, "click", "18_city_input_click", report_dir)
            interact_with_element(driver, city_input, "send_keys", "19_city_dropdown", report_dir, keys=Keys.SPACE, wait_time=2)
            interact_with_element(driver, city_input, "send_keys", "20_city_select", report_dir, keys=Keys.ARROW_DOWN)
            interact_with_element(driver, city_input, "send_keys", "21_city_confirm", report_dir, keys=Keys.ENTER)
            
        except Exception as e:
            print(f"ERROR: Failed in city selection: {str(e)}")
            raise
        
        # Step 5: Submit form and verify
        try:
            print("\n--- Step 5: Submit Form ---")
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[3]/div/button[2]/span')))
            print("Found submit button")
            submit_button.click()
            print("Clicked submit button")
            
            # Wait for success message
            try:
                quick_wait = WebDriverWait(driver, 2)
                message_found = False
                
                try:
                    print("Waiting for success message...")
                    success_message = quick_wait.until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/p'))
                    )
                    take_screenshot(driver, "22_success_message", report_dir)
                    print("Success message found and screenshot taken")
                    message_found = True
                    
                except Exception as e:
                    print(f"Could not catch success message: {str(e)}")
                    try:
                        success_message = quick_wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'el-message__content'))
                        )
                        take_screenshot(driver, "22_success_message_alt", report_dir)
                        print("Success message found with alternative selector")
                        message_found = True
                    except Exception as e:
                        print(f"Alternative selector also failed: {str(e)}")
                        raise
                
                if message_found:
                    print("TEST PASSED: Success message was found and verified")
                else:
                    raise Exception("TEST FAILED: Could not find success message")
                
            except Exception as e:
                print(f"Failed to verify success message: {str(e)}")
                take_screenshot(driver, "error_success_message", report_dir)
                raise
            
        except Exception as e:
            print(f"ERROR: Failed to verify new item: {str(e)}")
            take_screenshot(driver, "final_error", report_dir)
            raise
            
    except Exception as e:
        print(f"\n=== Test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

def add_ip(report_dir):
    """Handles the IP creation process"""
    try:
        print("\n=== Starting add_ip test ===")
        driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operation/ip")
        print(f"Current URL: {driver.current_url}")
        take_screenshot(driver, "23_initial_page", report_dir)
        
        random_ip = generate_random_ip()
        print(f"Generated random IP: {random_ip}")
        
        # Step 1: Click add IP button
        try:
            print("\n--- Step 1: Clicking Add IP Button ---")
            add_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/form/button[2]/span')))
            print("Found add IP button")
            interact_with_element(driver, add_button, "click", "24_add_button", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click add button: {str(e)}")
            raise
        
        # Step 2: Wait for popup
        try:
            print("\n--- Step 2: Waiting for Popup ---")
            popup = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[1]/span')))
            print("Found popup")
            take_screenshot(driver, "25_popup", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to find popup: {str(e)}")
            raise
        
        # Step 3: Select supplier
        try:
            print("\n--- Step 3: Selecting Supplier ---")
            supplier_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[2]/form/div[1]/div/div/div/input')
            print("Found supplier input")
            interact_with_element(driver, supplier_input, "click", "26_supplier_input", report_dir)
            
            print("Navigating to supplier using arrow keys...")
            for _ in range(42):  # Press down arrow 42 times
                fast_key_press(driver, supplier_input, Keys.ARROW_DOWN)
            
            fast_key_press(driver, supplier_input, Keys.ENTER)
            print("Selected supplier")
        except Exception as e:
            print(f"ERROR: Failed to select supplier: {str(e)}")
            raise
        
        # Step 4: Select server group
        try:
            print("\n--- Step 4: Selecting Server Group ---")
            server_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[2]/form/div[2]/div/div/div/input')
            print("Found server input")
            interact_with_element(driver, server_input, "click", "27_server_input", report_dir)
            
            interact_with_element(driver, server_input, "send_keys", "28_server_search", report_dir, keys="Server Group-MY")
            time.sleep(1)  # Wait for search results
            
            print("Selecting first server group from search results...")
            interact_with_element(driver, server_input, "send_keys", "29_server_select", report_dir, keys=Keys.ARROW_DOWN)
            time.sleep(0.1)  # Small delay
            interact_with_element(driver, server_input, "send_keys", "30_server_confirm", report_dir, keys=Keys.ENTER)
            print("Selected server group")
        except Exception as e:
            print(f"ERROR: Failed to select server group: {str(e)}")
            raise
        
        # Step 5: Enter IP address
        try:
            print("\n--- Step 5: Entering IP Address ---")
            ip_textarea = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[2]/form/div[3]/div/div[1]/textarea')
            print("Found IP textarea")
            interact_with_element(driver, ip_textarea, "send_keys", "31_ip_entered", report_dir, keys=random_ip)
        except Exception as e:
            print(f"ERROR: Failed to enter IP: {str(e)}")
            raise
        
        # Step 6: Submit form and verify
        try:
            print("\n--- Step 6: Submit Form ---")
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/section/div/div[2]/div/div[3]/div/button[2]/span')))
            print("Found submit button")
            submit_button.click()
            print("Clicked submit button")
            
            # Wait for success message
            try:
                quick_wait = WebDriverWait(driver, 2)
                message_found = False
                
                try:
                    print("Waiting for success message...")
                    success_message = quick_wait.until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/p'))
                    )
                    take_screenshot(driver, "32_success_message", report_dir)
                    print("Success message found and screenshot taken")
                    message_found = True
                    
                except Exception as e:
                    print(f"Could not catch success message: {str(e)}")
                    try:
                        success_message = quick_wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'el-message__content'))
                        )
                        take_screenshot(driver, "32_success_message_alt", report_dir)
                        print("Success message found with alternative selector")
                        message_found = True
                    except Exception as e:
                        print(f"Alternative selector also failed: {str(e)}")
                        raise
                
                if message_found:
                    print("TEST PASSED: Success message was found and verified")
                else:
                    raise Exception("TEST FAILED: Could not find success message")
                
            except Exception as e:
                print(f"Failed to verify success message: {str(e)}")
                take_screenshot(driver, "error_success_message", report_dir)
                raise
            
        except Exception as e:
            print(f"ERROR: Failed to verify new IP: {str(e)}")
            take_screenshot(driver, "final_error", report_dir)
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
        login_manager.login(report_dir)  # First login
        add_new_source(report_dir)  # Then add new source
        add_new_link(report_dir)  # Finally add new link
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
