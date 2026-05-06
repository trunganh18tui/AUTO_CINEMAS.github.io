import allure
import pytest
import random
import time
import json
import os
from pages.register_page import RegisterPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, TimeoutException

def load_test_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.normpath(os.path.join(project_root, "data", "register_data.json"))
    with open(data_path, encoding='utf-8') as f:
        return json.load(f)

@allure.feature("Beta Cinemas - POM Testing")
@pytest.mark.parametrize("data", load_test_data())
def test_full_registration_scenarios(driver, data):
    register_page = RegisterPage(driver)
    allure.dynamic.title(f"{data['tc_id']}: {data['description']}")

    with allure.step("1. Truy cập trang"):
        register_page.open()
        time.sleep(3)
        register_page.clean_popup()

    with allure.step("2. Nhập thông tin"):
        ts = str(int(time.time()))[-5:]
        # Email: Nếu JSON để 'auto' thì tạo email hợp lệ, ngược lại lấy từ JSON để test lỗi
        email = f"tester_{ts}@gmail.com" if data['email'] == "auto" else data['email']
        phone = f"0912{random.randint(100000,999999)}"
        register_page.fill_form(data, email, phone)

    with allure.step("3. Nhập Captcha"):
        register_page.get_ready_for_captcha()
        print(f"\n>>> ĐANG CHẠY: {data['tc_id']}")
        print(f">>> EMAIL NHẬP: {email} | KỲ VỌNG: {data['expected_result']}")
        input(">>> NHẬP CAPTCHA RỒI NHẤN ENTER TẠI TERMINAL...")

    with allure.step("4. Kiểm tra kết quả"):
        register_page.click_register()
        time.sleep(5)
        
        actual_res = ""
        try:
            # 1. Kiểm tra Alert (Lỗi Sai mã xác thực thường hiện ở đây)
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            actual_res = alert.text
            alert.accept()
        except:
            # 2. Nếu không có Alert, kiểm tra nội dung trang
            if "login.htm" in driver.current_url:
                actual_res = "Đăng ký tài khoản thành công"
            else:
                # Tìm các thông báo lỗi hiển thị trên trang (màu đỏ)
                try:
                    # Beta Cinemas dùng class 'text-danger' hoặc các thẻ label error
                    errors = driver.find_elements(By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'danger')]")
                    # Lấy danh sách text, lọc bỏ chuỗi rỗng
                    err_msgs = [e.text for e in errors if e.is_displayed() and len(e.text) > 3]
                    actual_res = " | ".join(err_msgs) if err_msgs else "Thất bại không xác định"
                except:
                    actual_res = "Thất bại - Web treo"

        print(f"\n[KẾT QUẢ THỰC TẾ]: {actual_res}")
        allure.attach(driver.get_screenshot_as_png(), name="Result", attachment_type=allure.attachment_type.PNG)
        
        # ASSERTION CHUẨN: Kiểm tra xem thông báo của web có chứa từ khóa kỳ vọng không
        assert data['expected_result'].lower() in actual_res.lower(), \
            f"FAIL {data['tc_id']}! Kỳ vọng: '{data['expected_result']}', Thực tế: '{actual_res}'"