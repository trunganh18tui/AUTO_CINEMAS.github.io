from pages.payment_page import PaymentPage
import time

def test_payment_without_terms(driver):
    # TODO: Điền link của trang thanh toán vào đây
    driver.get("https://betacinemas.vn/LINK_TRANG_THANH_TOAN")
    time.sleep(2)
    
    payment_page = PaymentPage(driver)
    
    # Gửi False để KHÔNG tích vào ô điều khoản
    payment_page.choose_vnpay_and_pay(check_agree=False)
    
    error = payment_page.get_terms_error()
    # TODO: Thay chữ báo lỗi dưới đây cho đúng với thực tế
    assert "Bạn phải đồng ý" in error