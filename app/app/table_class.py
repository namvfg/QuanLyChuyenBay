from app.create_table_fpdf2 import TicketPDF
# ticket_data = {
#     "flight": "VN123",
#     "passenger": "Nguyen Van A",
#     "id_card": "0123456789",
#     "phone": "0987654321",
#     "ticket_class": "Hang thương gia",
#     "price": "5,000,000 VND"
# }

def export_ticket(ticket_data, pdf_path):
    # Tạo PDF
    pdf = TicketPDF()
    font_path = "fonts/DejaVuSerif.ttf"  # Thay đường dẫn này thành nơi lưu font trên hệ thống của bạn
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    pdf.add_font("DejaVu", "I", font_path, uni=True)
    pdf.add_page()
    pdf.add_ticket_details(ticket_data)

    # Lưu PDF
    pdf.output(pdf_path)

    # Mở file PDF sau khi lưu (Windows)
    import os
    # Đường dẫn thư mục dự án
    project_dir = os.getcwd()

    os.startfile(os.path.join(project_dir, pdf_path))
