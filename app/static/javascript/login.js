console.log(`logged....!`);

const error = document.querySelector(".error");

var uname = document.getElementById("username");
var password = document.getElementById("password");

const submit = document.querySelector(".submit");

submit.addEventListener("click", function () {
  var name = uname.value;
  var pass = password.value;

  if (name === "" || uname === undefined) {
    error.innerHTML = `<p class="msg">username is requiered</p>`;
  } else if (pass === "" || pass === undefined) {
    error.innerHTML = `<p class="msg">password is requiered</p>`;
  } else {
    uname.value = "";
    password.value = "";
    submit.type = "submit";
    submit.click();
  }
});
