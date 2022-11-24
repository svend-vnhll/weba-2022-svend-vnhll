from django.core.exceptions import ValidationError
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from recap_match.logic import *
from recap_match.models import *
from django.template.loader import render_to_string
from django.contrib import messages
from templates.forms import *

DAYS = {'LUNDI': 1, 'MARDI': 2, 'MERCREDI': 3, 'JEUDI': 4, 'VENDREDI': 5}


def login(request):
    try:
        del request.session['id_admin']
    except KeyError:
        pass
    try:
        del request.session['id_cours']
    except KeyError:
        pass
    context = {'form_login': FrmLogin()}
    if request.method == "POST":
        form = FrmLogin(request.POST)
        if form.is_valid():
            if (Administrateur.objects.filter(adm_nom=request.POST.get('adm_nom')).count()) == 0:
                messages.info(request, "Identifiant ou mot de passe incorrect !")
                return redirect(login)
            elif check_password(request.POST.get('adm_mdp'),
                                Administrateur.objects.get(adm_nom=request.POST.get('adm_nom')).adm_mdp):
                request.session['id_admin'] = Administrateur.objects.get(adm_nom=request.POST.get('adm_nom')).id
                request.session['id_cours'] = 1
                return redirect(recap)
            else:
                messages.info(request, "Identifiant ou mot de passe incorrect !")
                return redirect(login)
        else:
            messages.info(request, "Erreur dans les inputs.")
            return redirect('login')
    else:
        return render(request, 'login.html', context)


def signin(request):
    # if request.session.get('id_admin', False):
    context = {'form_signin': FrmSignin()}
    if request.method == "POST":
        form = FrmSignin(request.POST)
        if form.is_valid():
            if (Administrateur.objects.filter(adm_nom__contains=request.POST.get('adm_nom')).count()) > 0:
                messages.info(request, "Ce nom est déjà pris !")
                return redirect(signin)
            else:
                admin = Administrateur()

                admin.adm_nom = form.cleaned_data['adm_nom']
                admin.adm_prenom = form.cleaned_data['adm_prenom']
                admin.adm_email = form.cleaned_data['adm_email']
                admin.adm_mdp = make_password(form.cleaned_data['adm_mdp'])

                admin.save()
                messages.info(request, "Nouvel admin créé !")
                return redirect(login)
    else:
        return render(request, 'signin.html', context)
    # else:
    #    return redirect(login)


def recap(request):
    matchs_cours = Match.objects.filter(mat_cours_id=request.session.get('id_cours'))
    if request.method == "POST":
        if request.POST.get('input') != "" and request.POST.get('input') is not None:
            if not verifie_chiffre(request.POST.get('input')):
                cours = Cours.objects.get(id=int(request.session.get('id_cours')))
                name = request.POST.get('input')
                if not cours.doublon_eleve(name):
                    eleve = Eleve.objects.get(id=int(request.POST.get('eleve')))
                    eleve.ele_nom = request.POST.get('input')
                    eleve.save()
                else:
                    return redirect(recap)

    all_eleves_cours = Eleve.objects.filter(ele_cours_id=request.session.get('id_cours')).order_by(
        'ele_nom').exclude(ele_nom="Elève")
    context = {'eleves': all_eleves_cours,
               'matchs': matchs_cours}
    return render(request, 'recap_eleves.html', context)


def recap_updating(request, id_eleve):
    matchs_cours = Match.objects.filter(mat_cours_id=request.session.get('id_cours'))
    all_eleves_cours = Eleve.objects.filter(ele_cours_id=request.session.get('id_cours')).order_by('ele_nom').exclude(
        ele_nom="Elève")

    context = {'eleves': all_eleves_cours,
               'matchs': matchs_cours,
               'updating': Eleve.objects.get(id=id_eleve)}
    return render(request, 'recap_eleves.html', context)


def delete_eleve(request, id_eleve):
    Eleve.objects.get(id=int(id_eleve)).delete_eleve()
    return redirect(recap)


def load_matchs(request, id_eleve):
    all_matchs = Match.objects.filter(mat_cours_id=request.session.get('id_cours'))
    eleve = Eleve.objects.get(id=int(id_eleve))
    context = {'all_matchs': all_matchs, 'id_eleve': int(id_eleve), 'eleve': eleve}
    rendered = render_to_string('div_matchs_eleves.html', context)
    return HttpResponse(rendered)


def load_echanges_match(request, id_eleve, id_match):
    match = Match.objects.get(id=int(id_match))
    all_echanges = Echange.objects.filter(ech_match_id=match.id).exclude(ech_zoneFinale=None)
    all_tirs = Tir.objects.filter(tir_echange__ech_match=match.id)
    if match.mat_eleA == Eleve.objects.get(id=int(id_eleve)):
        elvA = Eleve.objects.get(id=int(id_eleve))
        elvB = Eleve.objects.get(id=match.mat_eleB.id)
        target = "A"
    else:
        elvA = Eleve.objects.get(id=match.mat_eleA.id)
        elvB = Eleve.objects.get(id=int(id_eleve))
        target = "B"
    context = {'target': target, 'match': match, 'all_echanges': all_echanges, 'all_tirs': all_tirs, 'elvA': elvA,
               'elvB': elvB}
    rendered = render_to_string('div_echanges_match.html', context)
    return HttpResponse(rendered)


def load_infos_match(request, id_eleve, id_match):
    cpt_smashs = Match.objects.get(id=id_match).count_smashs_elv(id_eleve)
    cpt_faults = Match.objects.get(id=id_match).count_faults_elv(id_eleve)
    cpt_zd = Match.objects.get(id=id_match).count_points_zd_elv(id_eleve)
    context = {'smashs': cpt_smashs,
               'faults': cpt_faults,
               'zd': cpt_zd,
               'id_eleve': id_eleve,
               'id_match': id_match}
    rendered = render_to_string('div_infos_match.html', context)
    return HttpResponse(rendered)


def delete_player(request):
    if request.method == "POST":
        id_elv = request.POST.get('id_elv')
        match = Match.objects.get(id=request.POST.get('id_match'))
        if match.mat_eleA.id == int(id_elv):
            match.mat_eleA = Eleve.objects.get(ele_nom="Elève")
            match.save()
        elif match.mat_eleB.id == int(id_elv):
            match.mat_eleB = Eleve.objects.get(ele_nom="Elève")
            match.save()
        if match.mat_eleA.ele_nom == "Elève" and match.mat_eleB.ele_nom == "Elève":
            match.delete()
    return redirect(recap)
