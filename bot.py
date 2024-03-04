from os import system
from time import sleep
from colorama import init, Fore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

init(autoreset=True)


class Bot:
    def __init__(self):
        system("cls || clear")
        self.printBanner()
        print(Fore.YELLOW + "[~] Loading driver, please wait...")

        try:
            options = Options()
            options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
            )
            self.driver = webdriver.Chrome(options=options)

            print(Fore.GREEN + "[+] Driver loaded successfully")
            print()
        except Exception as e:
            print(Fore.RED + f"[!] Error loading driver: {e}")
            exit()

        self.url = "https://zefoy.com"
        self.captcha_xpath = "/html/body/div[5]/div[2]/form/div/div/div/div/button"
        self.services = {
            "followers": {
                "title": "Followers",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",
                "status": None,
            },
            "hearts": {
                "title": "Hearts",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[3]/div/button",
                "status": None,
            },
            "comment_hearts": {
                "title": "Comment Hearts",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[4]/div/button",
                "status": None,
            },
            "views": {
                "title": "Views",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[5]/div/button",
                "status": None,
            },
            "shares": {
                "title": "Shares",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[6]/div/button",
                "status": None,
            },
            "favorites": {
                "title": "Favorites",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[7]/div/button",
                "status": None,
            },
        }

    def start(self):
        self.driver.get(self.url)

        print(Fore.MAGENTA + "[!] In case of a 502 Bad Gateway error")
        print(Fore.MAGENTA + "[!] please refresh the page")
        print()

        self.wait_for_xpath(self.captcha_xpath)

        print(Fore.YELLOW + "[~] Please complete the captcha")

        self.wait_for_xpath(self.services["followers"]["xpath"])

        print(Fore.GREEN + "[+] Captcha completed successfully")
        print()

        self.driver.minimize_window()
        self.check_services()

        for index, service in enumerate(self.services):
            title = self.services[service]["title"]
            status = self.services[service]["status"]

            print(Fore.BLUE + f"[{str(index + 1)}] {title}".ljust(20), status)

        while True:
            try:
                choice = int(input(Fore.YELLOW + "[-] Choose an option : "))
            except ValueError:
                continue  # This ensures the loop continues after a ValueError

            if choice in range(1, 7):
                break

        self.select_service(choice)

    def select_service(self, choice):
        div = 6 + choice
        service_key = list(self.services.keys())[choice - 1]

        self.driver.find_element(By.XPATH, self.services[service_key]["xpath"]).click()

        print()
        video_url = input(Fore.MAGENTA + "[-] Video URL : ")
        print()

        self.start_service(div, video_url)

    def start_service(self, div, video_url):
        url_input_xpath = f"/html/body/div[{div}]/div/form/div/input"
        search_btn_xpath = f"/html/body/div[{div}]/div/form/div/div/button"
        send_btn_xpath = f"/html/body/div[{div}]/div/div/div[1]/div/form/button"

        input_element = self.driver.find_element(By.XPATH, url_input_xpath)
        input_element.clear()
        input_element.send_keys(video_url)

        while True:
            # Click the search button
            self.driver.find_element(By.XPATH, search_btn_xpath).click()

            # Attempt to click the send button if it's present
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, send_btn_xpath))
                ).click()
            except TimeoutException:
                # If the send button isn't found, click the search button again
                self.driver.find_element(By.XPATH, search_btn_xpath).click()

            remaining_time = self.check_remaining_time(div)

            if remaining_time is not None:
                print(Fore.YELLOW + f"[~] Sleeping for {remaining_time} seconds")
                sleep(remaining_time)

    def check_remaining_time(self, div):
        remaining_time_xpath = f"/html/body/div[{div}]/div/div/span[1]"

        try:
            element = self.driver.find_element(By.XPATH, remaining_time_xpath)
            text = element.text

            if "Please wait" in text:
                minutes = text.split("Please wait ")[1].split(" ")[0]
                seconds = text.split(" second")[0].split()[-1]
                sleep_duration = int(minutes) * 60 + int(seconds) + 5

                return sleep_duration
            else:
                return None
        except NoSuchElementException:
            return None

    def check_services(self):
        for service in self.services:
            xpath = self.services[service]["xpath"]

            try:
                element = self.driver.find_element(By.XPATH, xpath)

                if element.is_enabled():
                    self.services[service]["status"] = Fore.GREEN + "[WORKING]"
                else:
                    self.services[service]["status"] = Fore.RED + "[OFFLINE]"
            except NoSuchElementException:
                self.services[service]["status"] = Fore.RED + "[OFFLINE]"

    def wait_for_xpath(self, xpath):
        while True:
            try:
                self.driver.find_element(By.XPATH, xpath)
                return True
            except NoSuchElementException:
                sleep(1)

    def printBanner(self):
        print(
            """
████████╗██╗██╗░░██╗████████╗░█████╗░██╗░░██╗  ██████╗░░█████╗░████████╗
╚══██╔══╝██║██║░██╔╝╚══██╔══╝██╔══██╗██║░██╔╝  ██╔══██╗██╔══██╗╚══██╔══╝
░░░██║░░░██║█████═╝░░░░██║░░░██║░░██║█████═╝░  ██████╦╝██║░░██║░░░██║░░░
░░░██║░░░██║██╔═██╗░░░░██║░░░██║░░██║██╔═██╗░  ██╔══██╗██║░░██║░░░██║░░░
░░░██║░░░██║██║░╚██╗░░░██║░░░╚█████╔╝██║░╚██╗  ██████╦╝╚█████╔╝░░░██║░░░
░░░╚═╝░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝  ╚═════╝░░╚════╝░░░░╚═╝░░░

Made by : Simon Farah
Github  : https://github.com/simonfarah/tiktok-bot

------------------------------------------------------------------------
"""
        )


if __name__ == "__main__":
    bot = Bot()
    bot.start()
