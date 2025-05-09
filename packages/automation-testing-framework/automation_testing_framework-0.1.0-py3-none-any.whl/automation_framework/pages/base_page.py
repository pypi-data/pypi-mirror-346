import logging
import os
from typing import Optional, Union, List
try:
    import allure
    has_allure = True
except ImportError:
    has_allure = False

from playwright.sync_api import Page

from automation_framework.config.config import Config
from automation_framework.utils.playwright_wrapper import PlaywrightWrapper

class BasePage:
    """Base page class that all page objects will inherit from."""
    
    def __init__(self, page: Page):
        self.page = page
        self.pw = PlaywrightWrapper(page)  # Initialize the Playwright wrapper
        self.base_url = Config.BASE_URL
        self.timeout = Config.DEFAULT_TIMEOUT
        self.logger = logging.getLogger(__name__)

    def step(self, description):
        """Decorator for adding a step to the report."""
        def decorator(func):
            if has_allure:
                return allure.step(description)(func)
            return func
        return decorator

    def navigate_to(self, url_path: str):
        """
        Navigate to a specific URL path.
        
        Args:
            url_path: The URL path to navigate to
        """
        if has_allure:
            with allure.step(f"Navigate to {url_path}"):
                full_url = f"{self.base_url}{url_path}"
                self.logger.info(f"Navigating to: {full_url}")
                self.pw.navigate_to(full_url)
        else:
            full_url = f"{self.base_url}{url_path}"
            self.logger.info(f"Navigating to: {full_url}")
            self.pw.navigate_to(full_url)
        
    def get_title(self) -> str:
        """
        Get the page title.
        
        Returns:
            The page title
        """
        return self.page.title()
    
    def wait_for_element(self, selector: str, state: str = "visible"):
        """
        Wait for an element to be in a specific state.
        
        Args:
            selector: The element selector
            state: The element state to wait for (visible, hidden, attached, detached)
        """
        if has_allure:
            with allure.step(f"Wait for element {selector} to be {state}"):
                self.pw.wait_for_selector(selector, state=state)
        else:
            self.pw.wait_for_selector(selector, state=state)
        
    def click(self, selector: str):
        """
        Click on an element.
        
        Args:
            selector: The element selector
        """
        if has_allure:
            with allure.step(f"Click on {selector}"):
                self.pw.click(selector)
        else:
            self.pw.click(selector)
        
    def fill(self, selector: str, text: str):
        """
        Fill text into an input field.
        
        Args:
            selector: The element selector
            text: The text to fill
        """
        if has_allure:
            with allure.step(f"Fill {selector} with '{text}'"):
                self.pw.fill(selector, text)
        else:
            self.pw.fill(selector, text)
        
    def get_text(self, selector: str) -> str:
        """
        Get text from an element.
        
        Args:
            selector: The element selector
            
        Returns:
            The element text
        """
        return self.pw.get_text(selector)
    
    def is_element_visible(self, selector: str) -> bool:
        """
        Check if an element is visible.
        
        Args:
            selector: The element selector
            
        Returns:
            True if the element is visible, False otherwise
        """
        return self.pw.is_visible(selector)
    
    def take_screenshot(self, name: str) -> str:
        """
        Take a screenshot.
        
        Args:
            name: The screenshot name
            
        Returns:
            The screenshot path
        """
        # Ensure the screenshots directory exists
        os.makedirs(Config.SCREENSHOTS_PATH, exist_ok=True)
        
        # Generate a filename
        screenshot_path = f"{Config.SCREENSHOTS_PATH}/{name}.png"
        self.logger.info(f"Taking screenshot: {screenshot_path}")
        
        if has_allure:
            with allure.step(f"Take screenshot: {name}"):
                # Take the screenshot using Playwright's API
                screenshot_bytes = self.page.screenshot(full_page=True)
                
                # Save the screenshot to file
                with open(screenshot_path, 'wb') as f:
                    f.write(screenshot_bytes)
                
                # Attach the screenshot bytes directly to the Allure report
                allure.attach(
                    screenshot_bytes,
                    name=name,
                    attachment_type=allure.attachment_type.PNG
                )
        else:
            # Take the screenshot using Playwright's API
            screenshot_bytes = self.page.screenshot(full_page=True)
            
            # Save the screenshot to file
            with open(screenshot_path, 'wb') as f:
                f.write(screenshot_bytes)
        
        self.logger.info(f"Screenshot saved to: {screenshot_path}")
        return screenshot_path
    
    def element_contains_text(self, selector: str, text: str) -> bool:
        """
        Check if an element contains specific text.
        
        Args:
            selector: The element selector
            text: The text to check for
            
        Returns:
            True if the element contains the text, False otherwise
        """
        return self.pw.element_contains_text(selector, text)
    
    def select_option(self, selector: str, value: Optional[str] = None, index: Optional[int] = None, label: Optional[str] = None) -> List[str]:
        """
        Select an option from a dropdown.
        
        Args:
            selector: The element selector
            value: The option value
            index: The option index
            label: The option label
            
        Returns:
            List of selected values
        """
        if has_allure:
            with allure.step(f"Select option in {selector}"):
                return self.pw.select_option(selector, value, index, label)
        else:
            return self.pw.select_option(selector, value, index, label)
    
    def hover(self, selector: str):
        """
        Hover over an element.
        
        Args:
            selector: The element selector
        """
        if has_allure:
            with allure.step(f"Hover over {selector}"):
                self.pw.hover(selector)
        else:
            self.pw.hover(selector)
    
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """
        Get an attribute value from an element.
        
        Args:
            selector: The element selector
            attribute: The attribute name
            
        Returns:
            The attribute value or None if the attribute doesn't exist
        """
        return self.pw.get_attribute(selector, attribute)
    
    def check(self, selector: str):
        """
        Check a checkbox or radio button.
        
        Args:
            selector: The element selector
        """
        if has_allure:
            with allure.step(f"Check {selector}"):
                self.pw.check(selector)
        else:
            self.pw.check(selector)
    
    def uncheck(self, selector: str):
        """
        Uncheck a checkbox.
        
        Args:
            selector: The element selector
        """
        if has_allure:
            with allure.step(f"Uncheck {selector}"):
                self.pw.uncheck(selector)
        else:
            self.pw.uncheck(selector)
    
    def wait_for_url(self, url: str, timeout: Optional[int] = None):
        """
        Wait for URL to be a specific value.
        
        Args:
            url: The URL to wait for
            timeout: The timeout in milliseconds
        """
        if has_allure:
            with allure.step(f"Wait for URL: {url}"):
                self.pw.wait_for_url(url, timeout)
        else:
            self.pw.wait_for_url(url, timeout)

    def press_key(self, key: str):
        """
        Press a key on an element.
        
        Args:
            key: The key to press
        """
        if has_allure:
            with allure.step(f"Press key: {key}"):
                self.pw.press_global_key(key)
        else:
            self.pw.press_global_key(key)
