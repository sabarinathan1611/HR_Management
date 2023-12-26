
let todayAttendanceTable = document.querySelector("table.today-attendance-table")

let tableHead = todayAttendanceTable.querySelector("thead");
let tableBody = todayAttendanceTable.querySelector("tbody");

const employeeData = [
    { empid: "#0001",  date:"13-12-2023",status:"A", empname: "John Doe", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:05 AM", empouttime: "05:10 PM" },
    { empid: "#0002",  date:"13-12-2023",status:"P", empname: "Jane Doe", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:02 AM", empouttime: "04:08 PM" },
    { empid: "#0003",  date:"13-12-2023",status:"A", empname: "Alice Smith", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:07 AM", empouttime: "04:55 PM" },
    { empid: "#0004",  date:"13-12-2023",status:"P", empname: "Bob Johnson", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:01 AM", empouttime: "05:12 PM" },
    { empid: "#0005",  date:"13-12-2023",status:"A", empname: "Eve Williams", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:10 AM", empouttime: "05:20 PM" },
    { empid: "#0006",  date:"13-12-2023",status:"P", empname: "Charlie Brown", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:03 AM", empouttime: "05:11 PM" },
    { empid: "#0007",  date:"13-12-2023",status:"A", empname: "Lucy Miller", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:12 AM", empouttime: "05:18 PM" },
    { empid: "#0008",  date:"13-12-2023",status:"P", empname: "David Davis", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:06 AM", empouttime: "05:14 PM" },
    { empid: "#0009",  date:"13-12-2023",status:"A", empname: "Grace White", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:04 AM", empouttime: "04:19 PM" },
    { empid: "#0010", date:"13-12-2023",status:"P", empname: "Frank Black", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:15 AM", empouttime: "05:25 PM" },
    { empid: "#0011", date:"13-12-2023",status:"A", empname: "Helen Adams", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:09 AM", empouttime: "05:13 PM" },
    { empid: "#0012", date:"13-12-2023",status:"P", empname: "Ivan Foster", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:11 AM", empouttime: "04:37 PM" },
    { empid: "#0013", date:"13-12-2023",status:"A", empname: "Jessica Brown", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:08 AM", empouttime: "05:16 PM" },
    { empid: "#0014", date:"13-12-2023",status:"P", empname: "Kevin Taylor", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:13 AM", empouttime: "05:22 PM" },
    { empid: "#0015", date:"13-12-2023",status:"A", empname: "Laura Evans", shiftintime: "09:00 AM", shiftouttime: "05:00 PM", empintime: "09:14 AM", empouttime: "04:39 PM" },
];

function formatTime(hours, minutes) {
    return `${hours} hrs - ${minutes} mins`;
}

const workingHours = 8; // Assuming the working hours is 8 hours per day

function calculateLateBy(shiftInTime, empInTime) {
    const shiftInDateTime = new Date(`2000-01-01 ${shiftInTime}`);
    const empInDateTime = new Date(`2000-01-01 ${empInTime}`);
    const lateByMinutes = Math.max(0, empInDateTime - shiftInDateTime) / (1000 * 60);
    return lateByMinutes;
}

function calculateEarlyGo(shiftOutTime, empOutTime) {
    const shiftOutDateTime = new Date(`2000-01-01 ${shiftOutTime}`);
    const empOutDateTime = new Date(`2000-01-01 ${empOutTime}`);
    const earlyGoMinutes = Math.max(0, shiftOutDateTime - empOutDateTime) / (1000 * 60);
    return (earlyGoMinutes);
}

function calculateTotalDuration(empInTime, empOutTime) {
    const empInDateTime = new Date(`2000-01-01 ${empInTime}`);
    const empOutDateTime = new Date(`2000-01-01 ${empOutTime}`);

    if (isNaN(empInDateTime) || isNaN(empOutDateTime)) {
        return "Invalid input for total duration";
    }

    const totalDurationMinutes = (empOutDateTime - empInDateTime) / (1000 * 60);
    const totalDurationHours = Math.floor(totalDurationMinutes / 60);
    const remainingMinutes = Math.round(totalDurationMinutes % 60);
    return formatTime(totalDurationHours, remainingMinutes);
}

function calculateExtraTime(totalDuration) {
    let totalDurationMinutes;

    if (typeof totalDuration === 'string') {
        // If totalDuration is already in the "8 hrs - 5 mins" format, extract minutes
        const match = totalDuration.match(/(\d+) hrs - (\d+) mins/);
        if (match) {
            totalDurationMinutes = parseInt(match[1]) * 60 + parseInt(match[2]);
        } else {
            return "Invalid input for extra time";
        }
    } else {
        // If totalDuration is in minutes, use it directly
        totalDurationMinutes = totalDuration;
    }

    // Correct calculation for extra time
    const expectedWorkDuration = workingHours * 60;
    const extraTimeMinutes = totalDurationMinutes - expectedWorkDuration;
    const extraTimeHours = Math.floor(Math.abs(extraTimeMinutes) / 60);
    const remainingMinutes = Math.abs(extraTimeMinutes % 60);
    const sign = extraTimeMinutes >= 0 ? '+' : '-';
    
    return `${sign}${extraTimeHours} hrs - ${remainingMinutes} mins`;
}

// ... [previous code]

// Loop through each employee data
employeeData.forEach(employee => {
    const lateByMinutes = calculateLateBy(employee.shiftintime, employee.empintime);
    const earlyGoMinutes = calculateEarlyGo(employee.shiftouttime, employee.empouttime);
    const totalDuration = calculateTotalDuration(employee.empintime, employee.empouttime);
    const extraTime = calculateExtraTime(totalDuration);

    let status ;

    if (employee.status == "P") {
        status = `<i class="fas fa-check-circle"></i>`;
    }else if (employee.status == "A") {
        status = `<i class="fas fa-times-circle"></i>`;
    }else{
        status = `~`;
    }

    let tr = document.createElement("tr");

    tr.innerHTML = (`
        <td class="id">${employee.empid}</td>
        <td class="name">${employee.empname}</td>
        <td>${employee.date}</td>
        <td>${employee.shiftintime}</td>
        <td>${employee.shiftouttime}</td>
        <td>${employee.empintime}</td>
        <td>${employee.empouttime}</td>
        <td>${formatTime(parseInt(lateByMinutes/60), lateByMinutes % 60)}</td>
        <td>${formatTime(parseInt(earlyGoMinutes/60) , earlyGoMinutes % 60)}</td>
        <td>${totalDuration}</td>
        <td class="extra">${extraTime}</td>
        <td>${status}</td>
    `);

    document.querySelector(".today-attendance-table .tableBody").appendChild(tr);

});


let extraTd = todayAttendanceTable.querySelectorAll(".extra");

extraTd.forEach(extra => {
    if (extra.innerHTML[0] == "-") {
        extra.style.color = "red";
    }else if (extra.innerHTML[0] == "+") {
        extra.style.color = "green";
    } else {
        extra.style.color = "black";
    }
});


const attendance_table = document.querySelector(".attendance-table");

const tablerow = document.querySelectorAll(".filter tr");

const idsearch = document.getElementById("idsearch");

console.log(idsearch);

idsearch.addEventListener("input", () => {
    let input = idsearch.value;

    tablerow.forEach(row => {
        let id = row.querySelector(".id");
        if (id.innerHTML.toLowerCase() == input || id.innerHTML.toLowerCase().includes(input)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });

});

