 document.getElementById('login-form').addEventListener('submit', function(event) {
            event.preventDefault();  // Ngừng reload trang khi submit form

            // Tạo FormData từ form
            let formData = new FormData(this);
            let params = new URLSearchParams(window.location.search);
            let next = params.get('next') || '/';
            formData.append('next', next);
            // Gửi yêu cầu POST bằng fetch
            fetch('/login', {
                method: 'POST',
                body: formData // Dữ liệu được gửi dưới dạng FormData
            })
            .then(response => response.json())  // Parse JSON response
            .then(data => {
                if (data.status === "success") {
                    // Hiển thị thông báo thành công
                    toastr.success("Đăng nhập thành công!");
                    // Chuyển hướng trang
                    window.location.href = data.redirect;
                } else {
                    // Hiển thị thông báo lỗi
                    toastr.error(data.message);
                }
            })
            .catch(error => {
                toastr.error("Có lỗi xảy ra. Vui lòng thử lại.");
            });
        });