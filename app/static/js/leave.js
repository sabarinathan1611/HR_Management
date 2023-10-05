console.log(`"_leave.js connected..!_"`);

const profileSection = document.querySelector('.profileSection');
const closeForm = document.querySelector('.closeForm');
const leaveBtn = document.querySelector('.leaveBtn');

const otherRadioInputs = document.querySelectorAll('input[type="radio"]');
const otherTextArea = document.querySelector('.other');
const otherOption = document.getElementById("other");

// textarea enable and disable function..
otherRadioInputs.forEach(radio => {
    radio.addEventListener('click',function(){
        if (otherOption.checked == true) {
            otherTextArea.style.display = 'flex';
        }else{
            otherTextArea.style.display = 'none';
        }
    })
});



leaveBtn.addEventListener('click',function(){
    document.querySelector('.formSection').classList.add('active');
    profileSection.classList.remove('active');
});


closeForm.addEventListener('click',function(){
    document.querySelector('.formSection').classList.remove('active');
    profileSection.classList.add('active');
    document.querySelector('.leave').reset();
});

const user_input = document.querySelectorAll('.user_input');

user_input.forEach(input => {
    input.addEventListener('focus', function() {
        user_input.forEach(userInp => {
            userInp.classList.remove('active');
        });
        input.classList.add('active');
    });
});

// user



const changeOpts = document.querySelectorAll('.change');

changeOpts.forEach(change => {
    change.addEventListener('click',function(){
        document.getElementById('uname').value = change.innerHTML;
        document.querySelector('.changeOptContainer').style.display = 'block';
    })
});


const unameInput = document.getElementById('uname');

const user = {};

user.ID = document.querySelector('.uid').innerHTML;
console.log(user);

function checkInputType(input) {
    if (!isNaN(parseFloat(input)) && isFinite(input)) {
        return 'Number';
    } else if (typeof input === 'string') {
        if (!isNaN(Date.parse(input))) {
            return 'Date';
        } else if (input.includes('@') && input.includes('.')) {
            return 'Email';
        } else if (/^[a-zA-Z\s]+$/.test(input)) {
            return 'StringAlphabetical';
        } else {
            return 'String';
        }
    } else {
        return 'Unknown';
    }
}

function changeUserDet() {
    const input = unameInput.value;
    if (input) {
        const output = checkInputType(input);

        if (output === 'Number') {
            if (/^\d{10}$/.test(input)) {
                user.newId = input;
                document.querySelector('.changeOptContainer').style.display = 'none';
                document.querySelector('.uphone').innerHTML = input;
            } else {
                alert('Phone number should have exactly 10 digits.');
            }
        } else if (output === 'StringAlphabetical') {
            user.newName = input;
            document.querySelector('.uname').innerHTML = input;
            document.querySelector('.changeOptContainer').style.display = 'none';
        } else if (output === 'Date') {
            user.newDate = input;
            document.querySelector('.changeOptContainer').style.display = 'none';
            document.querySelector('.udoj').innerHTML = input;
        } else if (output === 'Email') {
            user.newEmail = input;
            document.querySelector('.changeOptContainer').style.display = 'none';
            document.querySelector('.uemail').innerHTML = input;
        } else {
            alert('Give a valid input!');
        }
        console.log(user);
    } else {
        alert('Empty request');
    }
}
