
function deleteEmp(EmpId) {
   
    fetch("/delete-emp", {
      method: "Emp",
      body: JSON.stringify({ EmpId: EmpId }),
    }).then((_res) => {
      window.location.href = "/";
      
    });
  }
