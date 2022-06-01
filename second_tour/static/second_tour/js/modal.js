// const modal = document.getElementById("myModal");
// const openBtn = document.getElementById("open_modal");
// const closeBtn1 = document.getElementsByClassName("close")[0];
// const closeBtn2 = document.getElementById('close_modal');
// const addBtn = document.getElementById('add_participant');
// const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
// let literGrades;
// console.log(csrfToken);
//
// openBtn.onclick = function() {
//   modal.style.display = "block";
//   getLiterGrade();
// }
//
// closeBtn1.onclick = function() {
//   modal.style.display = "none";
// }
//
// closeBtn2.onclick = function() {
//   modal.style.display = "none";
// }
//
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }
//
// addBtn.onclick = function() {
//   setTimeout(function() {
//       modal.style.display = "none";
//   }, 2000);
// }
//
// function getLiterGrade() {
//     const url = '/second_tour/check_list/add_participant';
//     fetch(url, {
//         method: 'GET',
//         headers: {
//         'Content-Type': 'application/json'
//       }
//     })
//     .then(response => {
//         const result = response.json();
//         const status_code = response.status;
//         if(status_code !== 200) {
//             console.log('Ошибка получения данных')
//             return false;
//         }
//         return result
//     })
//     .then(result => {
//         renderLitegrade(result);
//     })
//     .catch(error => { console.log(error) });
// }
//
// function renderLitegrade(litergrades) {
//     const literGrade = document.getElementById('litergrade');
//     litergrades.forEach( item => {
//         const gradeOption = document.createElement('option');
//         gradeOption.text = `${item.grade}.${item.name}`;
//         gradeOption.id = item.pk;
//         literGrade.appendChild(gradeOption);
//     });
//
// }