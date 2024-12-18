function submitSchedulingForm1(event) {
      event.preventDefault();
      let name = document.getElementById("flight_name").value;
      let airplaneId = document.getElementById("airplane_id").value;
      let route = JSON.parse(document.getElementById("route").value);
      let flightDate = document.getElementById("flight_date").value;
      routeId = route.route_id
      departureAirportId = route.departure_airport_id
      arrivalAirportId = route.arrival_airport_id

       fetch("/staff/scheduling1", {
            method: "POST",
            body: JSON.stringify({
                "name": name,
                "airplane_id": airplaneId,
                "route_id": routeId,
                "departure_airport_id": departureAirportId,
                "arrival_airport_id": arrivalAirportId,
                "flight_date": flightDate
            }),
            headers: {
                "Content-Type": "application/json"
            }
       })
       .then(respond => respond.json())
       .then(data => {
                if (data.status === "success") {
                    // Hiển thị thông báo thành công
                    toastr.success("Nhập thành công!");
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

};

function submitSchedulingForm2(event) {
      event.preventDefault();
      let seatClassPriceInputs = document.getElementsByClassName("seat_class_price");
      let i = 1;
      let seatClassPrices = {};
      for (let seatClassPriceInput of seatClassPriceInputs) {
        let seatClassPrice = parseInt(seatClassPriceInput.value);
        seatClassPrices[`${i}`] = seatClassPrice
        i++;
      }



      let waitingDurationInputs = document.getElementsByClassName("waiting_duration");
      let flyingDurationInputs = document.getElementsByClassName("flying_duration");
      let j = 1;
      let k = 1;
      let waitingDurations = {};
      let flyingDurations = {};
      for (let waitingDurationInput of waitingDurationInputs) {
        let waitingDuration = parseInt(waitingDurationInput.value);
        waitingDurations[`${j}`] = waitingDuration
        j++;
      }
       for (let flyingDurationInput of flyingDurationInputs) {
        let flyingDuration = parseInt(flyingDurationInput.value);
        flyingDurations[`${k}`] = flyingDuration
        k++;
      }
       console.log(seatClassPrices, waitingDurations, flyingDurations)


       fetch("/staff/scheduling2", {
            method: "POST",
            body: JSON.stringify({
                "ticket_prices": seatClassPrices,
                "waiting_durations": waitingDurations,
                "flying_duration": flyingDurations
            }),
            headers: {
                "Content-Type": "application/json"
            }
       })
       .then(respond => respond.json())
       .then(data => {
                if (data.status === "success") {
                    // Hiển thị thông báo thành công
                    toastr.success("Nhập thành công!");
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

};