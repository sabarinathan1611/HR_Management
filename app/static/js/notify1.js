console.log('notification js is connected .. !');

const notification = document.querySelectorAll('.notification');

const reasons = ['Late', 'Leave', 'HOD request', 'Missed Punch in','Missed Punch out','Shift Changed Person','Absent List'];

notification.forEach(click => {
    click.addEventListener("click", function () {
        click.classList.add("done");
        click.classList.remove("active");
        setTimeout(() => {
            click.remove();
        }, 1000);
    })
});

function removeNotify(event) {
    if (event.target.parentElement && event.target.parentElement.classList.contains("notification")) {
        event.target.parentElement.classList.add("done");
        event.target.parentElement.classList.remove("active");
    } else {
        event.target.classList.add("done");
        event.target.classList.remove("active");
    }

    setTimeout(() => {
        if (event.target.parentElement && event.target.parentElement.classList.contains("notification")) {
            event.target.parentElement.remove()
        } else {
            event.target.remove();
        }
    }, 500);
}


const addnotification = document.querySelector('.addnotification');

addnotification.addEventListener("click", function () {
    const rand_reasons = reasons[Math.floor(Math.random() * reasons.length)];

    const currentTime = new Date().toLocaleTimeString();

    var new_Notification = document.createElement("div")
    new_Notification.classList.add('notification');
 
    var notifyMsg = document.createElement("div");
    notifyMsg.classList.add('notifyMsg');
    notifyMsg.innerText = `${rand_reasons}`;

    var notifyTime = document.createElement("div");
    notifyTime.classList.add('notifyTime');
    notifyTime.innerText = `${currentTime}`;

    new_Notification.appendChild(notifyMsg);
    new_Notification.appendChild(notifyTime);

    new_Notification.addEventListener('click',function(event){
        removeNotify(event);
    });

    setTimeout(() => {
        new_Notification.classList.add('active');
    }, 200);

    document.querySelector(".innerNotification").appendChild(new_Notification);
});

const clear = document.querySelector(".clear");

clear.addEventListener("click",function(){
console.log('clearing  all notifications');

var count  = document.querySelector(".innerNotification").childElementCount;
// console.log(count);

for(let i = 0; i<count; i++){
    document.querySelector(".innerNotification").children[i].classList.remove('active');
    document.querySelector(".innerNotification").children[i].classList.add('done');
}


var clear = setInterval(() => {
    var innerNotification = document.querySelector(".innerNotification");
    while (innerNotification.firstChild) {
        innerNotification.firstChild.remove();
    }

    if (!innerNotification.firstChild) {
        clearInterval(clear);
    }
}, 750);


});