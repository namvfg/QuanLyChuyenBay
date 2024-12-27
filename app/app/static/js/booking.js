


function toggleSeat(seatId, seatName, seatClassName,ticketPrice, ticketPriceId, active) {
    if (active == "False") {
        button = document.getElementById(`seat_${seatId}`)
        fetch("/api/cart", {
        method: "post",
        body: JSON.stringify({
            "seat_id": seatId,
            "seat_name": seatName,
            "seat_class_name": seatClassName,
            "ticket_price": ticketPrice,
            "ticket_price_id": ticketPriceId
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if (data.status === "success") {
            document.getElementById("total-seats").value = data.total_quantity
            document.getElementById("amount-seats").value = data.total_amount.toLocaleString("en-US")
            document.getElementById("chosen-seats").value = data.chosen_seats
            array = data.chosen_id_seats
            array.pop()
            let mySet = new Set(array.map(item => item.toString()));
            if (mySet.has(seatId.toString()) == false) {
                document.getElementById("booked-table").innerHTML +=
                `
                    <tr id="seat${seatId}">
                        <td>${seatName}</td>
                        <td>${seatClassName}</td>
                        <td>${ticketPrice.toLocaleString("en-US")}</td>
                        <td><input type="button" class="btn btn-danger" value="Xóa" onclick="deleteCart(${seatId})"></td>
                    </tr>
                `
            }
            button.classList.add("clicked");
        }
        else {
            toastr.error(data.message)
        }
    }) //promise
    }
    else {
        toastr.error("Ghế này đã được đặt rồi")
    }
}

function deleteCart(seatId) {
    if (confirm("Bạn chắc chắn muốn xóa không?") == true) {
        fetch(`/api/cart/${seatId}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            console.info(data);
            document.getElementById("total-seats").value = data.total_quantity;
            document.getElementById("amount-seats").value = data.total_amount.toLocaleString("en-US");
            document.getElementById("chosen-seats").value = data.chosen_seats;

            // Kiểm tra và ẩn phần tử seatId nếu tồn tại
            let seatElement = document.getElementById(`seat${seatId}`);
            if (seatElement) {
                seatElement.remove() // Ẩn phần tử seat
            }

            // Kiểm tra và loại bỏ class 'clicked' khỏi nút nếu tồn tại
            let button = document.getElementById(`seat_${seatId}`);
            if (button) {
                button.classList.remove("clicked");
            }

        }).catch(err => console.info(err)); // Promise
    }
}

seatClassListBox = document.getElementById("myListBox")
seatClassListBox.addEventListener('change', function() {
    const selectedValue = this.value;

    let seats = document.getElementsByClassName(`seat`);
    for (let seat of seats) {
        seat.disabled = true;
        seat.classList.add("opacity-50")
    }

    let seatsInSeatClass = document.getElementsByClassName(`seat_class_${selectedValue}`);
    for (let seat of seatsInSeatClass) {
        seat.disabled = false;
        seat.classList.remove("opacity-50")
    }

});



