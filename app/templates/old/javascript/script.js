function toggleSidebar(event) {
    var sidebar = document.getElementById("sidebar");
    var btn = document.getElementById("menubtn");
  
    sidebar.classList.toggle("active");
    btn.classList.toggle("active");
  }
  
  var filter = document.getElementById("filter");
  const id = document.querySelectorAll(".id");
  const ename = document.querySelectorAll(".name");
  
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
      ename.forEach((e) => {
        value = value.toStrintg().toLowerCase();
        var nameV = e.innerHTML.toString().toLowerCase();
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
          console.log('present'+atn.innerHTML);
          if (atn.innerHTML.toString().toLowerCase() === "present") {
            atn.parentElement.style.display = "";
          } else {
            atn.parentElement.style.display = "none";
          }
        });
      } else {
        attends.forEach((atn) => {
          console.log('absent'+atn.innerHTML);
          if (atn.innerHTML.toString().toLowerCase() === "absent") {
            atn.parentElement.style.display = "";
          } else {
            atn.parentElement.style.display = "none";
          }
        });
      }
    });
  });
  
  // date filter
  
  // var fromDate = document.getElementById("from");
  // var toDate = document.getElementById("to");
  
  // /////////////////////////////////////////////////////////////////////////////////////////
  // function filterTableByDate() {
  //   console.log("called");
  //   if (fromDate.value === "" || fromDate.value.length <= 0) {
  //     if (document.querySelector(".alert")) {
  //       document.querySelector(".alert").remove();
  //     }
  //     var errorbox = document.createElement("div");
  //     errorbox.className = "alert alert-danger";
  //     errorbox.setAttribute("role", "alert");
  //     errorbox.innerHTML = `<i class="fas fa-exclamation-circle"></i> From date is empty `;
  
  //     document.querySelector("body").appendChild(errorbox);
  //   } else {
  //     const dates = document.querySelectorAll(".date");
  //     dates.forEach((date) => {
  //       var dates = date.innerHTML[0] + date.innerHTML[1];
  //       var fromd = fromDate.value.toString().slice(8, 10);
  //       var tod = toDate.value.toString().slice(8, 10);
  //       if (
  //         parseInt(dates) >= parseInt(fromd) &&
  //         parseInt(dates) <= parseInt(tod)
  //       ) {
  //         var mon = date.innerHTML;
  //         mon = mon[3] + mon[4];
  //         var fromMon = fromDate.value[5] + fromDate.value[6];
  //         var toMon = toDate.value[5] + toDate.value[6];
  
  //         if (parseInt(mon) >= fromMon && mon <= toMon) {
  //           date.parentElement.style.display = "";
  //         } else {
  //           date.parentElement.style.display = "none";
  //         }
  //       } else {
  //         date.parentElement.style.display = "none";
  //       }
  //     });
  //   }
  // }
  
  // document.getElementById("from").addEventListener("change", filterTableByDate);
  // document.getElementById("to").addEventListener("change", filterTableByDate);
  
  var edit_btns = document.querySelectorAll(".edit-btn");
  
  function editmodul(event) {
    var id = event.target.parentElement.parentElement.children[0].innerHTML;
    var uname = event.target.parentElement.parentElement.children[1].innerHTML;
    var attend = event.target.parentElement.parentElement.children[2].innerHTML;
    var dob = event.target.parentElement.parentElement.children[3].innerHTML;
    var workType = event.target.parentElement.parentElement.children[4].innerHTML;
    var phnum = event.target.parentElement.parentElement.children[5].innerHTML;
    var aadhar = event.target.parentElement.parentElement.children[6].innerHTML;
    var address = event.target.parentElement.parentElement.children[7].innerHTML;
    var gender = event.target.parentElement.parentElement.children[8].innerHTML;
    var module = document.querySelector(".module");
    module.classList.add("active");
    document.getElementById("empid").value = id;
    document.getElementById("uname").value = uname;
    document.getElementById("worktype").value = workType;
    document.getElementById("attend").value = attend;
    document.getElementById("dob").value = dob;
    document.getElementById("Phnumber").value = phnum;
    document.getElementById("aadhar").value = aadhar;
    document.getElementById("address").value = address;
    document.getElementById("gender").value = gender;
  }
  
  function change() {
    var module = document.querySelector(".module");
    module.classList.remove("active");
  }
  
  edit_btns.forEach((edit) => {
    edit.addEventListener("click", function (event) {
      editmodul(event);
    });
  });

function deleteEmp(EmpId) {
  // Sending a DELETE request to the server to delete the employee with the specified EmpId.
  console.log("emp: ",EmpId);
  fetch("/delete-emp", {
    method: "POST", 
    headers: {
      "Content-Type": "application/json", // Set the content type to JSON
    },
    body: JSON.stringify({ EmpId: EmpId }), // The request body contains the employee ID to be deleted in JSON format.
  }).then(response => response.json())
  .then(data =>{
    console.log(data);
    let msg = data;
    alert(msg.message);
  })
}

  const delete_btn = document.querySelectorAll(".delete-btn");
  
  delete_btn.forEach((btn) => {
    btn.addEventListener("click", function (event) {
      const empId = event.target.getAttribute('data-emp-id'); // Assuming you have stored the employee ID as a data attribute (e.g., data-emp-id) on the delete button.
      // console.log(empId);
      // console.log(typeof(empId));
      deleteEmp(empId); // Call the deleteEmp function with the employee ID.
      btn.parentElement.parentElement.remove();

      
    });
  });


function change(event) {
  var module = document.querySelector(".module");
  module.classList.remove("active");
  event.target.type = 'submit';
  event.target.click();

}
const addbtn = document.querySelector('.addbtn');
const addformbtn = document.querySelector('.addformbtn');
const addform = document.querySelector('.addform')

addbtn.addEventListener("click",function(){
    addform.classList.add('active');
});

addformbtn.addEventListener('click', function(){
    addform.classList.remove('active');
})
