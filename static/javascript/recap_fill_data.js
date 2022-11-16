
function showMatchs(id){
    $("#content").load('/load_matchs/' + id);
}

function showInfosMatch(id_elv, id_match){
    $("#echanges").load('/load_echanges_match/' + id_elv + '/' + id_match);
    $("#infos_match").load('/load_infos_match/' + id_elv + '/' + id_match);
}

function deleteEleveMatch(id_elv, id_match){
    if (window.confirm("Souhaitez-vous vraiment retirer cet élève de ce match ? \n" +
        "Aucun retour possible si vous acceptez !")){
        $.ajax({
            type: "POST",
            url: "/delete_player",
            data: {
                id_elv: id_elv,
                id_match: id_match
            },
            dataType: 'json'
        });
        setTimeout(function (){
            showMatchs(id_elv);
        }, 500)
    }
}

function deleteEleve(id_elv){
    if (window.confirm("Souhaitez-vous vraiment supprimer cet élève ? \n" +
        "Aucun retour possible si vous acceptez !")) {
        window.location.href = "/delete_eleve/" + id_elv;
    }
}

function updateEleve(id_elv){
    window.location.href = "/recap_updating/" + id_elv;
}

function confirmUpdate(id_elv){
    $.ajax({
            type: "POST",
            url: "/recap",
            data: {
                eleve: id_elv,
                input: document.getElementById('input').value,
            },
            dataType: 'json'
        });
    setTimeout(function (){
        window.location.href = "/recap";
        }, 100)
}