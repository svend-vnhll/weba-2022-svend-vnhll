let img_popup = document.getElementById("img_options");
let img_quit = document.getElementById('btn_quit');

try {
    document.addEventListener('click', function (event){
        if (event.target === img_popup) {
            if (window.confirm("Ces options sont verrouillées lorsqu'un match est lancé. \n" +
                "Terminez le match en cours pour pouvoir à nouveau y accéder.")){
                console.log('');
            }
        } else if (event.target === img_quit) {
            if (window.confirm("Vous êtes sur le point de quitter le match en cours et \n" +
                "perdre toutes les données récupérées jusqu'à présent. \n Voulez-vous vraiment continuer ?")) {
                $.ajax({
                type: "POST",
                url: "/reset_match",
                data: {
                    action: "new",
                },
                dataType: 'json'
            });
            window.location.href = "/observation";
            }
        }
    })
} catch (error) {
    console.log(error);
}