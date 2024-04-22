from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
import pytesseract
from io import BytesIO

class QWOPEnvironment:
    def __init__(self, driver_path=None):
        self.driver = webdriver.Safari(executable_path=driver_path) if driver_path else webdriver.Safari()
        self.driver.get("http://www.foddy.net/Athletics.html")
        time.sleep(4)
        self.canvas = self.driver.find_element(By.CSS_SELECTOR, 'canvas')
        self.canvas.click()
        time.sleep(1)

    def press_key(self, key: str, duration: float):
        actions = ActionChains(self.driver)
        actions.key_down(key).pause(duration).key_up(key).perform()

    def get_player_state(self):
        image = self.driver.get_screenshot_as_png()
        image = Image.open(BytesIO(image))
        return image.crop((420, 280, 1220, 925))

    def get_distance_state(self):
        image = self.driver.get_screenshot_as_png()
        image = Image.open(BytesIO(image)).crop((560, 170, 723, 230))
        distance_text = pytesseract.image_to_string(image, config='--psm 6')
        try:
            return float(distance_text)
        except ValueError:
            return 0.0

    def reset_game(self) -> None:
        self.driver.refresh()
        time.sleep(5)
        self.canvas = self.driver.find_element(By.CSS_SELECTOR, 'canvas')
        self.canvas.click()


    def is_game_over(self):
        pixel = Image.open(BytesIO(self.driver.get_screenshot_as_png())).getpixel((450, 350))
        return pixel[0] > 200

    def close(self):
        self.driver.quit()