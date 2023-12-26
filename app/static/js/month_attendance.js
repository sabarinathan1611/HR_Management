const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const totalDays = [31,28,31,30,31,30,31,31,30,31,30,31];
function formatDate(date) {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); // January is 0!
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
}

function getSaturdaysAndSundays(year) {
    const weekends = {};

    for (let month = 0; month < 12; month++) {
        let date = new Date(year, month, 1);
        weekends[monthNames[month]] = [];

        while (date.getMonth() === month) {
            if (date.getDay() === 0 || date.getDay() === 6) { // 0 = Sunday, 6 = Saturday
                weekends[monthNames[month]].push(formatDate(new Date(date)));
            }
            date.setDate(date.getDate() + 1);
        }
    }

    return weekends;
}

// Example usage for the year 2023
const weekendsByMonth = getSaturdaysAndSundays(2023);
// for (const [month, dates] of Object.entries(weekendsByMonth)) {
//     console.log(month + ":");
//     dates.forEach(dateString => console.log(dateString));
// }

let data = [];

function getForMonth(month) {
    // Convert the first letter to uppercase to match the format in weekendsByMonth
    const formattedMonth = month.charAt(0).toUpperCase() + month.slice(1).toLowerCase();

    // Check if the month exists in the data
    if (weekendsByMonth.hasOwnProperty(formattedMonth)) {
        console.log(formattedMonth + ":");
        weekendsByMonth[formattedMonth].forEach(dateString => {
            const day = dateString.split('/')[0]; // Extract the day
            data.push(parseInt(day)); // Print the day
        });
    } else {
        console.log("No data for " + formattedMonth);
    }
}

const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
];

const currentdate = new Date();
const currentMonthString = months[currentdate.getMonth()];

getForMonth(currentMonthString);  // Replace "January" with the desired month

console.log(data);



// attendance.js

// Function to generate a random value for attendance ('a' or 'p')


// attendance.js

// Function to generate a random value for attendance ('a' or 'p')
function getRandomAttendance() {
    return Math.random() < 0.5 ? 'a' : 'p';
}

// Array of random names
const names = [
  'Alice', 'Bob', 'Charlie', 'David', 'Emma',
  'Frank', 'Grace', 'Henry', 'Ivy', 'Jack', 'john', 'doe', 'ellise', 'ispum', 'lorem'
];

// Function to get a random name from the array
function getRandomName() {
    const randomIndex = Math.floor(Math.random() * names.length);
    return names[randomIndex];
}

// Function to generate the attendance table
function generateAttendanceTable() {
    const table = document.querySelector('.attendance-table');
    const tbody = document.querySelector('.attendance-table tbody');
    const thead = document.querySelector('.attendance-table thead tr');

    for(let i=1; i<=31;i++){
        const th = document.createElement('th');
        th.innerHTML = i;
        thead.appendChild(th);
    }
    // Generate 10 rows with sno, roll no, and random names
    for (let i = 1; i <= 15; i++) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="id">#${i.toString().padStart(4, '0')}</td>
            <td class="name">${names[i-1]}</td>
        `;

        // Generate 30 columns with random attendance data
        for (let j = 1; j <= 31; j++) {
            const td = document.createElement('td');
            const randomAttendance = getRandomAttendance();
            td.setAttribute('data-attendance', randomAttendance);
            // td.textContent = randomAttendance;
            if (data.includes(j)) {
                 td.innerHTML = 'H';
            }else{
                if (randomAttendance == 'p') {
                td.innerHTML = (
                    '<i class="fas fa-check-circle"></i>'
                );
            }else if (randomAttendance == "a") {
                td.innerHTML = (
                    '<i class="fas fa-times-circle"></i>'
                )
            }else{
                td.innerHTML = (
                    '-'
                )
            }
            }
            row.appendChild(td);
        }

        tbody.appendChild(row);
    }

    table.appendChild(tbody);
}

// Call the function to generate the attendance table when the script is loaded
generateAttendanceTable();