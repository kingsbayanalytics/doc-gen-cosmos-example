from base.base import BasePage
from playwright.sync_api import expect


class HomePage(BasePage):
    BROWSE_BUTTON = (
        "//p[contains(text(),'Let AI search through your files and provide answe')]"
    )
    HOME_TITLE = "//h2[normalize-space()='AI-powered document search and creation.']"
    BROWSE_TEXT = (
        "//p[contains(text(),'Let AI search through your files and provide answe')]"
    )
    GENERATE_TEXT = (
        "//p[normalize-space()='Have AI generate draft documents to save you time']"
    )

    def __init__(self, page):
        self.page = page

    def click_browse_button(self):
        # click on BROWSE
        self.page.wait_for_timeout(3000)
        self.page.locator(self.BROWSE_BUTTON).click()
        self.page.wait_for_timeout(5000)

    def validate_home_page(self):
        expect(self.page.locator(self.HOME_TITLE)).to_be_visible()
        expect(self.page.locator(self.BROWSE_TEXT)).to_be_visible()
        expect(self.page.locator(self.GENERATE_TEXT)).to_be_visible()
