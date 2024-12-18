document.getElementById('add-airplane-form').addEventListener('submit', function(event) {
    event.preventDefault();
    let name = document.getElementById("name").value
    let manufacturerId = document.getElementById("manufacturer").value;
    let mfgDate = document.getElementById("mfg_date").value;
    let seatQuantities = document.getElementsByClassName("seat_quantity");
    let seatTotal = 0;
    let i = 1;
    let seatInputs = {};
    for (let seatQuantity of seatQuantities) {
        let seatValue = parseInt(seatQuantity.value) || 0;
        seatTotal = seatTotal + seatValue
        seatInputs[`${i}`] = seatValue
        i++;
    }

    fetch('/admin/add_airplane/', {
        method: 'POST',
        body: JSON.stringify({
            "name": name,
            "manufacturer_id": manufacturerId,
            "mfg_date": mfgDate,
            "seat_quantity": seatTotal,
            "seat_inputs": seatInputs
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





