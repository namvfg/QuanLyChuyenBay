from fpdf import FPDF

class TicketPDF(FPDF):
    def header(self):
        # Tiêu đề
        self.set_font("DejaVu", style="B", size=12)
        self.cell(0, 10, "VÉ CHUYẾN BAY", align="C", ln=True)
        self.ln(5)  # Dòng trống sau tiêu đề

    def add_ticket_details(self, data):
        # Chiều rộng của các cột
        col_width = 95  # Mỗi cột có độ rộng bằng nửa trang
        row_height = 8  # Chiều cao mỗi hàng

        # Font chữ
        self.set_font("DejaVu", size=12)

        # Dòng 1
        self.cell(col_width, row_height, f"Chuyến bay: {data.get('flight', '............................')}", border=1)
        self.cell(col_width, row_height, f"Hành khách: {data.get('passenger', '........................')}", border=1, ln=True)

        # Dòng 2
        self.cell(col_width, row_height, f"CMND/CCCD: {data.get('id_card_number', '........................')}", border=1)
        self.cell(col_width, row_height, f"Điện thoại: {data.get('phone_number', '..........................')}", border=1, ln=True)

        # Dòng 3
        self.cell(col_width, row_height, f"Hạng ghế: {data.get('seat_class', '.........................')}", border=1)
        self.cell(col_width, row_height, f"Giá tiền: {data.get('ticket_price', '..............................')} VNĐ", border=1, ln=True)
