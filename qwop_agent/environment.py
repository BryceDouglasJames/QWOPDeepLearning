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
        # Initialize the driver, for now, it will just look for Safari
        self.driver = webdriver.Safari(executable_path=driver_path) if driver_path else webdriver.Safari()
        self.driver.get("http://www.foddy.net/Athletics.html")

        # Allow some time for the page to load
        time.sleep(2) 

        # Focus on the canvas where the game is rendered
        self.canvas = self.driver.find_element(By.CSS_SELECTOR, 'canvas')
        self.canvas.click()
        time.sleep(2) 

        # Initialize distance tracking for reward calculation
        self.previous_distance = 0

    def press_key(self, key: chr, duration: float = 0) -> None:
        ActionChains(self.driver) \
            .key_down(key) \
            .pause(duration)\
            .key_up(key)\
            .perform()        
       
    def get_player_state(self) -> Image:
        image = self.driver.get_screenshot_as_png()  
        image = Image.open(BytesIO(image))
        image = image.crop([420, 280, 1220, 925])
        return image

    def get_distance_state(self) -> float:
        image = self.driver.get_screenshot_as_png()  
        image = Image.open(BytesIO(image))
        image = image.crop([560, 170, 723, 230])

        # Using pytesseract to convert image to string
        distance = pytesseract.image_to_string(image, config='--psm 6')
        print("Extracted Text:", distance)
        self.previous_distance = distance
        return float(distance)

    def reset_game(self) -> None:
        self.driver.refresh()
        time.sleep(2)
        self.canvas = self.driver.find_element(By.CSS_SELECTOR, 'canvas')
        self.canvas.click()

    def is_game_over(self) -> bool:
        image = self.driver.get_screenshot_as_png()  
        image = Image.open(BytesIO(image))

        # Check if gg ribbons are displayed 
        pixel = image.getpixel((450, 350))

        if pixel[0] > 200:
            return True
        return False

    def close(self) -> None:
        self.driver.close()