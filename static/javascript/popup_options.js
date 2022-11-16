let menu_options = document.getElementById("pop_options");
let img_popup = document.getElementById("img_options");


function openOptions(){
    menu_options.style.visibility = "visible";
}

function closeOptions(){
    menu_options.style.visibility = "hidden";
}

try {
    document.addEventListener('click', function (event){
        if (event.target == img_popup) {
            openOptions();
        } else if (event.target != menu_options && event.target != img_popup) {
            closeOptions();
        }
    })
} catch (error) {
    console.log(error);
}
