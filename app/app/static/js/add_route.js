document.getElementById("add-route-form").addEventListener('submit', function(event) {
    event.preventDefault();
    let airportValues = document.getElementsByClassName("airport_value");
    let mySet = new Set();
    let sendRequest = true;
    let i = 0;
    let result = new Array();
    for (let airportValue of airportValues) {
        let value = parseInt(airportValue.value)
        if (i <= 1) {
            if (!value) {
                sendRequest = false;
                toastr.error("Sân bay đi và sân bay đến không được trống");
                break;
            }
        }
        else {
            if (!value) {
                break;
            }
        }
        if (mySet.has(value)) {
            sendRequest = false;
            toastr.error("Các sân bay không được trùng nhau");
            break;
        }
        else {
            mySet.add(value)
            result.push(value)
        }
        i++;
    }
    if (sendRequest == true) {
        let intermediateAirports = {}
        for (let i = 2; i < result.length; i++) {
             intermediateAirports[`${i - 1}`] = result[i]
        }
        let name = document.getElementById("name").value
        fetch('/admin/add_route/', {
        method: 'POST',
        body: JSON.stringify({
            "name": name,
            "departure_airport_id": result[0],
            "arrival_airport_id": result[1],
            "intermediate_airport_quantity": result.length - 2,
            "intermediate_airports": intermediateAirports
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
            setTimeout(() => {
                window.location.reload();
            }, 3000);
        } else {
            // Hiển thị thông báo lỗi
            toastr.error(data.message);
        }
    })
    .catch(error => {
        toastr.error("Có lỗi xảy ra. Vui lòng thử lại.");
    });
    }
});