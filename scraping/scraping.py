from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from scraping.web_driver import *
from utils.os_utils import *


url_home: str = "http://vitibrasil.cnpuv.embrapa.br/index.php"


def get_menu():
    try:
        menu: list = []
        driver = create_driver()
        driver.get(url_home)
        menu_bar = driver.find_element(by=By.ID, value="row_height")
        menu_bar_elements = menu_bar.find_elements(by=By.TAG_NAME, value="button")
        for element in menu_bar_elements:
            if element.text != "":
                value = element.get_attribute("value")
                menu_obj = {"id": value[value.index('_') + 1:], "nome": element.text, "link": url_home + "?opcao=" + value}
                menu.append(menu_obj)
        driver.quit()
        return menu
    except:
        raise Exception("Error")


def get_sub_menu(url: str):
    try:
        sub_menu: list = []
        driver = create_driver()
        driver.get(url)
        sub_menu_bar_elements = driver.find_elements(by=By.CLASS_NAME, value="btn_sopt")
        for element in sub_menu_bar_elements:
            if element.text != "":
                value = element.get_attribute("value")
                id_menu = url[url.index('_') + 1:]
                id_sub_menu = value[value.index('_') + 1:]
                sub_menu_obj = {"id": id_menu + id_sub_menu, "nome": element.text, "link": url + "&subopcao=" + value}
                sub_menu.append(sub_menu_obj)
        driver.quit()
        return sub_menu
    except:
        raise Exception("Error")


def get_csv_link(url):
    try:
        driver = create_driver()
        csv_url = ""
        driver.get(url)
        elements = driver.find_elements(by=By.TAG_NAME, value="a")
        for element in elements:
            url_aux = element.get_attribute("href")
            if ".csv" in url_aux:
                csv_url = url_aux
        driver.quit()
        return csv_url
    except:
        raise Exception("Error")


def download_csv(url, filename):
    try:
        filename = generate_filename(filename)
        create_directory(filename)
        urlretrieve(url, filename)
        return {"status": "OK", "message": "download successfully"}
    except:
        return {"status": "ERROR", "message": "download error"}


def map_site():
    try:
        menus = get_menu()
        for menu in menus:
            menu["sub_menu"] = get_sub_menu(menu.get("link"))
            if not menu.get("sub_menu"):
                menu["csv_link"] = get_csv_link(menu.get("link"))
            else:
                for sub_menu in menu.get("sub_menu"):
                    sub_menu["csv_link"] = get_csv_link(sub_menu.get("link"))
        return menus
    except:
        raise Exception("Error")


def download_all_csv():
    try:
        menus = get_menu()
        for menu in menus:
            menu["sub_menu"] = get_sub_menu(menu.get("link"))
            if not menu.get("sub_menu"):
                name = menu.get("nome")
                download_csv(get_csv_link(menu.get("link")), name.replace(" ", "-"))
            else:
                for sub_menu in menu.get("sub_menu"):
                    name = f"{menu.get("nome")}-{sub_menu.get("nome")}"
                    download_csv(get_csv_link(sub_menu.get("link")), name.replace(" ", "-"))
        return {"result": "success"}
    except:
        raise Exception("Error")
