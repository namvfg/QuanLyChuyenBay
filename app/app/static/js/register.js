 document.getElementById('register-form').addEventListener('submit', function(event) {
            event.preventDefault();  // Ngừng reload trang khi submit form

            // Tạo FormData từ form
            const formData = new FormData(this);
            // Gửi yêu cầu POST bằng fetch
            fetch('/register', {
                method: 'POST',
                body: formData // Dữ liệu được gửi dưới dạng FormData
            })
            .then(response => response.json())  // Parse JSON response
            .then(data => {
                if (data.status === "success") {
                    // Hiển thị thông báo thành công
                    toastr.success("Đăng ký thành công!");
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

document.getElementById('send-verify-code').addEventListener('click', function(event) {
    event.preventDefault();  // Ngừng reload trang khi submit form
    let inputs = document.getElementsByClassName("input-field");
    for (let input of inputs) {
        input.setAttribute("readonly", "true");
    }
    document.getElementById('verify_code').removeAttribute("readonly");

    let emailTarget = document.getElementById("email").value;
    // Gửi yêu cầu POST bằng fetch
    fetch('/api/verify_code', {
        method: 'POST',
        body: JSON.stringify({
            "email_target": emailTarget,
            "verify_code": -1
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        if (data.status === "success") {
            // Hiển thị thông báo thành công
            toastr.success(data.message);
        } else {
            // Hiển thị thông báo lỗi
            toastr.error(data.message);
        }
    })
    .catch(error => {
        toastr.error("Có lỗi xảy ra. Vui lòng thử lại.");
    });
});

document.getElementById('change_info').addEventListener('click', function(event) {
    event.preventDefault();  // Ngừng reload trang khi submit form
    let inputs = document.getElementsByClassName("input-field");
    for (let input of inputs) {
        input.removeAttribute("readonly");
    }
    document.getElementById('verify_code').setAttribute("readonly", "true");

    fetch('/api/clear_verify_code', {
        method: 'POST',
        body: JSON.stringify({
            "email_target": "",
            "verify_code": -1
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        if (data.status === "success") {
            // Hiển thị thông báo thành công
            toastr.success(data.message);
        } else {
            // Hiển thị thông báo lỗi
            toastr.error(data.message);
        }
    })
    .catch(error => {
        toastr.error("Có lỗi xảy ra. Vui lòng thử lại.");
    });
});

