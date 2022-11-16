try {
    $(document).ready(function () {
        $(".infos_cours").click(function (event) {
            event.preventDefault();
            window.location.href = "/choisir_cours/" + $(this).attr('id');
        });
    });

    $(document).ready(function () {
        $(".del_cours").click(function (event) {
            event.preventDefault();
            if (window.confirm("Êtes-vous sûr de vouloir supprimer ce cours ?")){
                window.location.href = "/supprimer_cours/" + $(this).attr('id');
            }
        });
    });

} catch (error) {
    console.log(error);
}


