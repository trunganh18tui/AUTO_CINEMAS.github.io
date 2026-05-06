import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    # CHỈ CẦN DUY NHẤT DÒNG NÀY, Selenium sẽ tự lo việc phiên bản
    my_driver = webdriver.Chrome() 
    my_driver.maximize_window()
    
    my_driver.get("https://betacinemas.vn/") 
    
    yield my_driver 
    
    my_driver.quit()