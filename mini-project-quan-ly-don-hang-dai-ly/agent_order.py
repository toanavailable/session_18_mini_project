"""Agent Order - Hệ thống quản lý đơn hàng đại lý (theo tài liệu SRS).

Mỗi đơn hàng (OrderRecord) là một Dictionary:
    {"id": str, "agent_name": str, "total_amount": int | float, "status": "Paid" | "Unpaid"}
Toàn bộ logic nằm trong các hàm; danh sách đơn hàng được tạo trong main() và truyền qua tham số.
"""

DISCOUNT_THRESHOLD = 100_000_000   # Mốc doanh thu được hưởng chiết khấu (VND)
DISCOUNT_RATE = 5                  # Chiết khấu 5% khi đạt mốc
LINE_WIDTH = 66


# =====================================================================
# CÁC HÀM PHỤ TRỢ
# =====================================================================
def format_money(amount):
    """Định dạng số tiền có dấu phẩy ngăn cách hàng nghìn.

    Tham số:
        amount (int | float): số tiền
    Trả về:
        str: ví dụ 45000000 -> "45,000,000"
    """
    if isinstance(amount, float) and amount.is_integer():
        amount = int(amount)
    return f"{amount:,}"


def input_required_text(prompt, field_name):
    """Nhập một trường chữ bắt buộc, lặp lại cho đến khi không rỗng.

    Tham số:
        prompt (str): câu nhắc nhập liệu
        field_name (str): tên trường để in thông báo lỗi
    Trả về:
        str: chuỗi đã bỏ khoảng trắng thừa
    """
    while True:
        text = " ".join(input(prompt).split())
        if text != "":
            return text
        print(f"[Lỗi]: {field_name} không được để trống!")


def input_amount(prompt):
    """Nhập giá trị đơn hàng, dùng try-except bắt lỗi ép kiểu, lặp đến khi là số > 0.

    Tham số:
        prompt (str): câu nhắc nhập liệu
    Trả về:
        int | float: giá trị hợp lệ (số nguyên nếu người dùng nhập số nguyên)
    """
    while True:
        text = input(prompt).strip()
        try:
            amount = float(text)
        except ValueError:
            print("[Lỗi]: Giá trị đơn hàng phải là số tiền lớn hơn 0! (ERR-02)")
            continue
        if not 0 < amount < float("inf"):          # chặn số âm, 0, nan, inf
            print("[Lỗi]: Giá trị đơn hàng phải là số tiền lớn hơn 0! (ERR-02)")
            continue
        return int(amount) if amount.is_integer() else amount


def find_order(orders_list, order_id):
    """Tìm đơn hàng theo mã.

    Tham số:
        orders_list (list[dict]): danh sách đơn hàng
        order_id (str): mã đơn hàng đã chuẩn hóa
    Trả về:
        dict | None: chính Dictionary của đơn hàng (để sửa trực tiếp), hoặc None nếu không có
    """
    for order in orders_list:
        if order["id"] == order_id:
            return order
    return None


# =====================================================================
# CÁC HÀM CHỨC NĂNG (THEO SRS)
# =====================================================================
def display_menu():
    """In menu chính. Không trả về giá trị."""
    print("\n" + "═" * 40)
    print(f"{'QUẢN LÝ ĐƠN HÀNG - AGENT ORDER':^40}")
    print("═" * 40)
    print("1. Xem danh sách đơn hàng hiện có")
    print("2. Tạo mới đơn hàng đại lý")
    print("3. Cập nhật trạng thái thanh toán")
    print("4. Tính tổng doanh thu & Chiết khấu")
    print("5. Thoát chương trình")
    print("═" * 40)


def show_orders(orders_list):
    """Chức năng 1: in danh sách đơn hàng dạng bảng căn lề. Không trả về giá trị.

    Tham số:
        orders_list (list[dict]): danh sách đơn hàng
    """
    if len(orders_list) == 0:
        print("Hệ thống hiện chưa có đơn hàng nào!")
        return
    print("── DANH SÁCH ĐƠN HÀNG ĐẠI LÝ ──")
    print(f"{'MÃ ĐƠN':<8}| {'TÊN ĐẠI LÝ':<22}| {'GIÁ TRỊ (VND)':>15} | TRẠNG THÁI")
    print("─" * LINE_WIDTH)
    for order in orders_list:
        print(f"{order['id']:<8}| {order['agent_name']:<22}| "
              f"{format_money(order['total_amount']):>15} | {order['status']}")
    print("─" * LINE_WIDTH)


def create_order(orders_list):
    """Chức năng 2: thu thập, validate và thêm đơn hàng mới (trạng thái mặc định Unpaid).

    Tham số:
        orders_list (list[dict]): danh sách đơn hàng gốc (được cập nhật trực tiếp trên vùng nhớ)
    Trả về:
        bool: True nếu tạo thành công, False nếu bị hủy do trùng mã
    """
    print("── TẠO MỚI ĐƠN HÀNG ──")
    order_id = input_required_text("Nhập mã đơn hàng: ", "Mã đơn hàng").replace(" ", "").upper()
    if find_order(orders_list, order_id) is not None:
        print("[Lỗi]: Mã đơn hàng này đã tồn tại trong hệ thống! (ERR-01)")
        return False

    agent_name = input_required_text("Nhập tên đại lý: ", "Tên đại lý")
    total_amount = input_amount("Nhập giá trị đơn hàng (VND): ")

    orders_list.append({
        "id": order_id,
        "agent_name": agent_name,
        "total_amount": total_amount,
        "status": "Unpaid",
    })
    print(f"[Thành công]: Đơn hàng {order_id} đã được tạo thành công!")
    return True


def update_payment_status(orders_list):
    """Chức năng 3: chuyển trạng thái đơn hàng từ Unpaid sang Paid theo mã.

    Tham số:
        orders_list (list[dict]): danh sách đơn hàng gốc
    Trả về:
        bool: True nếu cập nhật thành công, False nếu lỗi (ERR-03, ERR-04, danh sách rỗng)
    """
    print("── CẬP NHẬT TRẠNG THÁI THANH TOÁN ──")
    if len(orders_list) == 0:
        print("Hệ thống hiện chưa có đơn hàng nào!")
        return False

    order_id = input_required_text("Nhập mã đơn hàng cần cập nhật: ", "Mã đơn hàng").replace(" ", "").upper()
    order = find_order(orders_list, order_id)
    if order is None:
        print(f"[Lỗi]: Không tìm thấy đơn hàng nào có mã [{order_id}]! (ERR-03)")
        return False
    if order["status"] == "Paid":
        print("[Lỗi]: Đơn hàng này đã được thanh toán trước đó! (ERR-04)")
        return False

    print(f"Tìm thấy đơn hàng của: {order['agent_name']} "
          f"(Giá trị: {format_money(order['total_amount'])})")
    order["status"] = "Paid"            # sửa trực tiếp Dictionary trong danh sách gốc
    print(f"[Thành công]: Đơn hàng {order_id} đã được cập nhật trạng thái ĐÃ THANH TOÁN!")
    return True


def calculate_financials(orders_list):
    """Chức năng 4: tính doanh thu thực tế (đơn Paid) và chiết khấu. KHÔNG in ra màn hình.

    Tham số:
        orders_list (list[dict]): danh sách đơn hàng
    Trả về:
        tuple (total_revenue, discount_percent, discount_amount):
            total_revenue (int | float): tổng giá trị các đơn đã thanh toán
            discount_percent (int): 5 nếu doanh thu >= 100,000,000 VND, ngược lại 0
            discount_amount (int | float): tiền chiết khấu = doanh thu * phần trăm / 100
    """
    total_revenue = 0
    for order in orders_list:
        if order["status"] == "Paid":
            total_revenue += order["total_amount"]
    discount_percent = DISCOUNT_RATE if total_revenue >= DISCOUNT_THRESHOLD else 0
    discount_amount = total_revenue * discount_percent / 100
    if discount_amount == int(discount_amount):
        discount_amount = int(discount_amount)
    return total_revenue, discount_percent, discount_amount


def print_financial_report(orders_list):
    """Gọi calculate_financials, nhận Tuple kết quả và in báo cáo tài chính."""
    print("── BÁO CÁO TÀI CHÍNH DOANH NGHIỆP ──")
    if len(orders_list) == 0:
        print("Hệ thống hiện chưa có đơn hàng nào!")
        return
    total_revenue, discount_percent, discount_amount = calculate_financials(orders_list)
    print(f"+ Tổng doanh thu thực tế (Đã thanh toán): {format_money(total_revenue)} VND")
    print(f"+ Tỷ lệ chiết khấu áp dụng: {discount_percent}%")
    print(f"+ Số tiền chiết khấu đại lý nhận lại: {format_money(discount_amount)} VND")


# =====================================================================
# HÀM ĐIỀU PHỐI CHÍNH
# =====================================================================
def main():
    """Vòng lặp menu while True: nhận lựa chọn (có try-except) và gọi hàm chức năng."""
    orders = [
        {"id": "HD01", "agent_name": "Dai ly Hoang Long", "total_amount": 45000000, "status": "Paid"},
        {"id": "HD02", "agent_name": "Tap hoa Minh Thu", "total_amount": 15000000, "status": "Unpaid"},
    ]
    while True:
        display_menu()
        try:
            choice = int(input("Mời chọn chức năng (1-5): "))
        except ValueError:
            print("[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5! (ERR-05)")
            continue

        if choice == 1:
            show_orders(orders)
        elif choice == 2:
            create_order(orders)
        elif choice == 3:
            update_payment_status(orders)
        elif choice == 4:
            print_financial_report(orders)
        elif choice == 5:
            print("Cảm ơn bạn đã sử dụng phần mềm!")
            print("[Chương trình kết thúc]")
            break
        else:
            print("[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5! (ERR-05)")


if __name__ == "__main__":
    main()
