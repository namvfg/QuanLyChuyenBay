function submitPassengerInformationForm(event) {
        event.preventDefault();
        let mapData = new Map();
        passengerInfos = document.getElementsByClassName("passenger");
        for (let i = 0; i < passengerInfos.length; i++) {
            lastName = passengerInfos[i].querySelector(`#last_name_${i}`).value;
            firstName = passengerInfos[i].querySelector(`#first_name_${i}`).value;
            idCardNumber = passengerInfos[i].querySelector(`#id_card_number_${i}`).value;
            phoneNumber = passengerInfos[i].querySelector(`#phone_number_${i}`).value;
            let subData = {
                "last_name": lastName,
                "first_name": firstName,
                "id_card_number": idCardNumber,
                "phone_number": phoneNumber
            }
            mapData.set(i.toString(), subData)

        }

        let objData = Object.fromEntries(
            Array.from(mapData)
        );


       fetch("/passenger_information", {
            method: "POST",
            body: JSON.stringify(objData),
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

function submitPassengerInformationFormStaff(event) {
        event.preventDefault();
        let mapData = new Map();
        passengerInfos = document.getElementsByClassName("passenger");
        for (let i = 0; i < passengerInfos.length; i++) {
            lastName = passengerInfos[i].querySelector(`#last_name_${i}`).value;
            firstName = passengerInfos[i].querySelector(`#first_name_${i}`).value;
            idCardNumber = passengerInfos[i].querySelector(`#id_card_number_${i}`).value;
            phoneNumber = passengerInfos[i].querySelector(`#phone_number_${i}`).value;
            let subData = {
                "last_name": lastName,
                "first_name": firstName,
                "id_card_number": idCardNumber,
                "phone_number": phoneNumber
            }
            mapData.set(i.toString(), subData)

        }

        let objData = Object.fromEntries(
            Array.from(mapData)
        );


       fetch("/staff/passenger_information", {
            method: "POST",
            body: JSON.stringify(objData),
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