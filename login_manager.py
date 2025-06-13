"""
Login Manager Module
This module handles the login functionality for the test automation suite.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

class LoginManager:
    def __init__(self, driver: webdriver.Chrome, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def take_screenshot(self, step_name, report_dir):
        """Takes and saves a screenshot with the given step name"""
        screenshot_path = os.path.join(report_dir, f"{step_name}.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")

    def interact_with_element(self, element, action, step_name, report_dir, wait_time=1, **kwargs):
        """Handles element interaction with screenshots and highlighting"""
        try:
            self.driver.execute_script("arguments[0].style.border='3px solid red'", element)
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
            self.take_screenshot(step_name, report_dir)
            
        except Exception as e:
            raise Exception(f"Failed to {action} element: {str(e)}")

    def login(self, report_dir, username="abdullahahmad", password="Ahmad21@21@"):
        """Handles the login process"""
        try:
            print("\n=== Starting login process ===")
            self.driver.get("https://sso.xiaoxitech.com/login?project=lwlu63w1&cb=https%3A%2F%2Ftest-admin-ipipgo.cd.xiaoxigroup.net%2Fapp-manager%2F")
            print("Navigated to login page")
            self.take_screenshot("01_login_page", report_dir)
            
            # Step 1: Click initial button
            try:
                print("\n--- Step 1: Clicking initial button ---")
                initial_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/form/div[2]/div/div/button/span')))
                print("Found initial button")
                self.interact_with_element(initial_button, "click", "02_initial_button", report_dir)
            except Exception as e:
                print(f"ERROR: Failed to click initial button: {str(e)}")
                raise
            
            # Step 2: Wait for login form
            try:
                print("\n--- Step 2: Waiting for login form ---")
                login_form = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/form/div[4]/div/button/span')))
                print("Login form appeared")
                self.take_screenshot("03_login_form", report_dir)
            except Exception as e:
                print(f"ERROR: Failed to find login form: {str(e)}")
                raise
            
            # Step 3: Enter username
            try:
                print("\n--- Step 3: Entering username ---")
                username_input = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div/form/div[1]/div/div[1]/input')
                print("Found username input")
                self.interact_with_element(username_input, "send_keys", "04_username_input", report_dir, keys=username)
            except Exception as e:
                print(f"ERROR: Failed to enter username: {str(e)}")
                raise
            
            # Step 4: Enter password
            try:
                print("\n--- Step 4: Entering password ---")
                password_input = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div/form/div[2]/div/div/input')
                print("Found password input")
                self.interact_with_element(password_input, "send_keys", "05_password_input", report_dir, keys=password)
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
                self.wait.until(EC.url_contains("test-admin-ipipgo.cd.xiaoxigroup.net/app-manager"))
                print("Login successful")
                self.take_screenshot("06_login_success", report_dir)
            except Exception as e:
                print(f"ERROR: Failed to verify login: {str(e)}")
                raise
                
        except Exception as e:
            print(f"\n=== Login failed with error: {str(e)} ===")
            self.take_screenshot("final_error", report_dir)
            raise