function checkTicketCode(event) {
    event.preventDefault()
    let ticketCode = document.getElementById("ticket_code").value;
    fetch("/staff/export_ticket", {
        method: "post",
        body: JSON.stringify({
            "ticket_code": ticketCode
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
       if (data.status === "success") {
            // Hiển thị thông báo thành công
            toastr.success(data.message);
        } else {
            // Hiển thị thông báo lỗi
            toastr.error(data.message);
        }
    }) //promise
}