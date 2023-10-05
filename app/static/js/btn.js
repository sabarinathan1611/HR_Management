console.log( 'btn setup .js logged in ' );

const btnlist = document.querySelectorAll(".btnlist");
var tableName ;
btnlist.forEach(btn => {
    btn.addEventListener('click',function(){
        if (btn.classList.toString().toLowerCase().includes('leave')) {
            tableName = 'leavetable';
            sessionStorage.setItem('active',tableName);
        }else if (btn.classList.toString().toLowerCase().includes('late')) {
            // document.querySelector('.latetable').style.display = 'table';
            tableName = 'latetable';
            sessionStorage.setItem('active',tableName);
        }else if (btn.classList.toString().toLowerCase().includes('attendance')) {
            // document.querySelector('.attendancetable').style.display = 'table';
            tableName = 'attendancetable';
            sessionStorage.setItem('active',tableName);
        } 
        displayTable();
    });
});



// console.log('table name = '+ activeTableName);

function displayTable(){

    document.querySelectorAll(".table").forEach(table => {
        table.style.display = 'none';
    });

    var activeTableName = sessionStorage.getItem('active');
    
    if (activeTableName === undefined || activeTableName === null) {
        document.querySelector(`.leavetable`).style.display = 'table';
    }else{
        document.querySelector(`.${activeTableName}`).style.display = 'table';
    }
    
}

displayTable();