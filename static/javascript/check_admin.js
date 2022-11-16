let btn_quit = document.getElementById('btn_quit');
let btn_save = document.getElementById('btn_save');
let btn_eleves = document.getElementById('btn_eleves');
let btn_grille = document.getElementById('btn_grille');
let btn_recap = document.getElementById('btn_recap');

let confirmer = document.getElementById('Confirmer');
let annuler = document.getElementById('Annuler');
let check_admin = document.getElementById('check_admin');
let input_password = document.getElementById('input_password');


try {
    function showDiv(bool){
        if (bool){
            check_admin.style.visibility = "visible";
        } else {
            check_admin.style.visibility = "hidden";
        }
    }

    function setDestination(d){
        document.getElementById('destination').value = d;
        console.log(document.getElementById('destination').value);
    }

    document.addEventListener('click', function (event){
        if (event.target === btn_quit || event.target === btn_save || event.target === btn_eleves || event.target === btn_grille || event.target === btn_recap) {
            showDiv(true);
        } else if (event.target !== check_admin && event.target !== confirmer && event.target !== annuler && event.target !== input_password) {
            showDiv(false);
        }
    })

    confirmer.addEventListener('click', function(event){
        event.preventDefault();
        if (input_password.value === ''){
            document.getElementById('pass_alert').innerText = "Mot de passe erroné.";
        } else {

            $.ajax({
                type: "POST",
                url: "/redirected",
                data: {
                    destination: $('#destination').val(),
                    input: $('#input_password').val(),
                },
                dataType: 'json'
            });
            input_password.value = "";
            setTimeout(function(){
                $("#banner").load('/change_path');
                $("#pass_alert").load('/error_message');
                setTimeout(function(){
                    document.getElementById('link').click();
                }, 1000);
            }, 1000);

        }
    })
} catch (error) {
    console.log(error);
}