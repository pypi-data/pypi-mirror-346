"""browser_automation Module to automate configuration via a browser interface.

These are typically used as fallback options if no REST API or LLConfig can be used.

This module uses playwright: https://playwright.dev for broweser-based automation
and testing.

Here are few few examples of the most typical page matches with the different selector types:

| **Element to Match**     | **CSS**                        | **XPath**                                         | **Playwright `get_by_*` Method**          |
| ------------------------ | ------------------------------ | ------------------------------------------------- | ----------------------------------------- |
| Element with ID          | `#myId`                        | `//*[@id='myId']`                                 | *Not available directly; use `locator()`* |
| Element with class       | `.myClass`                     | `//*[@class='myClass']`                           | *Not available directly; use `locator()`* |
| Button with exact text   | `button:has-text("Submit")`    | `//button[text()='Submit']`                       | `get_by_role("button", name="Submit")`    |
| Button with partial text | `button:has-text("Sub")`       | `//button[contains(text(), 'Sub')]`               | `get_by_text("Sub")`                      |
| Input with name          | `input[name="email"]`          | `//input[@name='email']`                          | *Not available directly; use `locator()`* |
| Link by text             | `a:has-text("Home")`           | `//a[text()='Home']`                              | `get_by_role("link", name="Home")`        |
| Element with title       | `[title="Info"]`               | `//*[@title='Info']`                              | `get_by_title("Info")`                    |
| Placeholder text         | `input[placeholder="Search"]`  | `//input[@placeholder='Search']`                  | `get_by_placeholder("Search")`            |
| Label text (form input)  | `label:has-text("Email")`      | `//label[text()='Email']`                         | `get_by_label("Email")`                   |
| Alt text (image)         | `img[alt="Logo"]`              | `//img[@alt='Logo']`                              | `get_by_alt_text("Logo")`                 |
| Role and name (ARIA)     | `[role="button"][name="Save"]` | `//*[@role='button' and @name='Save']`            | `get_by_role("button", name="Save")`      |
| Visible text anywhere    | `:text("Welcome")`             | `//*[contains(text(), "Welcome")]`                | `get_by_text("Welcome")`                  |
| nth element in a list    | `ul > li:nth-child(2)`         | `(//ul/li)[2]`                                    | `locator("ul > li").nth(1)`               |
| Element with attribute   | `[data-test-id="main"]`        | `//*[@data-test-id='main']`                       | *Not available directly; use `locator()`* |
| Nested element           | `.container .button`           | `//div[@class='container']//div[@class='button']` | `locator(".container .button")`           |

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2025, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import logging
import os
import tempfile
import time
from http import HTTPStatus

default_logger = logging.getLogger("pyxecm.customizer.browser_automation")

# For backwards compatibility we also want to handle
# cases where the playwright modules have not been installed
# in the customizer container:
try:
    from playwright.sync_api import (
        Browser,
        BrowserContext,
        ElementHandle,
        Page,
        sync_playwright,
    )
    from playwright.sync_api import Error as PlaywrightError
except ModuleNotFoundError:
    default_logger.warning("Module playwright is not installed")

# We use "networkidle" as default "wait until" strategy as
# this seems to best harmonize with OTCS. Especially login
# procedure for OTDS / OTCS seems to not work with the "load"
# "wait until" strategy.
DEFAULT_WAIT_UNTIL_STRATEGY = "networkidle"

REQUEST_TIMEOUT = 30
REQUEST_RETRY_DELAY = 2
REQUEST_MAX_RETRIES = 3

class BrowserAutomation:
    """Class to automate settings via a browser interface."""

    logger: logging.Logger = default_logger

    def __init__(
        self,
        base_url: str = "",
        user_name: str = "",
        user_password: str = "",
        download_directory: str | None = None,
        take_screenshots: bool = False,
        automation_name: str = "",
        headless: bool = True,
        logger: logging.Logger = default_logger,
        wait_until: str | None = None,
    ) -> None:
        """Initialize the object.

        Args:
            base_url (str, optional):
                The base URL of the website to automate. Defaults to "".
            user_name (str, optional):
                If an authentication at the web site is required, this is the user name.
                Defaults to "".
            user_password (str, optional):
                If an authentication at the web site is required, this is the user password.
                Defaults to "".
            download_directory (str | None, optional):
                A download directory used for download links. If None,
                a temporary directory is automatically used.
            take_screenshots (bool, optional):
                For debugging purposes, screenshots can be taken.
                Defaults to False.
            automation_name (str, optional):
                The name of the automation. Defaults to "".
            headless (bool, optional):
                If True, the browser will be started in headless mode. Defaults to True.
            wait_until (str | None, optional):
                Wait until a certain condition. Options are:
                * "load" - Waits for the load event (after all resources like images/scripts load)
                * "networkidle" - Waits until there are no network connections for at least 500 ms.
                * "domcontentloaded" - Waits for the DOMContentLoaded event (HTML is parsed,
                  but subresources may still load).
            logger (logging.Logger, optional):
                The logging object to use for all log messages. Defaults to default_logger.

        """

        if not download_directory:
            download_directory = os.path.join(
                tempfile.gettempdir(),
                "browser_automations",
                automation_name,
                "downloads",
            )

        if logger != default_logger:
            self.logger = logger.getChild("browserautomation")
            for logfilter in logger.filters:
                self.logger.addFilter(logfilter)

        self.base_url = base_url
        self.user_name = user_name
        self.user_password = user_password
        self.logged_in = False
        self.download_directory = download_directory

        self.take_screenshots = take_screenshots
        self.screenshot_names = automation_name
        self.screenshot_counter = 1
        self.wait_until = wait_until if wait_until else DEFAULT_WAIT_UNTIL_STRATEGY

        self.screenshot_directory = os.path.join(
            tempfile.gettempdir(),
            "browser_automations",
            automation_name,
            "screenshots",
        )
        if self.take_screenshots and not os.path.exists(self.screenshot_directory):
            os.makedirs(self.screenshot_directory)

        self.playwright = sync_playwright().start()
        self.browser: Browser = self.playwright.chromium.launch(headless=headless)
        self.context: BrowserContext = self.browser.new_context(
            accept_downloads=True,
        )
        self.page: Page = self.context.new_page()

    # end method definition

    def take_screenshot(self) -> bool:
        """Take a screenshot of the current browser window and save it as PNG file.

        Returns:
            bool:
                True if successful, False otherwise

        """

        screenshot_file = "{}/{}-{}.png".format(
            self.screenshot_directory,
            self.screenshot_names,
            self.screenshot_counter,
        )
        self.logger.debug("Save browser screenshot to -> %s", screenshot_file)

        try:
            self.page.screenshot(path=screenshot_file)
            self.screenshot_counter += 1
        except Exception as e:
            self.logger.error("Failed to take screenshot; error -> %s", e)
            return False

        return True

    # end method definition

    def get_page(self, url: str = "", wait_until: str | None = None) -> bool:
        """Load a page into the browser based on a given URL.

        Args:
            url (str):
                URL to load. If empty just the base URL will be used.
            wait_until (str | None, optional):
                Wait until a certain condition. Options are:
                * "load" - Waits for the load event (after all resources like images/scripts load)
                  This is the safest strategy for pages that keep loading content in the background
                  like Salesforce.
                * "networkidle" - Waits until there are no network connections for at least 500 ms.
                  This seems to be the safest one for OpenText Content Server.
                * "domcontentloaded" - Waits for the DOMContentLoaded event (HTML is parsed,
                  but subresources may still load).

        Returns:
            bool:
                True if successful, False otherwise.

        """

        # If no specific wait until strategy is provided in the
        # parameter, we take the one from the browser automation class:
        if wait_until is None:
            wait_until = self.wait_until

        page_url = self.base_url + url

        try:
            self.logger.debug("Load page -> %s", page_url)

            # The Playwright Response object is different from the requests.response object!
            response = self.page.goto(page_url, wait_until=wait_until)
            if response is None:
                self.logger.warning("Loading of page -> %s completed but no response object was returned.", page_url)
            elif not response.ok:
                # Try to get standard phrase, fall back if unknown
                try:
                    phrase = HTTPStatus(response.status).phrase
                except ValueError:
                    phrase = "Unknown Status"
                self.logger.error(
                    "Response for page -> %s is not OK. Status -> %s/%s",
                    page_url,
                    response.status,
                    phrase,
                )
                return False

        except PlaywrightError as e:
            self.logger.error("Navigation to page -> %s has failed; error -> %s", page_url, str(e))
            return False

        if self.take_screenshots:
            self.take_screenshot()

        return True

    # end method definition

    def get_title(
        self,
        wait_until: str | None = None,
    ) -> str | None:
        """Get the browser title.

        This is handy to validate a certain page is loaded after get_page()

        Retry-safe way to get the page title, even if there's an in-flight navigation.

        Args:
            wait_until (str | None, optional):
                Wait until a certain condition. Options are:
                * "load" - Waits for the load event (after all resources like images/scripts load)
                  This is the safest strategy for pages that keep loading content in the background
                  like Salesforce.
                * "networkidle" - Waits until there are no network connections for at least 500 ms.
                  This seems to be the safest one for OpenText Content Server.
                * "domcontentloaded" - Waits for the DOMContentLoaded event (HTML is parsed,
                  but subresources may still load).

        Returns:
            str:
                The title of the browser window.

        """

        for _ in range(REQUEST_MAX_RETRIES):
            try:
                return self.page.title()
            except Exception as e:
                if "Execution context was destroyed" in str(e):
                    time.sleep(REQUEST_RETRY_DELAY)
                    self.page.wait_for_load_state(state=wait_until, timeout=REQUEST_TIMEOUT)
                else:
                    self.logger.error("Could not get page title; error -> %s", e)

        return None
    # end method definition

    def scroll_to_element(self, element: ElementHandle) -> None:
        """Scroll an element into view to make it clickable.

        Args:
            element (ElementHandle):
                Web element that has been identified before.

        """

        if not element:
            self.logger.error("Undefined element!")
            return

        try:
            element.scroll_into_view_if_needed()
        except PlaywrightError as e:
            self.logger.error("Error while scrolling element into view -> %s", str(e))

    # end method definition

    def find_elem(
        self,
        selector: str,
        selector_type: str = "id",
        role_type: str | None = None,
        show_error: bool = True,
    ) -> ElementHandle | None:
        """Find a page element.

        Args:
            selector (str):
                The name of the page element or accessible name (for role).
            selector_type (str, optional):
                One of "id", "name", "class_name", "xpath", "css", "role", "text", "title",
                "label", "placeholder", "alt".
            role_type (str | None, optional):
                ARIA role when using selector_type="role", e.g., "button", "textbox".
                If irrelevant then None should be passed for role_type.
            show_error (bool, optional):
                Show an error if not found or not visible.

        Returns:
            ElementHandle:
                The web element or None in case an error occured.

        """

        locator = None
        failure_message = "Cannot find page element with selector -> '{}' ({}){}".format(
            selector, selector_type, " and role type -> '{}'".format(role_type) if role_type else ""
        )
        success_message = "Found page element with selector -> '{}' ('{}'){}".format(
            selector, selector_type, " and role type -> '{}'".format(role_type) if role_type else ""
        )

        try:
            match selector_type:
                case "id":
                    locator = self.page.locator("#{}".format(selector))
                case "name":
                    locator = self.page.locator("[name='{}']".format(selector))
                case "class_name":
                    locator = self.page.locator(".{}".format(selector))
                case "xpath":
                    locator = self.page.locator("xpath={}".format(selector))
                case "css":
                    locator = self.page.locator(selector)
                case "text":
                    locator = self.page.get_by_text(selector)
                case "title":
                    locator = self.page.get_by_title(selector)
                case "label":
                    locator = self.page.get_by_label(selector)
                case "placeholder":
                    locator = self.page.get_by_placeholder(selector)
                case "alt":
                    locator = self.page.get_by_alt_text(selector)
                case "role":
                    if not role_type:
                        self.logger.error("Role type must be specified when using find method 'role'!")
                        return None
                    locator = self.page.get_by_role(role=role_type, name=selector)
                case _:
                    self.logger.error("Unsupported selector type -> '%s'", selector_type)
                    return None

            elem = locator.element_handle() if locator is not None else None
            if elem is None:
                if show_error:
                    self.logger.error(failure_message)
                else:
                    self.logger.warning(failure_message)
            else:
                self.logger.debug(success_message)

        except PlaywrightError as e:
            if show_error:
                self.logger.error("%s; error -> %s", failure_message, str(e))
            else:
                self.logger.warning("%s; error -> %s", failure_message, str(e))
            return None

        return elem

    # end method definition

    def find_elem_and_click(
        self,
        selector: str,
        selector_type: str = "id",
        role_type: str | None = None,
        scroll_to_element: bool = True,
        desired_checkbox_state: bool | None = None,
        is_navigation_trigger: bool = False,
        wait_until: str | None = None,
        show_error: bool = True,
    ) -> bool:
        """Find a page element and click it.

        Args:
            selector (str):
                The selector of the page element.
            selector_type (str, optional):
                One of "id", "name", "class_name", "xpath", "css", "role", "text", "title",
                "label", "placeholder", "alt".
            role_type (str | None, optional):
                ARIA role when using selector_type="role", e.g., "button", "textbox".
                If irrelevant then None should be passed for role_type.
            scroll_to_element (bool, optional):
                Scroll the element into view.
            desired_checkbox_state (bool | None, optional):
                If True/False, ensures checkbox matches state.
                If None then click it in any case.
            is_navigation_trigger (bool, optional):
                Is the click causing a navigation. Default is False.
            wait_until (str | None, optional):
                Wait until a certain condition. Options are:
                * "load" - Waits for the load event (after all resources like images/scripts load)
                  This is the safest strategy for pages that keep loading content in the background
                  like Salesforce.
                * "networkidle" - Waits until there are no network connections for at least 500 ms.
                  This seems to be the safest one for OpenText Content Server.
                * "domcontentloaded" - Waits for the DOMContentLoaded event (HTML is parsed,
                  but subresources may still load).
            show_error (bool, optional):
                Show an error if the element is not found or not clickable.

        Returns:
            bool:
                True if click is successful (or checkbox already in desired state),
                False otherwise.

        """

        # If no specific wait until strategy is provided in the
        # parameter, we take the one from the browser automation class:
        if wait_until is None:
            wait_until = self.wait_until

        if not selector:
            failure_message = "Missing element selector! Cannot find page element!"
            if show_error:
                self.logger.error(failure_message)
            else:
                self.logger.warning(failure_message)
            return False

        elem = self.find_elem(
            selector=selector, selector_type=selector_type, role_type=role_type, show_error=show_error
        )
        if not elem:
            return not show_error

        try:
            if scroll_to_element:
                self.scroll_to_element(elem)

            # Handle checkboxes
            is_checkbox = elem.get_attribute("type") == "checkbox"
            checkbox_state = None

            if is_checkbox and desired_checkbox_state is not None:
                checkbox_state = elem.is_checked()
                if checkbox_state == desired_checkbox_state:
                    self.logger.debug(
                        "Checkbox -> '%s' is already in desired state -> %s", selector, desired_checkbox_state
                    )
                    return True  # No need to click
                else:
                    self.logger.debug("Checkbox -> '%s' has state mismatch. Clicking to change state.", selector)

            if is_navigation_trigger:
                self.logger.info("Clicking on navigation-triggering element -> '%s'", selector)
                try:
                    with self.page.expect_navigation(wait_until=wait_until):
                        elem.click()
                except PlaywrightError as e:
                    self.logger.error(
                        "Navigation after clicking on element -> '%s' did not happen or failed; likely wrong parameter passed; error -> %s",
                        selector,
                        str(e),
                    )
                    return False
            else:
                self.logger.info("Clicking on non-navigating element -> '%s'", selector)
                try:
                    elem.click()
                    time.sleep(1)
                except PlaywrightError as e:
                    self.logger.error("Click failed -> %s", str(e))
                    return False

            if is_checkbox and desired_checkbox_state is not None:
                elem = self.find_elem(selector=selector, selector_type=selector_type, show_error=show_error)
                if elem:
                    checkbox_state = elem.is_checked()

            if checkbox_state is not None:
                if checkbox_state == desired_checkbox_state:
                    self.logger.debug(
                        "Successfully clicked checkbox element -> '%s'. It's state is now -> %s",
                        selector,
                        checkbox_state,
                    )
                else:
                    self.logger.error(
                        "Failed to flip checkbox element -> '%s' to desired state. It's state is still -> %s and not -> %s",
                        selector,
                        checkbox_state,
                        desired_checkbox_state,
                    )
            else:
                self.logger.debug("Successfully clicked element -> '%s'", selector)

            if self.take_screenshots:
                self.take_screenshot()

        except PlaywrightError as e:
            if show_error:
                self.logger.error("Cannot click page element -> '%s'; error -> %s", selector, str(e))
            else:
                self.logger.warning("Cannot click page element -> '%s'; warning -> %s", selector, str(e))
            return not show_error

        return True

    # end method definition

    def find_elem_and_set(
        self,
        selector: str,
        value: str | bool,
        selector_type: str = "id",
        role_type: str | None = None,
        is_sensitive: bool = False,
        show_error: bool = True,
    ) -> bool:
        """Find an page element and fill it with a new text.

        Args:
            selector (str):
                The name of the page element.
            value (str | bool):
                The new value (text string) for the page element.
            selector_type (str, optional):
                One of "id", "name", "class_name", "xpath", "css", "role", "text", "title",
                "label", "placeholder", "alt".
            role_type (str | None, optional):
                ARIA role when using selector_type="role", e.g., "button", "textbox".
                If irrelevant then None should be passed for role_type.
            is_sensitive (bool, optional):
                True for suppressing sensitive information in logging.
            show_error (bool, optional):
                Show an error if the element is not found or not clickable.

        Returns:
            bool:
                True if successful, False otherwise

        """

        elem = self.find_elem(selector=selector, selector_type=selector_type, role_type=role_type, show_error=True)
        if not elem:
            return False

        is_enabled = elem.is_enabled()
        if not is_enabled:
            message = "Cannot set elem -> '{}' ({}) to value -> '{}'. It is not enabled!".format(
                selector, selector_type, value
            )
            if show_error:
                self.logger.error(message)
            else:
                self.logger.warning(message)

            return False

        if not is_sensitive:
            self.logger.debug("Set element -> %s to value -> '%s'...", selector, value)
        else:
            self.logger.debug("Set element -> %s to value -> <sensitive>...", selector)

        try:
            # HTML '<select>' can only be identified based on its tag name:
            tag_name = elem.evaluate("el => el.tagName.toLowerCase()")
            # Checkboxes have tag name '<input type="checkbox">':
            input_type = elem.get_attribute("type")

            if tag_name == "select":
                options = elem.query_selector_all("option")
                option_values = [opt.inner_text().strip().replace("\n", "") for opt in options]
                if value not in option_values:
                    self.logger.warning(
                        "Provided value -> '%s' not in available drop-down options -> %s. Cannot set it!",
                        value,
                        option_values,
                    )
                    return False
                # We set the value over the (visible) label:
                elem.select_option(label=value)
            elif tag_name == "input" and input_type == "checkbox":
                # Handle checkbox
                if not isinstance(value, bool):
                    self.logger.error("Checkbox value must be a boolean!")
                    return False
                is_checked = elem.is_checked()
                if value != is_checked:
                    elem.check() if value else elem.uncheck()
            else:
                elem.fill(value)
        except PlaywrightError as e:
            message = "Cannot set page element selected by -> '{}' ({}) to value -> '{}'; error -> {}".format(
                selector, selector_type, value, str(e)
            )
            if show_error:
                self.logger.error(message)
            else:
                self.logger.warning(message)
            return False

        if self.take_screenshots:
            self.take_screenshot()

        return True

    # end method definition

    def find_element_and_download(
        self,
        selector: str,
        selector_type: str = "id",
        role_type: str | None = None,
        download_time: int = 30,
    ) -> str | None:
        """Click a page element to initiate a download.

        Args:
            selector (str):
                The page element to click for download.
            selector_type (str, optional):
                One of "id", "name", "class_name", "xpath", "css", "role", "text", "title",
                "label", "placeholder", "alt".
            role_type (str | None, optional):
                ARIA role when using selector_type="role", e.g., "button", "textbox".
                If irrelevant then None should be passed for role_type.
            download_time (int, optional):
                Time in seconds to wait for the download to complete.

        Returns:
            str | None:
                The full file path of the downloaded file.

        """

        try:
            with self.page.expect_download(timeout=download_time * 1000) as download_info:
                clicked = self.find_elem_and_click(selector=selector, selector_type=selector_type, role_type=role_type)
                if not clicked:
                    self.logger.error("Element not found to initiate download.")
                    return None

            download = download_info.value
            filename = download.suggested_filename
            save_path = os.path.join(self.download_directory, filename)
            download.save_as(save_path)
        except Exception as e:
            self.logger.error("Download failed; error -> %s", str(e))
            return None

        self.logger.info("Download file to -> %s", save_path)

        return save_path

    # end method definition

    def check_elems_exist(
        self,
        selector: str,
        selector_type: str = "id",
        role_type: str | None = None,
        value: str | None = None,
        attribute: str | None = None,
        substring: bool = True,
        min_count: int = 1,
        wait_time: float = 0.0,
        show_error: bool = True,
    ) -> tuple[bool | None, int]:
        """Check if (multiple) elements with defined attributes exist on page and return the number.

        Args:
            selector (str):
                Base selector.
            selector_type (str):
                One of "id", "name", "class_name", "xpath", "css", "role", "text", "title",
                "label", "placeholder", "alt".
                When using css, the selector becomes a raw CSS selector, and you can skip attribute
                and value filtering entirely if your selector already narrows it down.
                Examples for CSS:
                * selector="img" - find all img tags (images)
                * selector="img[title]" - find all img tags (images) that have a title attribute - independent of its value
                * selector="img[title*='Microsoft Teams']" - find all images with a title that contains "Microsoft Teams"
                * selector=".toolbar button" - find all buttons inside a .toolbar class
            role_type (str | None, optional):
                ARIA role when using selector_type="role", e.g., "button", "textbox".
                If irrelevant then None should be passed for role_type.
            value (str, optional):
                Value to match in attribute or element content.
            attribute (str, optional):
                Attribute name to inspect. If None, uses element's text.
            substring (bool):
                If True, allow partial match.
            min_count (int):
                Minimum number of required matches (# elements on page).
            wait_time (float):
                Time in seconds to wait for elements to appear.
            show_error (bool):
                Whether to log warnings/errors.

        Returns:
            bool | None:
                True if sufficient elements exist. False otherwise.
                None if an error occurs.
            int:
                Number of matched elements.

        """

        # Some operations that are done server-side and dynamically update
        # the page may require a waiting time:
        if wait_time > 0.0:
            self.logger.info("Wait for %d milliseconds before checking...", wait_time * 1000)
            self.page.wait_for_timeout(wait_time * 1000)

        try:
            match selector_type:
                case "id":
                    locator = self.page.locator("#{}".format(selector))
                case "name":
                    locator = self.page.locator("[name='{}']".format(selector))
                case "class_name":
                    locator = self.page.locator(".{}".format(selector))
                case "xpath":
                    locator = self.page.locator("xpath={}".format(selector))
                case "css":
                    locator = self.page.locator(selector)
                case "text":
                    locator = self.page.get_by_text(selector)
                case "title":
                    locator = self.page.get_by_title(selector)
                case "label":
                    locator = self.page.get_by_label(selector)
                case "placeholder":
                    locator = self.page.get_by_placeholder(selector)
                case "alt":
                    locator = self.page.get_by_alt_text(selector)
                case "role":
                    if not role_type:
                        self.logger.error("Role type must be specified when using find method 'role'!")
                        return (None, 0)
                    locator = self.page.get_by_role(role=role_type, name=selector)
                case _:
                    self.logger.error("Unsupported selector type -> '%s'", selector_type)
                    return (None, 0)

            matching_elems = []

            count = locator.count() if locator is not None else 0
            if count == 0:
                if show_error:
                    self.logger.error("No elements found using selector -> '%s' ('%s')", selector, selector_type)
                return (None, 0)

            for i in range(count):
                elem_handle = locator.nth(i).element_handle()
                if not elem_handle:
                    continue

                if value is None:
                    # No filtering, accept all elements
                    matching_elems.append(elem_handle)
                    continue

                # Get attribute or text content
                attr_value = elem_handle.get_attribute(attribute) if attribute else elem_handle.text_content()

                if not attr_value:
                    continue

                if (substring and value in attr_value) or (not substring and value == attr_value):
                    matching_elems.append(elem_handle)

            matching_elements_count = len(matching_elems)

            if matching_elements_count < min_count and show_error:
                self.logger.warning(
                    "%s matching elements found, expected at least %d",
                    "Only {}".format(matching_elements_count) if matching_elems else "No",
                    min_count,
                )
                return (False, matching_elements_count)

        except PlaywrightError as e:
            if show_error:
                self.logger.error("Failed to check if elements -> '%s' exist; errors -> %s", selector, str(e))
            return (None, 0)

        return (True, matching_elements_count)

    # end method definition

    def run_login(
        self,
        user_field: str = "otds_username",
        password_field: str = "otds_password",
        login_button: str = "loginbutton",
        page: str = "",
        wait_until: str | None = None,
        selector_type: str = "id",
    ) -> bool:
        """Login to target system via the browser.

        Args:
            user_field (str, optional):
                The name of the web HTML field to enter the user name. Defaults to "otds_username".
            password_field (str, optional):
                The name of the HTML field to enter the password. Defaults to "otds_password".
            login_button (str, optional):
                The name of the HTML login button. Defaults to "loginbutton".
            page (str, optional):
                The URL to the login page. Defaults to "".
            wait_until (str | None, optional):
                Wait until a certain condition. Options are:
                * "load" - Waits for the load event (after all resources like images/scripts load)
                  This is the safest strategy for pages that keep loading content in the background
                  like Salesforce.
                * "networkidle" - Waits until there are no network connections for at least 500 ms.
                  This seems to be the safest one for OpenText Content Server.
                * "domcontentloaded" - Waits for the DOMContentLoaded event (HTML is parsed,
                  but subresources may still load).
            selector_type (str, optional):
                One of "id", "name", "class_name", "xpath", "css", "role", "text", "title",
                "label", "placeholder", "alt".
                Default is "id".

        Returns:
            bool: True = success, False = error.

        """

        # If no specific wait until strategy is provided in the
        # parameter, we take the one from the browser automation class:
        if wait_until is None:
            wait_until = self.wait_until

        self.logged_in = False

        if (
            not self.get_page(url=page, wait_until=wait_until)
            or not self.find_elem_and_set(selector=user_field, selector_type=selector_type, value=self.user_name)
            or not self.find_elem_and_set(
                selector=password_field, selector_type=selector_type, value=self.user_password, is_sensitive=True
            )
            or not self.find_elem_and_click(
                selector=login_button, selector_type=selector_type, is_navigation_trigger=True, wait_until=wait_until
            )
        ):
            self.logger.error(
                "Cannot log into target system using URL -> %s and user -> '%s'!",
                self.base_url,
                self.user_name,
            )
            return False

        self.page.wait_for_load_state(wait_until)

        title = self.get_title()
        if not title:
            self.logger.error(
                "Cannot read page title after login - you may have the wrong 'wait until' strategy configured!",
            )
            return False


        if "Verify" in title:
            self.logger.error("Site is asking for a Verification Token. You may need to whitelist your IP!")
            return False
        if "Login" in title:
            self.logger.error("Authentication failed. You may have given the wrong password!")
            return False

        self.logged_in = True

        return True

    # end method definition

    def set_timeout(self, wait_time: float) -> None:
        """Wait for the browser to finish tasks (e.g. fully loading a page).

        This setting is valid for the whole browser session and not just
        for a single command.

        Args:
            wait_time (float):
                The time in seconds to wait.

        """

        self.logger.debug("Setting default timeout to -> %s seconds...", str(wait_time))
        self.page.set_default_timeout(wait_time * 1000)
        self.logger.debug("Setting navigation timeout to -> %s seconds...", str(wait_time))
        self.page.set_default_navigation_timeout(wait_time * 1000)

    # end method definition

    def end_session(self) -> None:
        """End the browser session and close the browser."""

        self.logger.debug("Ending browser automation session...")
        self.context.close()
        self.browser.close()
        self.logged_in = False
        self.playwright.stop()

    # end method definition
