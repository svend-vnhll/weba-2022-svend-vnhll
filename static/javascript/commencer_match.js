let commencer = document.getElementById('start');
let eleve_1;
let eleve_2;
let eleve_3;

function changementEleve1() {
    eleve_1 = document.getElementById('select_eleve1').value;
    return eleve_1;
}

function changementEleve2() {
    eleve_2 = document.getElementById('select_eleve2').value;
    return eleve_2;
}

function changementEleve3() {
    eleve_3 = document.getElementById('select_eleve3').value;
    return eleve_3;
}

eleve_1 = changementEleve1();
eleve_2 = changementEleve2();
eleve_3 = changementEleve3();


document.getElementById('start').addEventListener("click", function () {
    if ((eleve_1 == eleve_2 || eleve_1 == eleve_3) || eleve_2 == eleve_3 || eleve_1 == '' || eleve_2 == '' || eleve_3 == '') {
        alert("Erreur lors de la sélection des élèves.");

    } else {
        console.log(url_start);
        commencer.href = url_start + '/' + eleve_1+ '/' + eleve_2+ '/' + eleve_3;
    }
})
