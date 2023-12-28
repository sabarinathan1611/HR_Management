let date = new Date()
console.log("script.js connected");

let currentDate = date.getDate();
let currentMonth = date.getMonth();
let currentYear = date.getFullYear();

let displayDate = (currentDate+"/"+currentMonth+"/"+currentYear);

document.querySelector(".date").innerHTML = `Date : ${displayDate}`;
document.querySelector(".time").innerHTML = `Time : ${displayDate}`;


const notification_icon = document.querySelector(".notification-icon");

notification_icon.addEventListener("click", ()=> {
    document.querySelector(".notification-list").classList.toggle("active");
});

const toggle = document.querySelector(".toogle-sidebar");

toggle.addEventListener("click", ()=>{
    document.querySelector(".sidebar").classList.toggle("active");
    document.querySelector(".main").classList.toggle("active");
})


document.querySelector('.download-btn').addEventListener('click', function() {
    let confirmation = confirm("are you sure..?");

    if (confirmation) {
        document.querySelector(".model-footer").style.display = 'none';
        html2canvas(document.querySelector('.notification-model')).then(canvas => {
            // Create an image and set its source to the canvas data
            var image = canvas.toDataURL("image/png");
            // Create a temporary link to trigger the download
            var tmpLink = document.createElement('a');
            tmpLink.download = 'username.png'; // Set the download name
            tmpLink.href = image;
            
            // Temporarily add the link to the document and trigger the download
            document.body.appendChild(tmpLink);
            tmpLink.click();
            document.body.removeChild(tmpLink);
            document.querySelector(".model-footer").style.display = 'flex';
        });
    }
});

document.querySelector('.print-btn').addEventListener('click', function() {
    window.print();
});

