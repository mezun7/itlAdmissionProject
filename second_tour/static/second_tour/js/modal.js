const form = document.querySelector('.needs-validation');
const modal = document.getElementById("myModal");
const openBtn = document.getElementById("open_modal");
const closeBtn1 = document.getElementsByClassName("close")[0];
const closeBtn2 = document.getElementById('close_modal');
const addBtn = document.getElementById('add_participant');
const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
console.log(csrfToken);
let formData;

openBtn.onclick = function() {
    modal.style.display = "block";
    form.classList.remove('was-validated');
    getLiterGrade();
    formData = {
        email: document.getElementById('email'),
        surname: document.getElementById('surname'),
        name: document.getElementById('name'),
        patronymic: document.getElementById('patronymic'),
        gender: document.getElementById('gender'),
        litergrade: document.getElementById('litergrade'),
        phone: document.getElementById('phone'),
    };
}

closeBtn1.onclick = function() {
    for (const [key, value] of Object.entries(formData)) { value.value = ''}
    modal.style.display = "none";
}

closeBtn2.onclick = function() {
    for (const [key, value] of Object.entries(formData)) { value.value = ''}
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

addBtn.onclick = function() {
    if (form.checkValidity()) {
        let data = {
            email: formData.email.value.replace(/\s/g, ''),
            surname: formData.surname.value.replace(/\s/g, ''),
            name: formData.name.value.replace(/\s/g, ''),
            patronymic: formData.patronymic.value.replace(/\s/g, ''),
            gender: formData.gender.value,
            litergrade: formData.litergrade.value,
            grade: formData.litergrade[formData.litergrade.selectedIndex].text.split('.')[0],
            parent_name: '',
            mother: true,
            phone: formData.phone.value,
        };
        const url = '/second_tour/check_list/add_participant';
        fetch(url, {
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            return is_failed = response.text() ; //.toString() !== '0';
        })
        .then(data => showAlert(data));
        setTimeout(function() {
            for (const [key, value] of Object.entries(formData)) { value.value = ''}
            modal.style.display = "none";
            data = {};
        }, 500);
    };
    form.classList.add('was-validated');
}

function getLiterGrade() {
    const url = '/second_tour/check_list/add_participant';
    fetch(url, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
        const result = response.json();
        const status_code = response.status;
        if(status_code !== 200) {
            console.log('Ошибка получения данных')
            return false;
        }
        return result
    })
    .then(result => {
        renderLitegrade(result);
    })
    .catch(error => { console.log(error) });
}

function renderLitegrade(litergrades) {
    const literGrade = document.getElementById('litergrade');
    litergrades.forEach( item => {
        const gradeOption = document.createElement('option');
        gradeOption.text = `${item.grade}.${item.name}`;
        gradeOption.value = item.pk;
        literGrade.appendChild(gradeOption);
    });

}

jQuery(function($){
    $(".phone_no").mask("+7 (999) 999-99-99");
    $(".date").mask("99.99.9999");
});

function isFieldValidated() {
    'use strict'
    const form = document.querySelectorAll('.needs-validation')
    // let isValidated = false;
    // for (const [key, value] of Object.entries(formData)) {
    //     if (!formData[`${key}`].checkValidity()) {
    //         isValidated = false;
    //         formData[`${key}`].classList.add()
    //         formData[`${key}`].checkValidity()
    //         console.log(formData[`${key}`]);
    //     }
    // }
    return isValidated;
}