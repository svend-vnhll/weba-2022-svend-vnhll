let last_tir_zone;
let pop_inputs = document.getElementById('pop_input_tir');
let court = document.getElementById('court');
let body = document.getElementById('body');
let court_a = document.getElementById('eleA');
let court_b = document.getElementById('eleB');
let filet = document.getElementById('0');
let cpt_tir = 0;
const limite_score = 5;
let zone_precedente = "none";
let zones_a = [1,2,3,11,12,21,22,23,24,25,26,27]
let zones_b = [101,102,103,111,112,121,122,123,124,125,126,127]


function unlockResetButton(bool) {
    let div_reset = document.getElementById('img_reset')
    if (bool) {
        div_reset.innerHTML = "<img id='reset_btn' onclick='confirmAction()' src='" + static_path + "icones/icon_reset.png'>";
    } else {
        div_reset.innerHTML = "<img src='" + static_path + "icones/icon_reset_locked.png'>";
    }
}

function unlockNextButton(bool) {
    let div_next = document.getElementById('img_next')
    if (bool) {
        div_next.innerHTML = "<img id='next_btn' onclick='terminerMatch()'   src='" + static_path + "icones/icon_next.png'>";
    } else {
        div_next.innerHTML = "<img src='" + static_path + "icones/icon_next_locked.png'>";
    }
}

function terminerMatch() {
    $.ajax({
        type: "POST",
        url: "/terminer_match",
        dataType: 'json'
    });
    window.location.href = "/observation"
}

function confirmAction() {
    if (window.confirm("Vous êtes sur le point de relancer un match et perdre toutes les données récupérées jusqu'à présent. Voulez-vous vraiment recommencer ?")) {
        if (window.confirm("Conserver les mêmes élèves ?")) {
            $.ajax({
                type: "POST",
                url: "/reset_match",
                data: {
                    e1: elv1.toString(),
                    e2: elv2.toString(),
                    e3: elv3.toString(),
                },
                dataType: 'json'
            });
            setTimeout(function (){
                window.location.href = "/observation_evaluation/" + elv1.toString() + "/" + elv2.toString() + "/" + elv3.toString() + "/";
            }, 100)

        } else {
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
}

function placer_pop_input(event) {
    let y = event.pageY;
    let x = event.pageX;
    let top = (y / body.offsetHeight) * 100 - 14
    let left = (x / body.offsetWidth) * 100 - 3

    pop_inputs.style.visibility = "visible";
    pop_inputs.style.top = top + "%";
    pop_inputs.style.left = left + "%";
}

function eraseBorders(){
    let all_td = document.getElementsByTagName('td');
    for (let i = 0; i < all_td.length; i++){
        all_td[i].style.borderColor = "white";
        all_td[i].style.borderStyle = "solid";
    }
}


try {
    $(document).ready(function () {
        $("td").click(function (event) {
            event.preventDefault()
            let score_a = document.getElementById("score_a");
            let score_b = document.getElementById("score_b");
            eraseBorders()
            let is_valid = false;
            if ((parseInt(score_a.innerText) < limite_score) && parseInt(score_b.innerText) < limite_score){
                if (cpt_tir == 0) {
                filet.style.pointerEvents = "none";
                document.getElementById('smash').style.visibility = "hidden";
                document.getElementById('end').style.visibility = "hidden";
                document.getElementById('refocus').style.visibility = "hidden";
                } else if (cpt_tir == 1) {
                    filet.style.pointerEvents = "auto";
                    document.getElementById('smash').style.visibility = "hidden";
                    document.getElementById('end').style.visibility = "visible";
                    document.getElementById('refocus').style.visibility = "visible";

                }else{
                     filet.style.pointerEvents = "auto";
                    document.getElementById('smash').style.visibility = "visible";
                    document.getElementById('end').style.visibility = "visible";
                    document.getElementById('refocus').style.visibility = "visible";
                }
                for (let i = 0; i < zones_a.length; i++) {
                     if (parseInt($(this).attr("id")) === zones_a[i] && (zone_precedente === "none" || zone_precedente === "B")) {
                         if (parseInt($(this).attr("id")) > 20 && cpt_tir == 0){
                             is_valid = false;
                             document.getElementById($(this).attr("id")).style.pointerEvents = "none";
                         } else {
                             is_valid = true;
                             document.getElementById($(this).attr("id")).style.pointerEvents = "auto";
                             court_a.style.pointerEvents = "none";
                             filet.style.pointerEvents = "auto";
                             court_b.style.pointerEvents = "auto";
                             document.getElementById($(this).attr("id")).style.borderColor = "black";
                             document.getElementById($(this).attr("id")).style.borderStyle = "solid";
                             placer_pop_input(event)
                             zone_precedente = "A";
                             cpt_tir++
                             break
                         }

                    } else if (parseInt($(this).attr("id")) === zones_b[i] && (zone_precedente === "none" || zone_precedente === "A")) {
                        if (parseInt($(this).attr("id")) > 120 && cpt_tir == 0){
                            is_valid = false;
                             document.getElementById($(this).attr("id")).style.pointerEvents = "none";

                        } else {
                            is_valid = true;
                            court_a.style.pointerEvents = "auto";
                            filet.style.pointerEvents = "auto";
                            court_b.style.pointerEvents = "none";
                            document.getElementById($(this).attr("id")).style.borderColor = "black";
                            document.getElementById($(this).attr("id")).style.borderStyle = "solid";
                            placer_pop_input(event)
                            zone_precedente = "B";
                            cpt_tir++
                            break
                        }
                    }
                }
            }

            if (is_valid) {
                $.ajax({
                type: "POST",
                url: "/observation_evaluation/" + elv1.toString() + "/" + elv2.toString() + "/" + elv3.toString() + "/",
                data: {
                    zone: $(this).attr("id"),
                },
                dataType: 'json'
            });
            last_tir_zone = $(this).attr("id");
            unlockResetButton(true);
            }

        });
    });

    $(document).ready(function () {
        $("#refocus").click(function (event) {
            eraseBorders()
            event.preventDefault()

            cpt_tir-=1;
            $.ajax({
                type: "POST",
                url: "/change_last_zone",
                data: {
                    action: $(this).attr("id"),
                    last_zone: parseInt(last_tir_zone),
                },
                dataType: 'json'
            });
            if (cpt_tir == 1){
                document.getElementById('smash').style.visibility = "hidden";
            } else{
                document.getElementById('smash').style.visibility = "visible";
            }
            document.getElementById('smash').style.visibility = "hidden";
            document.getElementById('end').style.visibility = "hidden";
            document.getElementById('refocus').style.visibility = "hidden";
            pop_inputs.style.visibility = "hidden";
            court_a.style.pointerEvents = "auto";
            court_b.style.pointerEvents = "auto";
            if (zone_precedente === "A") {
                zone_precedente = "B";
            } else if (zone_precedente === "B"){
                zone_precedente = "A"
            }

        });
    });

    $(document).ready(function () {
        $("#0").click(function (event) {
            eraseBorders()
            event.preventDefault()
            if (cpt_tir === 0){
                filet.style.pointerEvents = "none";
            }else{
                document.getElementById('smash').style.visibility = "visible";
                document.getElementById('end').style.visibility = "visible";
                document.getElementById('refocus').style.visibility = "visible";
                filet.style.pointerEvents = "auto";
                $.ajax({
                type: "POST",
                url: "/observation_evaluation/" + elv1.toString() + "/" + elv2.toString() + "/" + elv3.toString() + "/",
                data: {
                    zone: $(this).attr("id"),
                },
                dataType: 'json'
            });
            cpt_tir++;
            last_tir_zone = $(this).attr("id");
            unlockResetButton(true);
            court_a.style.pointerEvents = "none";
            court_b.style.pointerEvents = "none";
            placer_pop_input(event)
            zone_precedente = "none";
            }

        });
    });

    $(document).ready(function () {
        $("#end").click(function (event) {
            eraseBorders()
            document.getElementById('smash').style.visibility = "hidden";
            document.getElementById('end').style.visibility = "hidden";
            document.getElementById('refocus').style.visibility = "hidden";
            $.ajax({
                type: "POST",
                url: "/end_echange",
                data: {
                    action: $(this).attr("id"),
                    last_zone: parseInt(last_tir_zone),
                },
                dataType: 'json'
            });
            pop_inputs.style.visibility = "hidden";
            court_a.style.pointerEvents = "auto";
            court_b.style.pointerEvents = "auto";
            zone_precedente = "none";
            cpt_tir = 0;
            setTimeout(function (){
                $("#dernier_echange").load('/load_echange');
                document.getElementById('echange_supprimer').style.visibility = 'visible'
                let premier_echange;
                let echange;
                if (document.getElementById('ech_id') === null){
                    premier_echange = document.getElementById('premier_echange')
                    $("#banner").load('/load_score/' + premier_echange.value);
                } else {
                    echange = document.getElementById('ech_id')
                    echange.value++;

                $("#banner").load('/load_score/' + echange.value);
                }
            }, 100);
            setTimeout(function (){
                let score_a = document.getElementById("score_a");
                let score_b = document.getElementById("score_b");
                console.log("A:" + parseInt(score_a.innerText))
                console.log("B:" + parseInt(score_b.innerText))
                console.log("Limite:" + limite_score)
                if (parseInt(score_a.innerText) >= limite_score || parseInt(score_b.innerText) >= limite_score){
                    court_a.style.pointerEvents = "none";
                    court_b.style.pointerEvents = "none";
                    filet.style.pointerEvents = "none";
                    unlockNextButton(true);
               }

            }, 2000)


        });
    });

    $(document).ready(function () {
        $("#smash").click(function (event) {
            eraseBorders()
            event.preventDefault()
            document.getElementById('smash').style.visibility = "hidden";
            document.getElementById('end').style.visibility = "hidden";
            document.getElementById('refocus').style.visibility = "hidden";

            $.ajax({
                type: "POST",
                url: "/end_echange",
                data: {
                    action: $(this).attr("id"),
                    last_zone: parseInt(last_tir_zone),
                },
                dataType: 'json'
            });
            pop_inputs.style.visibility = "hidden";
            court_a.style.pointerEvents = "auto";
            court_b.style.pointerEvents = "auto";
            zone_precedente = "none";
            cpt_tir = 0
            setTimeout(function (){
                $("#dernier_echange").load('/load_echange');
                document.getElementById('echange_supprimer').style.visibility = 'visible'
                let premier_echange;
                let echange;
                if (document.getElementById('ech_id') === null){
                    premier_echange = document.getElementById('premier_echange')
                    $("#banner").load('/load_score/' + premier_echange.value);
                } else {
                    echange = document.getElementById('ech_id')
                    echange.value++;
                    }
                    $("#banner").load('/load_score/' + echange.value);
            }, 100)

            setTimeout(function (){
                let score_a = document.getElementById("score_a");
                let score_b = document.getElementById("score_b");
                console.log("A:" + parseInt(score_a.innerText))
                console.log("B:" + parseInt(score_b.innerText))
                console.log("Limite:" + limite_score)
                if (parseInt(score_a.innerText) >= limite_score || parseInt(score_b.innerText) >= limite_score){
                    court_a.style.pointerEvents = "none";
                    court_b.style.pointerEvents = "none";
                    filet.style.pointerEvents = "none";
                    unlockNextButton(true);
               }

            }, 2000)

        });
    });

    $(document).ready(function () {
        $(document).on('submit','#form_echange',function (e){
            e.preventDefault();
            let ech_id = document.getElementById('ech_id')
            $.ajax({
               type: "POST",
                url: "/modifier_echange/" + ech_id.value,
                data: {
                    smash_gagnant: $('#ech_smashGagnant').val()
                },
                dataType: 'json'
            });
        })
    });

} catch (error) {
    console.log(error);
}






