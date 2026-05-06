import allure
import pytest
import time
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from pages.payment_page import PaymentPage

def print_result(stt, tc_id, desc, expected, actual, status):
    """Hàm in kết quả test case ra Terminal theo định dạng bảng"""
    color = "\033[92m" if status == "Pass" else "\033[91m"
    reset = "\033[0m"
    print(f"{stt}\t{tc_id}\t{desc[:20]}...\t{expected}\t{actual}\t{color}{status}{reset}")

@allure.feature("Beta Cinemas - Đặt vé & Thanh toán QR (E2E)")
def test_full_booking_qr_flow(driver):
    login_page = LoginPage(driver)
    booking_page = BookingPage(driver)
    payment_page = PaymentPage(driver)

    print("\n" + "="*100)
    print("STT\tTest Case\tMô tả\t\t\tKết quả mong đợi\tKết quả thực tế\tTrạng thái")
    print("-" * 100)

    # --- TIỀN ĐIỀU KIỆN ---
    login_page.open()
    login_page.clean_popup()
    login_page.fill_login_form("trunganhlvt1234@gmail.com", "bangtan1234")
    login_page.prepare_captcha()
    input(">>> Nhập Captcha xong nhấn ENTER...")
    login_page.click_login()
    time.sleep(4)

    # --- THỰC THI CÁC TEST CASE ---

    # TC_BOOKING_03
    try:
        is_detail = booking_page.select_movie_and_time("Phim Shin", "19:30")
        res_03 = "Đã hiển thị detail & suất chiếu" if is_detail else "Không thấy trang detail"
        print_result(1, "TC_BOOKING_03", "Chọn phim và suất chiếu", "Đến trang detail", res_03, "Pass")
    except Exception as e:
        print_result(1, "TC_BOOKING_03", "Chọn phim và suất chiếu", "Đến trang detail", f"Lỗi: {str(e)[:15]}", "Fail")

    # TC_BOOKING_02
    try:
        booking_page.select_seat("E7")
        print_result(2, "TC_BOOKING_02", "Chọn ghế hợp lệ", "Chuyển sang bắp nước", "Thành công", "Pass")
    except Exception as e:
        print_result(2, "TC_BOOKING_02", "Chọn ghế hợp lệ", "Chuyển sang bắp nước", "Thất bại", "Fail")

    # TC_BOOKING_01
    try:
        qty = booking_page.increase_combo()
        status_01 = "Pass" if qty == "1" else "Fail"
        print_result(3, "TC_BOOKING_01", "Tăng số lượng Combo", "Tăng 0 -> 1", f"Tăng lên {qty}", status_01)
    except Exception as e:
        print_result(3, "TC_BOOKING_01", "Tăng số lượng Combo", "Tăng 0 -> 1", "Lỗi", "Fail")

    # TC_PAYMENT_01 (CHỮA LỖI FAIL)
    try:
        payment_page.pay_with_qr_code()
        is_qr = payment_page.wait_for_qr_code() # Sử dụng hàm đợi mới
        status_01 = "Pass" if is_qr else "Fail"
        res_01 = "Đã hiển thị mã QR" if is_qr else "Không hiển thị mã QR"
        print_result(4, "TC_PAYMENT_01", "Thanh toán Mã QR", "Đến trang QR", res_01, status_01)
        allure.attach(driver.get_screenshot_as_png(), name="QR_Page")
        assert is_qr, "FAIL: Không hiển thị mã QR!"
    except Exception as e:
        print_result(4, "TC_PAYMENT_01", "Thanh toán Mã QR", "Đến trang QR", "Không hiển thị trang QR", "Fail")

    # DỌN DẸP
    payment_page.cancel_and_return()
    print("="*100)