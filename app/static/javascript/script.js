function toggleSidebar(event) {
  var sidebar = document.getElementById("sidebar");
  var btn = document.getElementById("menubtn");

  sidebar.classList.toggle("active");
  btn.classList.toggle("active");
}

var filter = document.getElementById("filter");
const id = document.querySelectorAll(".id");
const name = document.querySelectorAll(".name");

filter.addEventListener("input", function () {
  let value = filter.value;
  if (!isNaN(value)) {
    id.forEach((e) => {
      var idV = e.innerHTML;
      if (idV.includes(value)) {
        e.parentElement.style.display = "";
      } else {
        e.parentElement.style.display = "none";
      }
    });
  } else {
    name.forEach((e) => {
      var nameV = e.innerHTML;
      if (nameV.includes(value)) {
        e.parentElement.style.display = "";
      } else {
        e.parentElement.style.display = "none";
      }
    });
  }
});

const navbtns = document.querySelectorAll(".nav-item");

navbtns.forEach((btn) => {
  var attends = document.querySelectorAll(".attend");

  btn.addEventListener("click", function () {
    if (btn.getAttribute("index") === "0") {
      attends.forEach((atn) => {
        atn.parentElement.style.display = "";
      });
    } else if (btn.getAttribute("index") === "1") {
      attends.forEach((atn) => {
        if (atn.innerHTML.toLowerCase() === "present") {
          atn.parentElement.style.display = "";
        } else {
          atn.parentElement.style.display = "none";
        }
      });
    } else {
      attends.forEach((atn) => {
        if (atn.innerHTML.toLowerCase() === "absent") {
          atn.parentElement.style.display = "";
        } else {
          atn.parentElement.style.display = "none";
        }
      });
    }
  });
});

// date filter

var fromDate = document.getElementById("from");
var toDate = document.getElementById("to");

// toDate.addEventListener("input", function () {

// });

// /////////////////////////////////////////////////////////////////////////////////////////
function filterTableByDate() {
  if (fromDate.value === "" || fromDate.value.length <= 0) {
    if (document.querySelector(".alert")) {
      document.querySelector(".alert").remove();
    }
    var errorbox = document.createElement("div");
    errorbox.className = "alert alert-danger";
    errorbox.setAttribute("role", "alert");
    errorbox.innerHTML = `<i class="fas fa-exclamation-circle"></i> From date is empty `;

    document.querySelector("body").appendChild(errorbox);
  } else {
    const dates = document.querySelectorAll(".date");
    dates.forEach((date) => {
      if (date.innerHTML >= fromDate.value && date.innerHTML <= toDate.value) {
        var val = date.innerHTML;
        val = val[3] + val[4];
        var fromMon = fromDate.value[3] + fromDate.value[4];
        var toMon = toDate.value[3] + toDate.value[4];

        // date.parentElement.style.display = "";
        if (val >= fromMon && val <= toMon) {
          date.parentElement.style.display = "";
        } else {
          date.parentElement.style.display = "none";
        }
      } else {
        date.parentElement.style.display = "none";
      }
    });
  }
}

document.getElementById("from").addEventListener("keyup", filterTableByDate);
document.getElementById("to").addEventListener("keyup", filterTableByDate);
