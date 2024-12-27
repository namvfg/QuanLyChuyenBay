function pay() {
    if (confirm("Bạn chắc chắn muốn thanh toán không?") == true) {
        fetch("/pay", {
        method: "post"
        }).then(res => res.json()).then(data => {
            if (data.status === "success") {
                toastr.success("Chuyển trang trong 3s");
                setTimeout(() => {
                     window.location.href = data.redirect;
                }, 3000);
            } else {
                    // Hiển thị thông báo lỗi
                    toastr.error(data.message);
            }
        }).catch(error => {
                toastr.error("Có lỗi xảy ra. Vui lòng thử lại.");
            });
    }
}

function pay_staff(event) {
    event.preventDefault();
    if (confirm("Bạn chắc chắn muốn thanh toán không?") == true) {
        fetch("/staff/pay", {
        method: "post",
        body: JSON.stringify({
            "payment_method": document.getElementById("payment_method").value
        }),
        headers: {
            "Content-Type": "application/json"
        }
        }).then(res => res.json()).then(data => {
            if (data.status === "success") {
                toastr.success("Chuyển trang trong 3s");
                setTimeout(() => {
                     window.location.href = data.redirect;
                }, 3000);
            } else {
                    // Hiển thị thông báo lỗi
                    toastr.error(data.message);
            }
        }).catch(error => {
                toastr.error("Có lỗi xảy ra. Vui lòng thử lại.");
            });
    }
}