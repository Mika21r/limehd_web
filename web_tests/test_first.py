import pytest
from playwright.sync_api import sync_playwright, expect
import allure

@allure.feature("Веб-приложение LimeHD")
class TestLimeHDWeb:

    @allure.title("Добавление канала в избранное и проверка в разделе Избранное")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_to_favorites(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            with allure.step("Открыть главную страницу"):
                page.goto("https://limehd.tv/")
                page.wait_for_load_state("domcontentloaded")

            channel_name = "Матч ТВ"

            with allure.step(f"Найти канал '{channel_name}' и нажать на звездочку добавления в избранное"):
                channel_card = page.locator("a[data-test='channel-name-link']").filter(has_text=channel_name)
                channel_card.locator("[data-test='favorite-add']").click()

            with allure.step("Перейти в раздел 'Избранное'"):
                page.get_by_text("Избранное", exact=True).first.click()
                page.wait_for_load_state("domcontentloaded")

            with allure.step(f"Проверить, что канал '{channel_name}' отображается в Избранном"):
                favorite_locator = page.locator("a[data-test='channel-name-link']", has_text=channel_name)
                expect(favorite_locator).to_be_visible(timeout=10000)

            context.close()
            page.close()
            browser.close()