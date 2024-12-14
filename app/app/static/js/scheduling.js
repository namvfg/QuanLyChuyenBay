document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.getElementById("add-intermediate-airport");
    const container = document.getElementById("intermediate-airports-container");

    const maxAirports = 2; // Số lượng sân bay trung gian tối đa

    // Hàm tạo combobox sân bay
    function createAirportSelect(index) {
        const div = document.createElement("div");
        div.classList.add("d-flex", "align-items-center", "mb-2");
        div.id = `airport-${index}`;

        const select = document.createElement("select");
        select.classList.add("form-select", "border", "border-dark", "me-2");
        select.name = `intermediate-airport-${index}`;
        select.innerHTML = `
            <option value="" selected>Chọn sân bay trung gian</option>
            {% for airport in airport_info %}
            <option value="{{ airport['id'] }}">{{ airport['name'] }}</option>
            {% endfor %}
        `;

        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.classList.add("btn", "btn-danger");
        removeButton.textContent = "Xóa";

        // Sự kiện xóa sân bay
        removeButton.addEventListener("click", function () {
            div.remove();
            checkDuplicateSelection(); // Kiểm tra lại sau khi xóa
            if (container.children.length < maxAirports) {
                addButton.disabled = false; // Cho phép thêm sân bay nếu chưa đủ
            }
        });

        select.addEventListener("change", checkDuplicateSelection);

        div.appendChild(select);
        div.appendChild(removeButton);

        return div;
    }

    // Hàm kiểm tra giá trị trùng lặp
    function checkDuplicateSelection() {
        const selects = container.querySelectorAll("select");
        const values = Array.from(selects).map(select => select.value);
        const duplicates = values.filter((value, index, self) => value && self.indexOf(value) !== index);

        selects.forEach(select => {
            if (duplicates.includes(select.value)) {
                select.classList.add("is-invalid");
            } else {
                select.classList.remove("is-invalid");
            }
        });
    }

    // Sự kiện thêm sân bay trung gian
    addButton.addEventListener("click", function () {
        const currentCount = container.children.length;

        if (currentCount < maxAirports) {
            const newAirport = createAirportSelect(currentCount + 1);
            container.appendChild(newAirport);
            checkDuplicateSelection();
        }

        if (container.children.length >= maxAirports) {
            addButton.disabled = true; // Vô hiệu hóa nút nếu đủ số lượng
        }
    });
});
