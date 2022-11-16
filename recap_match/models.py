from django.db import models
from django.conf import settings
from django.db.models import Q
from recap_match.logic import *

static_url = settings.STATIC_URL
LISTE_VOLEES = [(2223, 2223), (2324, 2324), (2425, 2425),
                (2526, 2526), (2627, 2627), (2728, 2728),
                (2829, 2829), (2930, 2930)]
SEMESTRES = [(1, 1), (2, 2)]
JOURS_SEMAINE = [('LUNDI', 'LUNDI'), ('MARDI', 'MARDI'), ('MERCREDI', 'MERCREDI'),
                 ('JEUDI', 'JEUDI'), ('VENDREDI', 'VENDREDI')]
HORAIRES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
            (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)]


class Administrateur(models.Model):
    adm_nom = models.CharField(max_length=32, null=False)
    adm_prenom = models.CharField(max_length=32, null=False)
    adm_email = models.EmailField(max_length=32, null=False)
    adm_mdp = models.CharField(max_length=128, null=False)

    def has_cours(self, selected):
        all_cours = Cours.objects.filter(cou_admin=self)
        for cours in all_cours:
            if (cours.cou_classe == selected.cou_classe and
                cours.cou_jour == selected.cou_jour and
                cours.cou_horaireDeb == selected.cou_horaireDeb and
                cours.cou_horaireFin == selected.cou_horaireFin and
                cours.cou_semestre == selected.cou_semestre and
                cours.cou_annee == selected.cou_annee) or \
                    (cours.cou_jour == selected.cou_jour and
                     cours.cou_horaireDeb == selected.cou_horaireDeb and
                     cours.cou_horaireFin == selected.cou_horaireFin and
                     cours.cou_semestre == selected.cou_semestre and
                     cours.cou_annee == selected.cou_annee):
                return True
        return False


class Cours(models.Model):
    cou_classe = models.CharField(max_length=32, null=False)
    cou_jour = models.CharField(max_length=8, null=False, choices=JOURS_SEMAINE)
    cou_horaireDeb = models.DecimalField(max_digits=2, decimal_places=0, null=False, choices=HORAIRES)
    cou_horaireFin = models.DecimalField(max_digits=2, decimal_places=0, null=False, choices=HORAIRES)
    cou_semestre = models.DecimalField(max_digits=1, decimal_places=0, null=False, choices=SEMESTRES)
    cou_annee = models.DecimalField(max_digits=4, decimal_places=0, null=False, choices=LISTE_VOLEES)

    cou_admin = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('cou_classe', 'cou_jour', 'cou_horaireDeb', 'cou_horaireFin', 'cou_semestre', 'cou_annee')

    def get_valeur_grille_zone(self, no_zone):
        grille = Grille.objects.get(gri_cours=self)
        if (1 <= no_zone <= 3) or (101 <= no_zone <= 103):
            res = ['zd', grille.gri_zoneDangereuse]
            return res
        elif (11 <= no_zone <= 12) or (111 <= no_zone <= 112):
            res = ['zn', grille.gri_pointSimple]
            return res
        elif (21 <= no_zone <= 27) or (121 <= no_zone <= 127):
            res = ['out', grille.gri_pointSimple]
            return res

    def doublon_eleve(self, nom_input):
        eleves = Eleve.objects.filter(ele_cours=self)
        for eleve in eleves:
            if eleve.ele_nom.upper() == nom_input.upper():
                return True
        return False


class Grille(models.Model):
    gri_zoneDangereuse = models.DecimalField(max_digits=1, decimal_places=0)
    gri_pointSimple = models.DecimalField(max_digits=1, decimal_places=0)
    gri_smash = models.DecimalField(max_digits=1, decimal_places=0)
    gri_cours = models.ForeignKey(Cours, on_delete=models.CASCADE, null=False)

    def points_totaux(self):
        return 5 * (self.gri_zoneDangereuse + self.gri_smash)


class Eleve(models.Model):
    ele_nom = models.CharField(max_length=16, null=False)

    ele_cours = models.ForeignKey(Cours, on_delete=models.CASCADE, null=False)

    def __str__(self):
        nom = self.ele_nom
        return nom

    def get_moyenne_notes(self):
        matchs = Match.objects.filter(mat_cours=self.ele_cours)
        moyenne = 0
        cpt = 0
        for match in matchs:
            if match.mat_eleA == self:
                moyenne = moyenne + match.mat_noteEleA
                cpt += 1
            elif match.mat_eleB == self:
                moyenne = moyenne + match.mat_noteEleB
                cpt += 1
        if cpt == 0:
            return 1
        else:
            return moyenne / cpt

    def delete_eleve(self):
        matchs = Match.objects.filter(mat_cours=self.ele_cours)
        for match in matchs:
            if match.mat_eleA == self:
                match.mat_eleA = Eleve.objects.get(ele_nom="Elève")
                match.save()
            elif match.mat_eleB == self:
                match.mat_eleB = Eleve.objects.get(ele_nom="Elève")
                match.save()
        self.delete()


class Match(models.Model):
    mat_ptsEleA = models.DecimalField(max_digits=2, decimal_places=0, null=True, default=0)
    mat_ptsEleB = models.DecimalField(max_digits=2, decimal_places=0, null=True, default=0)
    mat_noteEleA = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=0)
    mat_noteEleB = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=0)

    mat_eleA = models.ForeignKey(Eleve, on_delete=models.SET_NULL, related_name='eleveA', null=True)
    mat_eleB = models.ForeignKey(Eleve, on_delete=models.SET_NULL, related_name='eleveB', null=True)
    mat_obs = models.ForeignKey(Eleve, on_delete=models.SET_NULL, related_name='observateur', null=True)
    mat_cours = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True)

    def initialiser(self, e1, e2, e3):
        self.mat_eleA = e1
        self.mat_obs = e2
        self.mat_eleB = e3
        self.save()

    def count_smashs_elv(self, id_eleve):
        echanges = Echange.objects.filter(ech_match=self)
        compteur = 0
        for echange in echanges:
            if self.mat_eleA.id == int(id_eleve) and (Tir.objects.filter(tir_echange=echange).count() > 2):
                if echange.ech_smashGagnant and \
                        (echange.ech_zoneFinale == 101 or
                         echange.ech_zoneFinale == 102 or
                         echange.ech_zoneFinale == 103 or
                         echange.ech_zoneFinale == 111 or
                         echange.ech_zoneFinale == 112):
                    compteur += 1
            elif self.mat_eleB.id == int(id_eleve) and (Tir.objects.filter(tir_echange=echange).count() > 2):
                if echange.ech_smashGagnant and \
                        (echange.ech_zoneFinale == 1 or
                         echange.ech_zoneFinale == 2 or
                         echange.ech_zoneFinale == 3 or
                         echange.ech_zoneFinale == 11 or
                         echange.ech_zoneFinale == 12):
                    compteur += 1
        return compteur

    def count_faults_elv(self, id_eleve):
        echanges = Echange.objects.filter(ech_match=self)
        compteur = 0
        for echange in echanges:
            tot_tirs = Tir.objects.filter(tir_echange=echange).count()
            seq_avt_dern_tir = tot_tirs - 1
            if self.mat_eleA.id == int(id_eleve):
                if echange.type_fin() == "faut_serv_A" or echange.type_fin() == "out_A" or echange.type_fin() == "filet_A":
                    compteur += 1
            elif self.mat_eleB.id == int(id_eleve):
                if echange.type_fin() == "faut_serv_B" or echange.type_fin() == "out_B" or echange.type_fin() == "filet_B":
                    compteur += 1
        return compteur

    def count_points_zd_elv(self, id_eleve):
        echanges = Echange.objects.filter(ech_match=self)
        compteur = 0
        for echange in echanges:
            if self.mat_eleA.id == int(id_eleve) and (Tir.objects.filter(tir_echange=echange).count() > 2):
                if 101 <= echange.ech_zoneFinale <= 103:
                    compteur += 1
            elif self.mat_eleB.id == int(id_eleve) and (Tir.objects.filter(tir_echange=echange).count() > 2):
                if 1 <= echange.ech_zoneFinale <= 3:
                    compteur += 1
        return compteur

    def get_first_echange(self):
        return Echange.objects.filter(ech_match=self).first()

    def get_final_echange(self):
        return Echange.objects.filter(ech_match=self).latest('ech_sequence')


class Echange(models.Model):
    ech_sequence = models.DecimalField(max_digits=4, decimal_places=0)
    ech_zoneFinale = models.DecimalField(max_digits=3, decimal_places=0, null=True)
    ech_smashGagnant = models.BooleanField(null=True)

    ech_match = models.ForeignKey(Match, on_delete=models.CASCADE)
    ech_eleve = models.ForeignKey(Eleve, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(ech_sequence__gt=0) & Q(ech_sequence__lt=100), name='ck_ech_sequence')
        ]

    def type_fin(self):
        if Tir.objects.filter(tir_echange=self).count() == 2 and \
                ((1 <= self.ech_zoneFinale <= 3) or (101 <= self.ech_zoneFinale <= 103) or
                 (11 <= self.ech_zoneFinale <= 12) or (111 <= self.ech_zoneFinale <= 112)):
            if (self.ech_zoneFinale == 2 or self.ech_zoneFinale == 11) and \
                    (self.get_avant_dernier_tir().tir_zoneDepart != 112 and
                     self.get_avant_dernier_tir().tir_zoneDepart != 103):
                return "faut_serv_B"
            elif (self.ech_zoneFinale == 3 or self.ech_zoneFinale == 12) and \
                    (self.get_avant_dernier_tir().tir_zoneDepart != 111 and
                     self.get_avant_dernier_tir().tir_zoneDepart != 102):
                return "faut_serv_B"
            elif (self.ech_zoneFinale == 102 or self.ech_zoneFinale == 111) and \
                    (self.get_avant_dernier_tir().tir_zoneDepart != 12 and
                     self.get_avant_dernier_tir().tir_zoneDepart != 3):
                return "faut_serv_A"
            elif (self.ech_zoneFinale == 103 or self.ech_zoneFinale == 112) and \
                    (self.get_avant_dernier_tir().tir_zoneDepart != 11 and
                     self.get_avant_dernier_tir().tir_zoneDepart != 2):
                return "faut_serv_A"
            elif self.ech_zoneFinale == 101:
                return "faut_serv_A"
            elif self.ech_zoneFinale == 1:
                return "faut_serv_B"
            elif (1 <= self.ech_zoneFinale <= 3) or (101 <= self.ech_zoneFinale <= 103):
                if (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "A":
                    return "zd_A"
                elif (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "B":
                    return "zd_B"
            elif (11 <= self.ech_zoneFinale <= 12) or (111 <= self.ech_zoneFinale <= 112):
                if (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "A":
                    return "point_A"
                elif (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "B":
                    return "point_B"
        elif (121 <= self.ech_zoneFinale <= 127) or (21 <= self.ech_zoneFinale <= 27):
            if (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "A":
                return "out_A"
            elif (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "B":
                return "out_B"
        elif self.ech_zoneFinale == 0:
            if (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "A":
                return "filet_A"
            elif (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "B":
                return "filet_B"
        elif (1 <= self.ech_zoneFinale <= 3) or (101 <= self.ech_zoneFinale <= 103):
            if (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "A":
                return "zd_A"
            elif (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "B":
                return "zd_B"
        elif (11 <= self.ech_zoneFinale <= 12) or (111 <= self.ech_zoneFinale <= 112):
            if (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "A":
                return "point_A"
            elif (get_player_zone(self.get_avant_dernier_tir().tir_zoneDepart)) == "B":
                return "point_B"

    def get_avant_dernier_tir(self):
        return Tir.objects.get(tir_sequence=(Tir.objects.filter(tir_echange=self).latest('id').tir_sequence - 1),
                               tir_echange=self)

    def get_current_score(self):
        if self.ech_zoneFinale is None:
            all_previous_ech = Echange.objects.filter(ech_match=self.ech_match, ech_sequence__lt=self.ech_sequence)
        else:
            all_previous_ech = Echange.objects.filter(ech_match=self.ech_match, ech_sequence__lt=self.ech_sequence + 1)

        scoreA = 0
        scoreB = 0
        for echange in all_previous_ech:
            if echange.type_fin() == "out_A":
                # print("out_A")
                scoreB += 1
            elif echange.type_fin() == "out_B":
                # print("out_B")
                scoreA += 1
            elif echange.type_fin() == "faut_serv_A":
                # print("faut_serv_A")
                scoreB += 1
            elif echange.type_fin() == "faut_serv_B":
                # print("faut_serv_B")
                scoreA += 1
            elif echange.type_fin() == "filet_A":
                # print("filet_A")
                scoreB += 1
            elif echange.type_fin() == "filet_B":
                # print("filet_B")
                scoreA += 1
            elif echange.type_fin() == "zd_A":
                # print("zd_A")
                scoreA += 1
            elif echange.type_fin() == "zd_B":
                # print("zd_B")
                scoreB += 1
            elif echange.type_fin() == "point_A":
                # print("point_A")
                scoreA += 1
            elif echange.type_fin() == "point_B":
                # print("point_B")
                scoreB += 1
        return str(scoreA) + " - " + str(scoreB)

    def count_tir(self):
        tirs = Tir.objects.filter(tir_echange=self).count()
        return tirs


class Tir(models.Model):
    tir_sequence = models.DecimalField(max_digits=5, decimal_places=0)
    tir_zoneDepart = models.DecimalField(max_digits=3, decimal_places=0)
    tir_echange = models.ForeignKey(Echange, on_delete=models.CASCADE)

    def suivant(self, seq, zndep, echange):
        self.tir_sequence = seq
        self.tir_zoneDepart = zndep
        self.tir_echange = echange
        self.save()
