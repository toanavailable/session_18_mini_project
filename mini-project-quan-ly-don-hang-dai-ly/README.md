# Mini Project - Hệ thống Quản lý Đơn hàng Đại lý (Agent Order)

Chương trình dòng lệnh (CLI) quản lý đơn hàng giữa tổng kho và các đại lý, xây dựng theo tài liệu **SRS - Quản lý đơn hàng Đại lý**. Dữ liệu tổ chức bằng **List của Dictionary**; **toàn bộ logic nằm trong các hàm độc lập**, không có mã nguồn tự do bên ngoài hàm.

## 1. Mục tiêu

- Vận dụng cấu trúc dữ liệu List của Dictionary để tổ chức dữ liệu dạng bản ghi.
- Thành thạo tư duy lập trình hàm: chia nhỏ bài toán, thiết kế và đặt tên hàm, truyền tham số và trả về giá trị (`return`).
- Áp dụng tư duy phân tích yêu cầu từ tài liệu đặc tả (SRS) vào lập trình thực tế.
- Quản lý dự án trên GitHub.

## 2. Mô tả bài toán

### Menu bắt buộc

```
════════════════════════════════════════
     QUẢN LÝ ĐƠN HÀNG - AGENT ORDER     
════════════════════════════════════════
1. Xem danh sách đơn hàng hiện có
2. Tạo mới đơn hàng đại lý
3. Cập nhật trạng thái thanh toán
4. Tính tổng doanh thu & Chiết khấu
5. Thoát chương trình
════════════════════════════════════════
Mời chọn chức năng (1-5): 
```

### Yêu cầu chức năng (theo SRS)

| Lựa chọn | Chức năng | Hàm (tên theo SRS) | Mô tả |
|---|---|---|---|
| 1 | Xem danh sách đơn hàng | `show_orders(orders_list)` | In bảng căn lề; danh sách trống thì báo "Hệ thống hiện chưa có đơn hàng nào!". Không trả về giá trị |
| 2 | Tạo mới đơn hàng | `create_order(orders_list)` | Nhập mã, tên đại lý, giá trị; kiểm tra trùng mã, chuỗi rỗng, số tiền > 0; trạng thái mặc định `Unpaid`; thêm trực tiếp vào danh sách |
| 3 | Cập nhật thanh toán | `update_payment_status(orders_list)` | Tìm theo mã: không thấy → ERR-03; đã `Paid` → ERR-04; `Unpaid` → chuyển sang `Paid` |
| 4 | Doanh thu & chiết khấu | `calculate_financials(orders_list)` | Cộng các đơn `Paid`; ≥ 100,000,000 VND chiết khấu 5%, ngược lại 0%; **return Tuple** `(tổng doanh thu, % chiết khấu, tiền chiết khấu)`; nơi gọi hàm tự in kết quả |
| 5 | Thoát | `main()` | In lời chào và dừng chương trình |

### Danh mục mã lỗi (SRS mục 5, 6)

| Mã lỗi | Thông báo | Vị trí | Xử lý |
|---|---|---|---|
| ERR-01 | `[Lỗi]: Mã đơn hàng này đã tồn tại trong hệ thống!` | Tạo đơn | Hủy thao tác, quay lại menu |
| ERR-02 | `[Lỗi]: Giá trị đơn hàng phải là số tiền lớn hơn 0!` | Tạo đơn | Số âm, 0 hoặc chữ → nhập lại số tiền đến khi hợp lệ |
| ERR-03 | `[Lỗi]: Không tìm thấy đơn hàng nào có mã [Mã số]!` | Cập nhật đơn | Kết thúc hàm xử lý |
| ERR-04 | `[Lỗi]: Đơn hàng này đã được thanh toán trước đó!` | Cập nhật đơn | Giữ nguyên dữ liệu |
| ERR-05 | `[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5!` | Menu chính | Chữ hoặc số ngoài [1, 5] → quay lại menu |

## 3. Phân tích và thiết kế

### 3.1. Thiết kế dữ liệu (OrderRecord)

```python
orders = [
    {"id": "HD01", "agent_name": "Dai ly Hoang Long", "total_amount": 45000000, "status": "Paid"},
    {"id": "HD02", "agent_name": "Tap hoa Minh Thu", "total_amount": 15000000, "status": "Unpaid"},
]
```

| Trường | Kiểu | Ý nghĩa | Ràng buộc |
|---|---|---|---|
| `id` | str | Mã đơn hàng duy nhất | Không rỗng, không trùng, chuẩn hóa viết hoa, bỏ khoảng trắng |
| `agent_name` | str | Tên đại lý | Không rỗng, gộp khoảng trắng thừa |
| `total_amount` | int / float | Giá trị đơn hàng (VND) | Số và > 0 |
| `status` | str | Trạng thái thanh toán | Chỉ `"Paid"` hoặc `"Unpaid"`; mặc định `"Unpaid"` |

Danh sách `orders` được tạo **trong `main()`** và truyền vào các hàm qua tham số `orders_list`. List và dict là kiểu mutable, nên `append()` hay `order["status"] = "Paid"` trong hàm thay đổi ngay dữ liệu gốc trong `main()` (yêu cầu toàn vẹn dữ liệu, SRS 3.1). Chương trình không dùng biến toàn cục cho dữ liệu.

### 3.2. Bảng phân rã hàm

| Hàm | Tham số | Giá trị trả về | Vai trò |
|---|---|---|---|
| `format_money(amount)` | int / float | `str` có dấu phẩy | Helper định dạng tiền |
| `input_required_text(prompt, field_name)` | str, str | `str` không rỗng | Helper nhập chữ, lặp đến khi hợp lệ |
| `input_amount(prompt)` | str | int / float > 0 | Helper nhập tiền, **try-except** `ValueError`, lặp đến khi hợp lệ (ERR-02) |
| `find_order(orders_list, order_id)` | list, str | `dict` hoặc `None` | Helper tìm kiếm, dùng chung cho chức năng 2 và 3 |
| `display_menu()` | không | `None` | In menu |
| `show_orders(orders_list)` | list | `None` | Chức năng 1 - hiển thị |
| `create_order(orders_list)` | list | `bool` | Chức năng 2 - thêm mới |
| `update_payment_status(orders_list)` | list | `bool` | Chức năng 3 - cập nhật |
| `calculate_financials(orders_list)` | list | `tuple` 3 giá trị | Chức năng 4 - **chỉ tính toán, không in** |
| `print_financial_report(orders_list)` | list | `None` | Gọi hàm tính toán, nhận Tuple và in báo cáo |
| `main()` | không | `None` | Vòng lặp `while True`, try-except menu, điều phối |

### 3.3. Luồng chương trình (Pseudocode)

```
main():
    orders ← dữ liệu mẫu
    LẶP MÃI:
        display_menu()
        THỬ: choice ← int(input(...))
        BẮT ValueError: in ERR-05; quay lại đầu vòng lặp
        1 → show_orders(orders)
        2 → create_order(orders)
        3 → update_payment_status(orders)
        4 → print_financial_report(orders)
        5 → in lời chào; THOÁT
        khác → in ERR-05

create_order(list):
    mã ← input_required_text(...) → bỏ khoảng trắng, viết hoa
    NẾU find_order(list, mã) ≠ None: in ERR-01; TRẢ VỀ False
    tên ← input_required_text(...)
    tiền ← input_amount(...)            # try-except + lặp đến khi > 0 (ERR-02)
    list.append({id, agent_name, total_amount, status: "Unpaid"}); TRẢ VỀ True

update_payment_status(list):
    NẾU list rỗng: thông báo; TRẢ VỀ False
    đơn ← find_order(list, mã)
    đơn là None → ERR-03; đơn["status"] == "Paid" → ERR-04
    ngược lại: đơn["status"] ← "Paid"; in [Thành công]

calculate_financials(list):
    tổng ← tổng total_amount của các đơn có status == "Paid"
    phần_trăm ← 5 NẾU tổng ≥ 100,000,000 NGƯỢC LẠI 0
    TRẢ VỀ (tổng, phần_trăm, tổng × phần_trăm / 100)
```

### 3.4. Các điểm kỹ thuật chính

- **Hàm tính toán trả về Tuple:** `calculate_financials` không `print` gì, chỉ `return (total_revenue, discount_percent, discount_amount)`. Hàm `print_financial_report` nhận Tuple bằng unpacking `total, percent, amount = calculate_financials(orders)` rồi in. Tách tính toán khỏi hiển thị giúp hàm dễ kiểm thử (ví dụ ở mục 5) và dùng lại được cho báo cáo khác.
- **try-except:** dùng ở menu (`int(input())`) và ô nhập tiền (`float(text)`). Nhập chữ sẽ gây `ValueError` và được bắt lại để in mã lỗi, chương trình không crash.
- **Ràng buộc số tiền:** `0 < amount < inf` chặn cả số âm, 0 và các giá trị đặc biệt như `nan`, `inf` mà `float()` vẫn chấp nhận.
- **Kiểm soát ranh giới:** chức năng 1, 3, 4 kiểm tra danh sách rỗng trước khi duyệt hoặc cập nhật.
- **Căn lề bảng:** cột chữ căn trái (`:<8`, `:<22`), cột tiền căn phải (`:>15`) với dấu phẩy ngăn cách hàng nghìn.

## 4. Mã nguồn

File: [`agent_order.py`](agent_order.py)

```python
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
```

## 5. Kết quả chạy thử

Kịch bản chạy toàn bộ chức năng và mọi mã lỗi *(ẩn khung menu lặp lại)*:

```
Mời chọn chức năng (1-5): abc
[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5! (ERR-05)

Mời chọn chức năng (1-5): 9
[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5! (ERR-05)

Mời chọn chức năng (1-5): 0
[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5! (ERR-05)

Mời chọn chức năng (1-5): 1
── DANH SÁCH ĐƠN HÀNG ĐẠI LÝ ──
MÃ ĐƠN  | TÊN ĐẠI LÝ            |   GIÁ TRỊ (VND) | TRẠNG THÁI
──────────────────────────────────────────────────────────────────
HD01    | Dai ly Hoang Long     |      45,000,000 | Paid
HD02    | Tap hoa Minh Thu      |      15,000,000 | Unpaid
──────────────────────────────────────────────────────────────────

Mời chọn chức năng (1-5): 4
── BÁO CÁO TÀI CHÍNH DOANH NGHIỆP ──
+ Tổng doanh thu thực tế (Đã thanh toán): 45,000,000 VND
+ Tỷ lệ chiết khấu áp dụng: 0%
+ Số tiền chiết khấu đại lý nhận lại: 0 VND

Mời chọn chức năng (1-5): 2
── TẠO MỚI ĐƠN HÀNG ──
Nhập mã đơn hàng: HD03
Nhập tên đại lý: Sieu thi MiniMart
Nhập giá trị đơn hàng (VND): 25000000
[Thành công]: Đơn hàng HD03 đã được tạo thành công!

Mời chọn chức năng (1-5): 2
── TẠO MỚI ĐƠN HÀNG ──
Nhập mã đơn hàng: HD01
[Lỗi]: Mã đơn hàng này đã tồn tại trong hệ thống! (ERR-01)

Mời chọn chức năng (1-5): 2
── TẠO MỚI ĐƠN HÀNG ──
Nhập mã đơn hàng:   
[Lỗi]: Mã đơn hàng không được để trống!
Nhập mã đơn hàng: hd04
Nhập tên đại lý:    
[Lỗi]: Tên đại lý không được để trống!
Nhập tên đại lý: Cua hang Ba Nam
Nhập giá trị đơn hàng (VND): -5
[Lỗi]: Giá trị đơn hàng phải là số tiền lớn hơn 0! (ERR-02)
Nhập giá trị đơn hàng (VND): 0
[Lỗi]: Giá trị đơn hàng phải là số tiền lớn hơn 0! (ERR-02)
Nhập giá trị đơn hàng (VND): abc
[Lỗi]: Giá trị đơn hàng phải là số tiền lớn hơn 0! (ERR-02)
Nhập giá trị đơn hàng (VND): 35000000
[Thành công]: Đơn hàng HD04 đã được tạo thành công!

Mời chọn chức năng (1-5): 3
── CẬP NHẬT TRẠNG THÁI THANH TOÁN ──
Nhập mã đơn hàng cần cập nhật: HD02
Tìm thấy đơn hàng của: Tap hoa Minh Thu (Giá trị: 15,000,000)
[Thành công]: Đơn hàng HD02 đã được cập nhật trạng thái ĐÃ THANH TOÁN!

Mời chọn chức năng (1-5): 3
── CẬP NHẬT TRẠNG THÁI THANH TOÁN ──
Nhập mã đơn hàng cần cập nhật: HD01
[Lỗi]: Đơn hàng này đã được thanh toán trước đó! (ERR-04)

Mời chọn chức năng (1-5): 3
── CẬP NHẬT TRẠNG THÁI THANH TOÁN ──
Nhập mã đơn hàng cần cập nhật: HD99
[Lỗi]: Không tìm thấy đơn hàng nào có mã [HD99]! (ERR-03)

Mời chọn chức năng (1-5): 4
── BÁO CÁO TÀI CHÍNH DOANH NGHIỆP ──
+ Tổng doanh thu thực tế (Đã thanh toán): 60,000,000 VND
+ Tỷ lệ chiết khấu áp dụng: 0%
+ Số tiền chiết khấu đại lý nhận lại: 0 VND

Mời chọn chức năng (1-5): 3
── CẬP NHẬT TRẠNG THÁI THANH TOÁN ──
Nhập mã đơn hàng cần cập nhật: hd03
Tìm thấy đơn hàng của: Sieu thi MiniMart (Giá trị: 25,000,000)
[Thành công]: Đơn hàng HD03 đã được cập nhật trạng thái ĐÃ THANH TOÁN!

Mời chọn chức năng (1-5): 3
── CẬP NHẬT TRẠNG THÁI THANH TOÁN ──
Nhập mã đơn hàng cần cập nhật: HD04
Tìm thấy đơn hàng của: Cua hang Ba Nam (Giá trị: 35,000,000)
[Thành công]: Đơn hàng HD04 đã được cập nhật trạng thái ĐÃ THANH TOÁN!

Mời chọn chức năng (1-5): 1
── DANH SÁCH ĐƠN HÀNG ĐẠI LÝ ──
MÃ ĐƠN  | TÊN ĐẠI LÝ            |   GIÁ TRỊ (VND) | TRẠNG THÁI
──────────────────────────────────────────────────────────────────
HD01    | Dai ly Hoang Long     |      45,000,000 | Paid
HD02    | Tap hoa Minh Thu      |      15,000,000 | Paid
HD03    | Sieu thi MiniMart     |      25,000,000 | Paid
HD04    | Cua hang Ba Nam       |      35,000,000 | Paid
──────────────────────────────────────────────────────────────────

Mời chọn chức năng (1-5): 4
── BÁO CÁO TÀI CHÍNH DOANH NGHIỆP ──
+ Tổng doanh thu thực tế (Đã thanh toán): 120,000,000 VND
+ Tỷ lệ chiết khấu áp dụng: 5%
+ Số tiền chiết khấu đại lý nhận lại: 6,000,000 VND

Mời chọn chức năng (1-5): 5
Cảm ơn bạn đã sử dụng phần mềm!
[Chương trình kết thúc]
```

Kiểm thử riêng: danh sách rỗng và giá trị Tuple trả về của `calculate_financials`:

```python
show_orders([]); print_financial_report([])
calculate_financials([... 120,000,000 Paid])                     # (120000000, 5, 6000000)
calculate_financials([... 60,000,000 Paid, 90,000,000 Unpaid])   # (60000000, 0, 0): đơn Unpaid không tính
calculate_financials([... 100,000,000 Paid])                     # (100000000, 5, 5000000): đúng mốc vẫn được 5%
```

```
Hệ thống hiện chưa có đơn hàng nào!
── BÁO CÁO TÀI CHÍNH DOANH NGHIỆP ──
Hệ thống hiện chưa có đơn hàng nào!
(120000000, 5, 6000000)
(60000000, 0, 0)
(100000000, 5, 5000000)
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả mong đợi | Kết quả |
|---|---|---|---|
| Menu nhập chữ / ngoài dải | `abc`, `9`, `0` | ERR-05, quay lại menu | Đạt |
| Xem danh sách mẫu | Chọn 1 | Bảng 2 đơn căn lề thẳng hàng | Đạt |
| Danh sách trống | `show_orders([])` | Hệ thống hiện chưa có đơn hàng nào! | Đạt |
| Tạo đơn hợp lệ | HD03, Sieu thi MiniMart, 25000000 | [Thành công]: Đơn hàng HD03 đã được tạo thành công! | Đạt |
| Trùng mã | HD01 | ERR-01, hủy thao tác | Đạt |
| Mã / tên rỗng | khoảng trắng | Báo lỗi, nhập lại | Đạt |
| Giá trị sai | `-5`, `0`, `abc` | ERR-02, nhập lại đến khi hợp lệ | Đạt |
| Mã chữ thường | `hd04` | Lưu thành HD04 | Đạt |
| Cập nhật thành công | HD02 | Chuyển Paid, [Thành công] | Đạt |
| Đã thanh toán | HD01 | ERR-04, giữ nguyên | Đạt |
| Không tìm thấy | HD99 | ERR-03 | Đạt |
| Báo cáo dưới mốc | 60,000,000 | Chiết khấu 0%, 0 VND | Đạt |
| Báo cáo đạt mốc | 120,000,000 | Chiết khấu 5%, 6,000,000 VND | Đạt |
| Đúng mốc 100,000,000 | gọi hàm | 5%, 5,000,000 | Đạt |
| Thoát | 5 | Lời chào + [Chương trình kết thúc] | Đạt |

## 6. Ghi chú

- Tên hàm và tên trường dữ liệu theo **tài liệu SRS** (`show_orders`, `create_order`, `update_payment_status`, `calculate_financials`; `agent_name`, `total_amount`). Ví dụ khởi tạo trong đề dùng `name`, `price`; SRS (mục 4 - Data model) là đặc tả chính thức nên được ưu tiên.
- Số tiền được hiển thị có dấu phẩy ngăn cách hàng nghìn ở mọi nơi (bảng, cập nhật, báo cáo) theo yêu cầu "định dạng tiền tệ rõ ràng, dễ nhìn" của SRS 7.2.
- Thông báo lỗi in kèm mã lỗi trong ngoặc, ví dụ `(ERR-01)`, đúng như output mẫu của đề.

## 7. Cách chạy

Yêu cầu Python 3.x:

```bash
python agent_order.py
```

## Báo cáo

- [Báo cáo dạng Word (DOCX)](bao-cao-mini-project-quan-ly-don-hang-dai-ly.docx)
