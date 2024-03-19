from selenium import webdriver
from userInfo import username, password
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Instagram:
    driver_path = "/Users/doganeceilayda/Desktop/chromedriver_mac_arm64"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.followers = []

        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option("prefs",{"intl.accept_languages":"en,en_US"})

        self.browser = webdriver.Chrome(Instagram.driver_path, options=self.browserProfile)

    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)

        usernameInput = self.browser.find_element(By.NAME, "username")
        passwordInput = self.browser.find_element(By.NAME, "password")

        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)

        passwordInput.send_keys(Keys.ENTER)
        time.sleep(5)

        try:
            self.browser.find_element(By.CLASS_NAME, "cmbtv").find_element(By.TAG_NAME, "button").click()
            time.sleep(4)
        except:
            pass

        try:
            self.browser.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div[3]/button[2]").click()
            time.sleep(4)
        except:
            pass

    def getFollowers(self, max):
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(3)
        follower_button = self.browser.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        follower_button.click()
        time.sleep(3)

        dialog = self.browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]')
        count = len(dialog.find_elements(By.CSS_SELECTOR, 'li'))

        print(f"takipci sayisi: {count}")

        while count < max:
            dialog.click()
            action = webdriver.ActionChains(self.browser)
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)

            new_count = len(dialog.find_elements(By.CSS_SELECTOR, 'li'))

            if count != new_count:
                count = new_count
                print(f"takipci sayisi: {count}")
                time.sleep(1)
            else:
                break

        followers = dialog.find_elements(By.CSS_SELECTOR, 'li')[:max]

        for user in followers:
            link = user.find_element(By.TAG_NAME, "a").get_attribute("href")
            self.followers.append(link)

        self.saveToFile(self.followers)

    def saveToFile(self, followers):
        with open ("followers.txt","w", encoding="UTF-8") as file:
            for user in followers:
                file.write(user + "\n")

    def followUser(self, username):
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(2)

        followButton = self.browser.find_element(By.TAG_NAME, "button")

        if followButton.text == "Follow" or followButton.text == "Follow Back":
            followButton.click()
            time.sleep(2)
        else:
            print(f"{username} sayfasini zaten takip ediyorsunuz.")

    def followUsers(self, users):
        for user in users:
            self.followUser(user)

    def unFollowUser(self, username):
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(2)

        btn = self.browser.find_element(By.TAG_NAME, "button")
        if btn.text == "Following":
            btn.click()
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Unfollow"]'))).click()
            time.sleep(2)
        else:
            print(f"{username} sayfasini zaten takip etmiyorsunuz.")

    def unFollowUsers(self, users):
        for user in users:
            self.unFollowUser(user)

    def __del__(self):
        time.sleep(5)
        self.browser.quit()

app = Instagram(username, password)
app.signIn()
app.getFollowers(50)
app.followUsers(["eceilaydadogan","netflix"])
app.unFollowUsers(["netflix"])
