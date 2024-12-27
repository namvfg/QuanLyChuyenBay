function checkPhoneNumber(obj) {
    fetch("/api/check_phone_number", {
        method: "post",
        body: JSON.stringify({
            "phone_number": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if (data.status == "exist") {
            document.getElementById("last_name").value = data.last_name;
            document.getElementById("first_name").value = data.first_name;
            toastr.success("Đã có tài khoản")
        }
        else if (data.status == "not_exist"){
            toastr.success("Chưa có tài khoản")
            document.getElementById("last_name").value = "";
            document.getElementById("first_name").value = "";
        }
        else {
            toastr.error(data.message)
            document.getElementById("last_name").value = "";
            document.getElementById("first_name").value = "";
        }
    }) //promise
}

function submitCustomerInformationForm(event) {
        event.preventDefault();

        lastName = document.getElementById("last_name").value;
        firstName = document.getElementById("first_name").value;
        phoneNumber = document.getElementById("phone_number").value;
       fetch("/staff/customer_information", {
            method: "post",
            body: JSON.stringify({
                "phone_number": phoneNumber,
                "last_name": lastName,
                "first_name": firstName
            }),
            headers: {
                "Content-Type": "application/json"
            }
       })
       .then(respond => respond.json())
       .then(data => {
                if (data.status === "success") {
                    toastr.success("Nhập thành công!");
                    window.location.href = data.redirect;
                } else {
                    toastr.error(data.message);
                }
            })
            .catch(error => {
                toastr.error("Có lỗi xảy ra. Vui lòng thử lại.");
            });

};
