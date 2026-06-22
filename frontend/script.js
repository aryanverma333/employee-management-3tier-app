const API_URL = "http://localhost:5050";

async function loadEmployees() {
    try {
        const response = await fetch(`${API_URL}/employees`);
        const employees = await response.json();

        const employeeList = document.getElementById("employeeList");
        employeeList.innerHTML = "";

        employees.forEach(employee => {
            const li = document.createElement("li");

            li.className =
                "list-group-item d-flex justify-content-between align-items-center";

            li.textContent = employee.name;

            employeeList.appendChild(li);
        });

    } catch (error) {
        console.error("Error loading employees:", error);
    }
}

async function addEmployee() {

    const nameInput = document.getElementById("employeeName");
    const name = nameInput.value.trim();

    if (!name) {
        alert("Please enter employee name");
        return;
    }

    try {

        await fetch(`${API_URL}/employee`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name
            })
        });

        nameInput.value = "";

        loadEmployees();

    } catch (error) {
        console.error("Error adding employee:", error);
    }
}

window.onload = loadEmployees;