function toggleSeat(seatId, seatName, ticketPrice, ticketPriceId, active) {
    if (active == false) {
        fetch("/api/add_seat", {
        method: "post",
        body: JSON.stringify({
            "seat_id": seatId,
            "seat_name": seatName
            "ticket_price": ticketPrice,
            "ticket_price_id": ticketPriceId
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        document.getElementById("total-seats").value = data.total_quantity
        document.getElementById("amount-seats").value = data.total_amount
    }) //promise
    }
    else {

    }

}