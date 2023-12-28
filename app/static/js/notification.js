const bell_btn = document.querySelector(".notification-btn");
const notifications = document.querySelector(".notifications");
const add = document.querySelector(".add");

bell_btn.addEventListener("click", ()=>{
    notifications.classList.toggle("active");
});

add.addEventListener("click", ()=> {
    let li = document.createElement("li");

    li.innerHTML = `
        <li class="notification">
                <div class="profile">
                    <img src="icon/default.jpeg" alt="default user">
                </div>
                <div class="notification-details">
                    <div class="notification-user-name user-name">
                        User name 1
                    </div>
                    <div class="notification-message message-subject">
                        requesting leave regarding late for today bla bla bla
                        requesting leave regarding late for today bla bla bla
                    </div>
                </div>
            </li>
    `;
    notifications.appendChild(li);

    let count = notifications.childElementCount;
    if (count > 9) {
        count = "9+";
    }

    document.querySelector(".count").innerHTML = count;
});