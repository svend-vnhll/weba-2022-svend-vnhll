# Generated by Django 4.1.3 on 2022-11-10 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adm_nom', models.CharField(max_length=32)),
                ('adm_prenom', models.CharField(max_length=32)),
                ('adm_email', models.EmailField(max_length=32)),
                ('adm_mdp', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cou_classe', models.CharField(max_length=32)),
                ('cou_jour', models.CharField(choices=[('LUNDI', 'LUNDI'), ('MARDI', 'MARDI'), ('MERCREDI', 'MERCREDI'), ('JEUDI', 'JEUDI'), ('VENDREDI', 'VENDREDI')], max_length=8)),
                ('cou_horaireDeb', models.DecimalField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], decimal_places=0, max_digits=2)),
                ('cou_horaireFin', models.DecimalField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], decimal_places=0, max_digits=2)),
                ('cou_semestre', models.DecimalField(choices=[(1, 1), (2, 2)], decimal_places=0, max_digits=1)),
                ('cou_annee', models.DecimalField(choices=[(2223, 2223), (2324, 2324), (2425, 2425), (2526, 2526), (2627, 2627), (2728, 2728), (2829, 2829), (2930, 2930)], decimal_places=0, max_digits=4)),
                ('cou_admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recap_match.administrateur')),
            ],
        ),
        migrations.CreateModel(
            name='Echange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ech_sequence', models.DecimalField(decimal_places=0, max_digits=4)),
                ('ech_zoneFinale', models.DecimalField(decimal_places=0, max_digits=3, null=True)),
                ('ech_smashGagnant', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Eleve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ele_nom', models.CharField(max_length=16)),
                ('ele_cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recap_match.cours')),
            ],
        ),
        migrations.CreateModel(
            name='Tir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tir_sequence', models.DecimalField(decimal_places=0, max_digits=5)),
                ('tir_zoneDepart', models.DecimalField(decimal_places=0, max_digits=3)),
                ('tir_echange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recap_match.echange')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mat_ptsEleA', models.DecimalField(decimal_places=0, default=0, max_digits=2, null=True)),
                ('mat_ptsEleB', models.DecimalField(decimal_places=0, default=0, max_digits=2, null=True)),
                ('mat_noteEleA', models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True)),
                ('mat_noteEleB', models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True)),
                ('mat_cours', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recap_match.cours')),
                ('mat_eleA', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eleveA', to='recap_match.eleve')),
                ('mat_eleB', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eleveB', to='recap_match.eleve')),
                ('mat_obs', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='observateur', to='recap_match.eleve')),
            ],
        ),
        migrations.CreateModel(
            name='Grille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gri_zoneDangereuse', models.DecimalField(decimal_places=0, max_digits=1)),
                ('gri_pointSimple', models.DecimalField(decimal_places=0, max_digits=1)),
                ('gri_smash', models.DecimalField(decimal_places=0, max_digits=1)),
                ('gri_cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recap_match.cours')),
            ],
        ),
        migrations.AddField(
            model_name='echange',
            name='ech_eleve',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recap_match.eleve'),
        ),
        migrations.AddField(
            model_name='echange',
            name='ech_match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recap_match.match'),
        ),
        migrations.AddConstraint(
            model_name='echange',
            constraint=models.CheckConstraint(check=models.Q(('ech_sequence__gt', 0), ('ech_sequence__lt', 100)), name='ck_ech_sequence'),
        ),
        migrations.AlterUniqueTogether(
            name='cours',
            unique_together={('cou_classe', 'cou_jour', 'cou_horaireDeb', 'cou_horaireFin', 'cou_semestre', 'cou_annee')},
        ),
    ]
