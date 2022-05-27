let is_failed = true;
getHasComeBoxes();
handleEditButtonsClick();
handleLiterGradeChanges();

// get_data(1);

function get_data(id) {
    let url =  `litergrade_list/${id}`
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => {
        let result = response.json()
        let status_code = response.status;
        if(status_code !== 200) {
            console.log('Error in getting list!')
            return false;
        }
        return result
    })
    .then(result => {
        // console.log(result);
        render_table(result);
    })
    .catch(error => {
        console.log(error)
    })
}

function render_table(data) {
    console.log(data.table_head);
    const app = document.getElementById('app');
    const table = document.createElement('table');
    table.className = 'table table-striped table-bordered w-50';
    const thead = document.createElement('thead');
    const thead_tr = document.createElement('tr');
    data.table_head.forEach(element => {
        let th = document.createElement('th')
        th.innerHTML = element;
        th.className = 'text-center'
        thead_tr.appendChild(th);
    });
    app.appendChild(table).appendChild(thead).appendChild(thead_tr);
    const tbody = document.createElement('tbody');
    let num = 1;
    data.data.forEach(element => {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.innerHTML = num.toString();
        td.className = 'text-center'
        tr.appendChild(td);
        num++;
        const keys = ['last_name' , 'first_name' , 'fathers_name' , 'litergarde', 'has_come']
        let csrfToken = getCookie('csrftoken');
        for (const [key, value] of Object.entries(element)) {
            if (keys.includes(key)) {
                const td = document.createElement('td');
                if (key !== 'has_come') td.innerHTML = value.toString()
                else {
                    const form = document.createElement('form');
                    form.action = ''
                    form.method = 'post'
                    const csrfTokeninput = document.createElement('input');
                    csrfTokeninput.type = 'hidden';
                    csrfTokeninput.name = 'csrfmiddlewaretoken';
                    csrfTokeninput.value = csrfToken;
                    form.appendChild(csrfTokeninput);
                    const inputParticipant = document.createElement('input');
                    inputParticipant.type = 'hidden';
                    inputParticipant.value = element.pk;
                    inputParticipant.name = 'participant_pk';
                    form.appendChild(inputParticipant);
                    const input = document.createElement('input');
                    input.type = 'checkbox';
                    input.checked = value.toString() === 'true';
                    input.id = element.pk;
                    input.name = 'has_come';
                    input.className = 'has_come';
                    td.appendChild(form).appendChild(input);
                }
                if (key === 'litergarde' || key === 'has_come') td.className = 'text-center'
                tr.appendChild(td)
            }
        }
        tbody.appendChild(tr);
    })
    table.appendChild(tbody);
    getHasComeBoxes();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getHasComeBoxes() {
    let has_come = document.querySelectorAll('.has_come');
    has_come.forEach(
        element => element.addEventListener('change', event => {
            let pk = element.id;
            let has_come = element.checked;
            postHasComeState(pk, has_come);
            event.stopImmediatePropagation();
            event.preventDefault();
        })
    );
}

function postHasComeState(participant_pk, has_come) {
    let data = {participant_pk: participant_pk, has_come: has_come};
    const url = '/second_tour/check_list/set_has_come';
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
        return response.text();
        //return response.json()
    })
    .then(data => showAlert(data) )
}

function postParticipantLiterGrade(participant_pk, litergrade_pk) {
    let data = {participant_pk: participant_pk, litergrade_pk: litergrade_pk};
    const url = '/second_tour/check_list/set_participant_litergrade';
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
    .then(data => showAlert(data) )
}

function showAlert(data) {
    const parent_div = document.getElementById('app');
        const status_alert = document.createElement('div');
        if (data.toString() === '0') {
            status_alert.className = 'alert alert-success';
            status_alert.innerHTML = 'Действие выполнено успешно';
        } else {
            status_alert.className = 'alert alert-danger';
            status_alert.innerHTML = `Ошибка: ${data}`;
        }
        status_alert.style.maxWidth = '400px'
        status_alert.style.opacity = '0.92';
        status_alert.tabIndex = 1000;
        status_alert.style.position = 'fixed';
        status_alert.style.left = `calc(50%-${status_alert.style.width / 2}`;
        status_alert.style.top =  '65px';// `calc(50%-${status_alert.style.height / 2}`;
        parent_div.appendChild(status_alert)
        setTimeout(function() {
            status_alert.remove();
        }, 2500);
}

function handleEditButtonsClick() {
    let edit_btn = document.querySelectorAll('#edit_btn');
    edit_btn.forEach(
        element => element.addEventListener('click', event => {
            const btn = event.currentTarget;
            const span = btn.parentElement.firstElementChild;
            btn.hidden = true;
            const  select = btn.parentElement.children[2].hidden = false;
            event.stopImmediatePropagation();
            event.preventDefault();
        })
    );
}

function handleLiterGradeChanges() {
    let selects = document.querySelectorAll('#liter_grade_select');
    selects.forEach(
        element => element.addEventListener('change', event => {
            const select = event.currentTarget;
            const span = select.parentElement.firstElementChild;
            const btn = select.parentElement.children[1].hidden = false ;
            select.hidden = true;
            const litergrade_pk = select.options[select.selectedIndex].value;
            const oldValue = span.innerHTML;
            const participant_pk = select.parentElement.parentElement.lastElementChild.firstElementChild.value.toString();
            span.innerHTML = select.options[select.selectedIndex].text;
            postParticipantLiterGrade(participant_pk, litergrade_pk);
            // alert(is_failed);
            event.stopImmediatePropagation();
            event.preventDefault();
        })
    );
}

function renderSelect(parentElement) {
    const select = document.createElement('select');
    const option = document.createElement('option');
    option.selected = true;
    option.value = '';
    select.appendChild(option);
    const literGrades = [71, 72, 73, 74, 75, 76];
    literGrades.forEach(element => {
        const option = document.createElement('option');
        option.value = element.toString();
        option.text = element.toString();
        select.appendChild(option);
    })
    parentElement.appendChild(select);
}


/*
    (function() {
        let selector = '.has_come';
        document.addEventListener('change', function(e) {
            // All click events will be handled by this function, so it needs to be as cheap as possible. To check
            // whether this function should be invoked, we're going to check whether the element that was clicked on
            // was the elemnt that we care about. The element that was clicked on is made available at "e.target"
            let el = e.target;
            // Check if it matches our previously defined selector
            if (!el.matches(selector)) {
                return;
            }
            // This is a contrived example that just sleeps for one second, however more commonly you'll see this with
            // AJAX calls or just expensive JavaScript.
            setTimeout(function() {
                alert('Hello!');
            }, 3000); // 3 second timeout
            console.log(el);
        });
    })();
*/