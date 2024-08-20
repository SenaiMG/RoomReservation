document.addEventListener("DOMContentLoaded", function() {
    "use strict";

    var date = new Date();
    var today = date.getDate();

    document.getElementById("prev").addEventListener("click", function() {
        prev_year({ date: date });
    });
    document.getElementById("next").addEventListener("click", function() {
        next_year({ date: date });
    });

    var months = document.getElementsByClassName("month");
    for (var i = 0; i < months.length; i++) {
        months[i].addEventListener("click", function() {
            month_click({ date: date, monthElement: this });
        });
    }

    var activeMonth = document.getElementsByClassName("months-row")[0].children[date.getMonth()];
    activeMonth.classList.add("active-month");

    init_calendar(date);
});

function init_calendar(date) {
    var tbody = document.getElementsByClassName("tbody")[0];
    var eventsContainer = document.getElementsByClassName("events-container")[0];
    tbody.innerHTML = "";
    eventsContainer.innerHTML = "";

    var calendar_days = tbody;
    var month = date.getMonth();
    var year = date.getFullYear();
    var day_count = days_in_month(month, year);
    var row = document.createElement("tr");
    row.className = "table-row";
    var today = date.getDate();

    date.setDate(1);
    var first_day = date.getDay();

    for (var i = 0; i < 35 + first_day; i++) {
        var day = i - first_day + 1;
        if (i % 7 === 0) {
            calendar_days.appendChild(row);
            row = document.createElement("tr");
            row.className = "table-row";
        }
        var curr_date;
        if (i < first_day || day > day_count) {
            curr_date = document.createElement("td");
            curr_date.className = "table-date nil";
        } else {
            curr_date = document.createElement("td");
            curr_date.className = "table-date";
            curr_date.textContent = day;
            curr_date.addEventListener("click", function() {
                date_click(new Date(year, month, this.textContent), this);
            });
        }
        row.appendChild(curr_date);
    }
    calendar_days.appendChild(row);
    document.getElementsByClassName("year")[0].textContent = year;
}

function days_in_month(month, year) {
    return new Date(year, month + 1, 0).getDate();
}

async function date_click(date, element) {
    var activeDate = document.getElementsByClassName("active-date")[0];
    var selectElement = document.getElementById('list_room');
    var room = selectElement.value;
    if (activeDate) {
        activeDate.classList.remove("active-date");
    }
    element.classList.add("active-date");
    
    // Chamar a API para obter os dados das horas disponíveis
    try {
        const baseURL = window.location.origin;
        const response = await fetch(`${baseURL}/api/check-availability/${room}/${date.toISOString().split('T')[0]}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }

        const data = await response.json();
        
        var date_input = document.getElementById('date');
        date_input.value = date.toLocaleDateString();
        // Exibir os dados na dialog com checklist
        if (data.available_hours.length > 0) {
            show_event_form({
                "occasion": "Horas disponíveis em " + date.toLocaleDateString(),
                "details": data.available_hours.map(hour => hour.range_hour) // Passa como array de strings
            });
        } else {
            show_event_form({
                "occasion": "Nenhuma hora disponível em " + date.toLocaleDateString(),
                "details": []
            });
        }

    } catch (error) {
        console.error('Erro ao chamar a API:', error);
        show_event_form({
            "occasion": "Erro ao obter dados",
            "details": []
        });
    }
}

function month_click(event) {
    var eventsContainer = document.getElementsByClassName("events-container")[0];
    eventsContainer.style.display = "block";
    document.getElementById("dialog").style.display = "none";

    var date = event.date;
    var activeMonth = document.getElementsByClassName("active-month")[0];
    if (activeMonth) {
        activeMonth.classList.remove("active-month");
    }
    event.monthElement.classList.add("active-month");

    var new_month = Array.prototype.indexOf.call(event.monthElement.parentNode.children, event.monthElement);
    date.setMonth(new_month);
    init_calendar(date);
}

function next_year(event) {
    var date = event.date;
    var new_year = date.getFullYear() + 1;
    document.getElementsByClassName("year")[0].textContent = new_year;
    date.setFullYear(new_year);
    init_calendar(date);
}

function prev_year(event) {
    var date = event.date;
    var new_year = date.getFullYear() - 1;
    document.getElementsByClassName("year")[0].textContent = new_year;
    date.setFullYear(new_year);
    init_calendar(date);
}

function show_event_form(data) {
    var dialog = document.getElementById("dialog");
    dialog.style.display = "block";

    document.getElementById("name").value = data.occasion;

    // Limpar o conteúdo anterior
    var checklistContainer = document.getElementById("checklist-container");
    checklistContainer.innerHTML = "";  // Limpar o conteúdo anterior

    // Se houver detalhes (ou seja, horas disponíveis), criar checkboxes e dividir em duas colunas
    if (data.details && Array.isArray(data.details)) {
        var row = document.createElement("div");
        row.className = "row";

        var col1 = document.createElement("div");
        col1.className = "col-6";

        var col2 = document.createElement("div");
        col2.className = "col-6";

        data.details.forEach(function(item, index) {
            var checkboxItem = document.createElement("div");
            checkboxItem.className = "form-check";

            var checkbox = document.createElement("input");
            checkbox.className = "form-check-input";
            checkbox.type = "checkbox";
            checkbox.name = "hours";
            checkbox.id = "hour" + index;
            checkbox.value = item;

            var label = document.createElement("label");
            label.className = "form-check-label";
            label.htmlFor = "hour" + index;
            label.textContent = item;

            checkboxItem.appendChild(checkbox);
            checkboxItem.appendChild(label);

            // Alternar entre as colunas
            if (index % 2 === 0) {
                col1.appendChild(checkboxItem);
            } else {
                col2.appendChild(checkboxItem);
            }
        });

        row.appendChild(col1);
        row.appendChild(col2);
        checklistContainer.appendChild(row);
    }

    document.getElementById("cancel-button").onclick = function() {
        document.getElementById("name").classList.remove("error-input");
        dialog.style.display = "none";
    };

    document.getElementById("ok-button").onclick = function() {
        dialog.style.display = "none";
        alert("Solicitação enviada!");  // Apenas para simular o salvamento
    };
}

const months = [
    "January", 
    "February", 
    "March", 
    "April", 
    "May", 
    "June", 
    "July", 
    "August", 
    "September", 
    "October", 
    "November", 
    "December"
];

function mostardiv() {
    var div = document.getElementById("calen");
    div.style.visibility = "visible";
    
    var selectElement = document.getElementById('list_room');
    var selectedValue = selectElement.value;

    var hiddenField = document.getElementById('room');
    hiddenField.value = selectedValue;
}

function mostardivprof() {
    var div = document.getElementById("prof");
    div.style.visibility = "visible";
    var selectProf = document.getElementById('list_teacher');
    var ProfValue = selectProf.value;
    var hiddenProf = document.getElementById('teacher');
    hiddenProf.value = ProfValue;
}

document.getElementById('list_teacher').addEventListener('change', mostardivprof);
document.getElementById('list_room').addEventListener('change', mostardiv);