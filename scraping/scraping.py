from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from models.sub_menu import SubMenu
from models.menu import Menu
from scraping.web_driver import *
from utils.os_utils import *

# Site home page url
url_home: str = "http://vitibrasil.cnpuv.embrapa.br/index.php"


def get_menu():
    """
        List all menus on the site
    """
    try:
        menu: list[Menu] = []
        driver = create_driver()
        driver.get(url_home)
        menu_bar = driver.find_element(by=By.ID, value="row_height")
        menu_bar_elements = menu_bar.find_elements(by=By.TAG_NAME, value="button")
        for element in menu_bar_elements:
            if element.text != "":
                value = element.get_attribute("value")
                menu_obj = Menu(id=value[value.index('_') + 1:], name=element.text, url=url_home + "?opcao=" + value)
                menu.append(menu_obj)
        driver.quit()
        return menu
    except:
        raise Exception("Error")


def get_sub_menu(url: str):
    """
        List all submenus
    """
    try:
        sub_menu: list[SubMenu] = []
        driver = create_driver()
        driver.get(url)
        sub_menu_bar_elements = driver.find_elements(by=By.CLASS_NAME, value="btn_sopt")
        for element in sub_menu_bar_elements:
            if element.text != "":
                value = element.get_attribute("value")
                id_menu = url[url.index('_') + 1:]
                id_sub_menu = value[value.index('_') + 1:]
                sub_menu_obj = SubMenu(id=id_menu + id_sub_menu, menu_id=id_menu, name=element.text, url=url + "&subopcao=" + value)
                sub_menu.append(sub_menu_obj)
        driver.quit()
        return sub_menu
    except:
        raise Exception("Error")


def get_csv_url(url):
    """
        search for csv file url on page
    """
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
    """
       download csv file
    """
    try:
        filename = generate_filename(filename)
        create_directory(filename)
        urlretrieve(url, filename)
        return {"status": "OK", "message": "download successfully"}
    except:
        return {"status": "ERROR", "message": "download error"}


def map_site():
    """
        maps the site returning all menus and sub menus
    """
    try:
        menus = get_menu()
        for menu in menus:
            menu.sub_menu = get_sub_menu(menu.url)
            if not menu.sub_menu:
                menu.csv_url = get_csv_url(menu.url)
            else:
                for sub_menu in menu.sub_menu:
                    sub_menu.csv_url = get_csv_url(sub_menu.url)
        return menus
    except:
        raise Exception("Error")


def download_all_csv():
    """
        goes through all the menus downloading the csv files that are found
    """
    try:
        menus = map_site()
        for menu in menus:
            if not menu.sub_menu:
                name = menu.name
                download_csv(get_csv_url(menu.url), name.replace(" ", "-"))
            else:
                for sub_menu in menu.sub_menu:
                    name = menu.name + '-' + sub_menu.name
                    download_csv(get_csv_url(sub_menu.url), name.replace(" ", "-"))
        return {"status": "OK", "message": "download successfully"}
    except:
        raise Exception("Error")
