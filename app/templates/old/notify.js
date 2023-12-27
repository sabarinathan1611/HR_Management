console.log('notification js is connected .. !');

// Ensure the DOM is ready before executing JavaScript.
document.addEventListener("DOMContentLoaded", function () {
    const notifications = document.querySelectorAll('.notification');

    notifications.forEach(notification => {
        notification.addEventListener("click", function () {
            notification.classList.add("done");
            notification.classList.remove("active");
            setTimeout(() => {
                notification.remove();
            }, 1000);
        });
    });

    const clear = document.querySelector(".clear");

    clear.addEventListener("click", function () {
        console.log('clearing all notifications');

        var count = document.querySelector(".innerNotification").childElementCount;

        for (let i = 0; i < count; i++) {
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
});
