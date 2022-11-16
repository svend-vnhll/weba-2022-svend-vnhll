from django.forms import ModelForm, PasswordInput
from recap_match.models import *


class FrmLogin(ModelForm):
    class Meta:
        model = Administrateur
        fields = ['adm_nom', 'adm_mdp']
        labels = {
            'adm_nom': 'Nom',
            'adm_mdp': 'Mot de passe'
        }
        widgets = {
            'adm_mdp': PasswordInput()
        }


class FrmSignin(ModelForm):
    class Meta:
        model = Administrateur
        fields = ['adm_nom', 'adm_prenom', 'adm_email', 'adm_mdp']
        labels = {
            'adm_nom': 'Nom',
            'adm_prenom': 'Prénom',
            'adm_email': 'E-mail',
            'adm_mdp': 'Mot de passe'
        }
        widgets = {
            'adm_mdp': PasswordInput()
        }


class FrmCours(ModelForm):
    class Meta:
        model = Cours
        fields = ['cou_classe', 'cou_jour', 'cou_horaireDeb', 'cou_horaireFin', 'cou_semestre', 'cou_annee']
        labels = {
            'cou_classe': 'Classe',
            'cou_jour': 'Jour',
            'cou_horaireDeb': 'Horaire Début',
            'cou_horaireFin': 'Horaire Fin',
            'cou_semestre': 'Semestre',
            'cou_annee': 'Volée'
        }


class FrmEleve(ModelForm):
    class Meta:
        model = Eleve
        fields = ['ele_nom']
        labels = {
            'ele_nom': 'Pseudonyme'
        }


class FrmEchange(ModelForm):

    class Meta:
        model = Echange
        fields = ['ech_smashGagnant']
        labels = {
            'ech_smashGagnant': 'Smash'
        }


class FrmGrille(ModelForm):
    class Meta:
        model = Grille
        fields = ['gri_pointSimple', 'gri_zoneDangereuse', 'gri_smash']
        labels = {
            'gri_pointSimple': 'Simple',
            'gri_zoneDangereuse': 'Zone dangereuses',
            'gri_smash': 'Smash'
        }



