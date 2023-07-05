import pytest
from selenium import webdriver


@pytest.fixture(params=["chrome"],scope="class")
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    elif request.param == "safari":
        driver = webdriver.Safari()
    else:
        print("The given parameters are not matched")
    driver.maximize_window()
    driver.get("https://npiregistry.cms.hhs.gov/search")
    request.cls.driver = driver
    yield
    driver.quit()



