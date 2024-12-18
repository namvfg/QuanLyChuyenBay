document.addEventListener('DOMContentLoaded', () => {
    const totalSeatsInput = document.getElementById('total-seats');
    const amountSeatsInput = document.getElementById('amount-seats');
    const seatPrice = 1400000; // Giá mỗi ghế
    let selectedSeats = 0; // Tổng số ghế đã chọn

    document.querySelectorAll('.seat-toggle').forEach(button => {
        button.addEventListener('click', () => {
            button.classList.toggle('active'); // Thay đổi trạng thái ghế

            if (button.classList.contains('active')) {
                // Ghế được chọn
                selectedSeats++;
            } else {
                // Bỏ chọn ghế
                selectedSeats--;
            }

            // Cập nhật tổng số ghế và tổng tiền
            totalSeatsInput.value = selectedSeats;
            amountSeatsInput.value = selectedSeats * seatPrice;
        });
    });
});