from datetime import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager  # Import ChromeDriverManager

class GoldBarChallengeAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get("http://sdetchallenge.fetch.com/")

    def click_weigh_button(self):
        weigh_button = self.driver.find_element_by_id("weigh")
        weigh_button.click()

    def click_reset_button(self):
        reset_button = self.driver.find_element_by_id("reset")
        reset_button.click()

    def fill_bowl(self, left_bowl, right_bowl):
        for i in range(9):
            left_input = self.driver.find_element_by_id(f"left_{i}")
            right_input = self.driver.find_element_by_id(f"right_{i}")

            left_input.clear()
            left_input.send_keys(left_bowl[i])

            right_input.clear()
            right_input.send_keys(right_bowl[i])

    def get_measurement_result(self):
        result = self.driver.find_element_by_id("result")
        return result.text.strip()

    def click_fake_bar_number(self, fake_bar_number):
        fake_bar_button = self.driver.find_element_by_id(f"coin_{fake_bar_number}")
        fake_bar_button.click()

    def get_alert_message(self):
        time.sleep(1)  # Allow time for the alert to appear
        alert = self.driver.switch_to.alert
        alert_message = alert.text
        alert.accept()
        return alert_message

    def close_browser(self):
        self.driver.quit()


def find_fake_gold_bar():
    automation = GoldBarChallengeAutomation()

    # Weighing 1: Compare bars 0, 1 on the left side with bars 2, 3 on the right side
    left_bowl = [1, 0, 0, 0, 0, 0, 0, 0, 0]
    right_bowl = [0, 1, 0, 0, 0, 0, 0, 0, 0]
    automation.fill_bowl(left_bowl, right_bowl)
    automation.click_weigh_button()
    result = automation.get_measurement_result()

    if result == "left":
        # The fake bar is either 0 or 1
        fake_bar_number = 0 if automation.get_measurement_result() == "left" else 1
    elif result == "right":
        # The fake bar is either 2 or 3
        fake_bar_number = 2 if automation.get_measurement_result() == "left" else 3
    else:
        # Both sides are equal, initialize the fake_bar_number to 4 (arbitrary, as any of 4 to 8 can be fake)
        fake_bar_number = 4

        # Iterate through the remaining bars (4 to 8)
        for i in range(4, 9):
            # Weighing i: Compare the suspected fake bar with a known good bar
            left_bowl = [0] * 9
            right_bowl = [0] * 9
            left_bowl[fake_bar_number] = 1
            right_bowl[i] = 1
            automation.fill_bowl(left_bowl, right_bowl)
            automation.click_weigh_button()

            if automation.get_measurement_result() == "left":
                fake_bar_number = fake_bar_number if i < fake_bar_number else i
                break
            elif automation.get_measurement_result() == "right":
                fake_bar_number = fake_bar_number if i > fake_bar_number else i
                break

    automation.click_fake_bar_number(fake_bar_number)

    alert_message = automation.get_alert_message()

    print("Alert Message:", alert_message)
    print("Number of Weighings:", 1)  # Modify accordingly
    print("List of Weighings:", ["Weighing 1: Left vs Right"])  # Modify accordingly

    automation.close_browser()

find_fake_gold_bar()
