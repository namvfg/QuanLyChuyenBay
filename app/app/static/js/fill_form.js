function fillForm(departureAirportAddress, arrivalAirportAddress) {
    document.getElementById('start_point').value = departureAirportAddress;
    document.getElementById('end_point').value = arrivalAirportAddress;
    window.scrollTo({ top: 0, behavior: 'smooth' });
    toastr.success("Đã điền vào form");
}

