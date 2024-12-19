// Lấy form theo id
document.getElementById('passwordForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Ngừng reload trang khi submit form

    // Lấy dữ liệu từ form
    const formData = new FormData(this);

    // Kiểm tra xác nhận mật khẩu
    const newPassword = formData.get('newPassword');
    const confirmPassword = formData.get('confirmPassword');
    if (newPassword !== confirmPassword) {
        toastr.error("Mật khẩu xác nhận không khớp. Vui lòng thử lại.");
        return; // Ngừng thực thi nếu không khớp
    }

    // Gửi yêu cầu POST bằng fetch
    fetch('/info_page', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json()) // Parse JSON response
        .then(data => {
            if (data.status === "success") {
                // Hiển thị thông báo thành công
                toastr.success(data.message);

                // Đóng modal sau khi đổi mật khẩu thành công
                const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
                modal.hide();
            } else {
                // Hiển thị thông báo lỗi
                toastr.error(data.message);
            }
        })
        .catch(error => {
            toastr.error("Có lỗi xảy ra. Vui lòng thử lại.");
            console.error("Error:", error);
        });
});
