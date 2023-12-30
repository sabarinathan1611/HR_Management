let date = new Date();

let currentDate = date.getDate();
let currentMonth = date.getMonth();
let currentYear = date.getFullYear();

let displayDate = currentDate + "/" + currentMonth + "/" + currentYear;

if (document.querySelector(".date")) {
  document.querySelector(".date").innerHTML = `Date : ${displayDate}`;
}

if (document.querySelector(".time")) {
  document.querySelector(".time").innerHTML = `Time : ${displayDate}`;
}

// const notification_icon = document.querySelector(".notification-icon");

// notification_icon.addEventListener("click", ()=> {
//     document.querySelector(".notification-list").classList.toggle("active");
// });

const toggle = document.querySelector(".toogle-sidebar");

toggle.addEventListener("click", () => {
  document.querySelector(".sidebar").classList.toggle("active");
  document.querySelector(".main").classList.toggle("active");
});





document.addEventListener("DOMContentLoaded", function () {
  let all_downloads = document.querySelectorAll(".download");

  all_downloads.forEach((download) => {
    download.addEventListener("click", () => {
      let parent = download.parentElement.parentElement.parentElement;
      let table = parent.querySelector("table");

      // Convert the table to a worksheet
      let ws = XLSX.utils.table_to_sheet(table);

      // Create a workbook with a single worksheet
      let wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

      // Convert the workbook to an array buffer
      var wbArrayBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });

      // Create a Blob from the array buffer
      var blob = new Blob([wbArrayBuffer], {
        type: "application/octet-stream",
      });

      // Trigger download using FileSaver.js
      let fileName = parent.querySelector(".frame-details").textContent;
      saveAs(blob, `${fileName}.xlsx`);
    });
  });
});
