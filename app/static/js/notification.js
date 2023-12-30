const bell_btn = document.querySelector(".notification-btn");
const notifications = document.querySelector(".notifications");
const add = document.querySelector(".add");
let count = notifications.childElementCount;

if (count > 9) {
    count = "9+";
}

document.querySelector(".count").innerHTML = count;

document.addEventListener('click', function (event) {
    const isNotificationButton = event.target.closest('.notification-btn');
    const isNotificationContainer = event.target.closest('.notifications');

    if (!(isNotificationButton || isNotificationContainer)) {
        notifications.classList.remove("active");
        console.log("Removed active class");
    }
});

bell_btn.addEventListener("click", () => {
    notifications.classList.toggle("active");
    console.log("Toggled active class");
});

      const socket = io();
      socket.on("late", function (late_permission) {
          console.log("Received late_permission:",late_permission.emp_id);
          const notifications = document.querySelector(".notifications");
          
          if(document.querySelector(".notification-box")){
                const default_notification=document.querySelector(".notification-box");
                default_notification.style.display = "none";
                default_notification.disabled = true;
              }
                  notifications.innerHTML += `
                  <li class="notification-box">
                      <div class="profile">
                          <img src="icon/default.jpeg" alt="default user">
                      </div>
                      <div class="notification-details">
                          <div class="notification-user-name">
                              ${late_permission.emp_name}
                          </div>
                          <div class="notification-message">
                              Late - ${late_permission.reason}
                          </div>
                      </div>
                  </li>
                                `;
                  let count = notifications.childElementCount;
                  if (count > 10) {
                      count = "9+";
                  }

                  document.querySelector(".count").innerHTML = count-1;
                });

          socket.on("leave", function (leave_permission) {
              console.log("Received leave_permission:",leave_permission.emp_id);
              const notifications = document.querySelector(".notifications");

              if(document.querySelector(".notification-box")){
                const default_notification=document.querySelector(".notification-box");
                default_notification.style.display = "none";
                default_notification.disabled = true;
              }

                  notifications.innerHTML += `
                  <li class="notification-box">
                      <div class="profile">
                          <img src="icon/default.jpeg" alt="default user">
                      </div>
                      <div class="notification-details">
                          <div class="notification-user-name">
                              ${leave_permission.emp_name}
                          </div>
                          <div class="notification-message">
                              Leave - ${leave_permission.reason}
                          </div>
                      </div>
                  </li>
                                `;
                  let count = notifications.childElementCount;
                  if (count > 10) {
                      count = "9+";
                  }

                  document.querySelector(".count").innerHTML = count-1;
                });