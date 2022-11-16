function openForm() {
    document.getElementById("popup_form").style.visibility = "visible";
    document.getElementById("popup_form").style.display = "block";
}

function closeForm() {
    document.getElementById("popup_form").style.visibility = "hidden";
    document.getElementById("popup_form").style.display = "none";
}

// document.addEventListener('click', function (event){
//         if (event.target === document.getElementById('popup_form')){
//             openForm();
//         }
//         else if (event.target !== document.getElementById("popup_form")) {
//             closeForm();
//         }
// })
