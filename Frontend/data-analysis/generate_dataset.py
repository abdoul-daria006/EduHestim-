"""
╔══════════════════════════════════════════════════════════════╗
║         EduHestim — Générateur de Dataset Faker              ║
║   Thème : Analyse de Données pour la Gestion des EDT         ║
║   Entités : Salles, Réservations, Enseignants, Étudiants,    ║
║             Emplois du Temps, Conflits, Modifications         ║
╚══════════════════════════════════════════════════════════════╝

Installation :
    pip install faker pandas openpyxl numpy

Usage :
    python generate_dataset.py
    
Sortie :
    eduhestim_dataset.xlsx  (9 feuilles)
    csv/                    (9 fichiers CSV)
"""

from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

fake = Faker('fr_FR')
random.seed(42)
Faker.seed(42)
np.random.seed(42)

# ============================================================
# CONFIGURATION
# ============================================================
NB_SALLES        = 25
NB_ENSEIGNANTS   = 40
NB_ETUDIANTS     = 250
NB_CLASSES       = 12
NB_MODULES       = 20
NB_EDT_ENTREES   = 600
NB_RESERVATIONS  = 800
NB_CONFLITS      = 80
NB_MODIFICATIONS = 150

ANNEE_DEBUT = datetime(2024, 9, 16)
ANNEE_FIN   = datetime(2025, 6, 30)

# ============================================================
# REFERENTIELS
# ============================================================
JOURS_SEMAINE = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
CRENEAUX = [
    ('08:00', '10:00'),
    ('10:15', '12:15'),
    ('14:00', '16:00'),
    ('16:15', '18:15'),
]
FILIERES      = ['Informatique', 'Management', 'Mathematiques', 'Physique', 'Langues', 'Droit']
NIVEAUX       = ['L1', 'L2', 'L3', 'M1', 'M2']
TYPES_SALLE   = ['Normale', 'Informatique', 'Amphitheatre', 'Laboratoire']
BATIMENTS     = ['Batiment A', 'Batiment B', 'Batiment C', 'Batiment D']
TYPES_COURS   = ['CM', 'TD', 'TP']
DEPARTEMENTS  = ['Informatique', 'Mathematiques', 'Physique', 'Management', 'Langues', 'Droit']
NOMS_MODULES  = [
    'Algorithmique', 'Bases de donnees', 'Reseaux informatiques', 'Developpement web',
    'Intelligence artificielle', 'Machine Learning', 'Systemes exploitation',
    'Programmation Python', 'Analyse mathematique', 'Algebre lineaire',
    'Statistiques appliquees', 'Physique quantique', 'Management de projet',
    'Anglais professionnel', 'Droit commercial', 'Comptabilite', 'Marketing digital',
    'Cybersecurite', 'Cloud Computing', 'Data Science'
]
STATUTS_DEMANDE = ['en_attente', 'approuve', 'refuse']
MOTIFS_MODIF = [
    'Report pour jour ferie', 'Annulation enseignant absent',
    'Changement de salle', 'Decalage horaire', 'Cours rattrapage',
    'Modification emploi du temps', 'Salle indisponible', 'Evenement exceptionnel'
]
TYPES_CONFLIT = [
    'Double reservation salle', 'Conflit horaire enseignant',
    'Salle indisponible', 'Chevauchement de creneaux', 'Capacite insuffisante',
]

def rand_date():
    delta = ANNEE_FIN - ANNEE_DEBUT
    return ANNEE_DEBUT + timedelta(days=random.randint(0, delta.days))

def rand_weekday():
    d = rand_date()
    while d.weekday() >= 5:
        d = rand_date()
    return d

# ============================================================
# 1. SALLES
# ============================================================
print("Generating salles...")
cap_par_type = {
    'Normale':      [30, 35, 40],
    'Informatique': [20, 25, 30],
    'Amphitheatre': [100, 150, 200, 250],
    'Laboratoire':  [15, 20, 25],
}

salles = []
for i in range(1, NB_SALLES + 1):
    t = random.choice(TYPES_SALLE)
    salles.append({
        'ID_Salle':       f'S{i:03d}',
        'Nom_Salle':      f'{t[:4]}-{i:02d}',
        'Batiment':       random.choice(BATIMENTS),
        'Type_Salle':     t,
        'Capacite':       random.choice(cap_par_type[t]),
        'Disponible':     random.choices([True, False], weights=[85, 15])[0],
        'Nb_Reservations':0,
        'Taux_Occupation':0.0,
    })

df_salles = pd.DataFrame(salles)
salles_ids = df_salles['ID_Salle'].tolist()

# ============================================================
# 2. ENSEIGNANTS
# ============================================================
print("Generating enseignants...")
grades = ['Professeur', 'Maitre de conferences', 'Assistant', 'Vacataire']

enseignants = []
for i in range(1, NB_ENSEIGNANTS + 1):
    enseignants.append({
        'ID_Enseignant':         f'ENS{i:03d}',
        'Nom':                   fake.last_name(),
        'Prenom':                fake.first_name(),
        'Email':                 fake.email(),
        'Telephone':             fake.phone_number(),
        'Grade':                 random.choice(grades),
        'Departement':           random.choice(DEPARTEMENTS),
        'Annees_Experience':     random.randint(1, 30),
        'Date_Embauche':         fake.date_between(start_date='-20y', end_date='-1y').strftime('%Y-%m-%d'),
        'Volume_Horaire_Hebdo':  random.choice([6, 8, 10, 12, 14, 16, 18]),
        'Nb_Cours_Assignes':     0,
        'Volume_Horaire_Total':  0,
    })

df_enseignants = pd.DataFrame(enseignants)
ens_ids  = df_enseignants['ID_Enseignant'].tolist()
ens_noms = {r['ID_Enseignant']: f"{r['Prenom']} {r['Nom']}" for _, r in df_enseignants.iterrows()}

# ============================================================
# 3. CLASSES
# ============================================================
print("Generating classes...")
classes = []
for i in range(1, NB_CLASSES + 1):
    f = random.choice(FILIERES)
    n = random.choice(NIVEAUX)
    classes.append({
        'ID_Classe':             f'CL{i:02d}',
        'Nom_Classe':            f'{f[:3].upper()}-{n}',
        'Filiere':               f,
        'Niveau':                n,
        'Annee_Scolaire':        '2024-2025',
        'Nb_Etudiants_Max':      random.choice([25, 30, 35, 40]),
        'Nb_Etudiants_Inscrits': 0,
    })

df_classes = pd.DataFrame(classes)
classes_ids = df_classes['ID_Classe'].tolist()
classes_list = classes

# ============================================================
# 4. ETUDIANTS
# ============================================================
print("Generating etudiants...")
statuts_etu = ['Actif', 'Suspendu', 'Diplome', 'Abandonne']
classe_count = {cid: 0 for cid in classes_ids}

etudiants = []
for i in range(1, NB_ETUDIANTS + 1):
    cl = random.choice(classes_list)
    cid = cl['ID_Classe']
    classe_count[cid] += 1
    etudiants.append({
        'ID_Etudiant':      f'ET{i:04d}',
        'Nom':              fake.last_name(),
        'Prenom':           fake.first_name(),
        'Email':            fake.email(),
        'Telephone':        fake.phone_number(),
        'Date_Naissance':   fake.date_of_birth(minimum_age=18, maximum_age=28).strftime('%Y-%m-%d'),
        'ID_Classe':        cid,
        'Filiere':          cl['Filiere'],
        'Niveau':           cl['Niveau'],
        'Statut':           random.choices(statuts_etu, weights=[80, 5, 10, 5])[0],
        'Date_Inscription': fake.date_between(start_date='-4y', end_date='-1m').strftime('%Y-%m-%d'),
        'Boursier':         random.choice([True, False]),
        'Taux_Absence':     round(max(0, min(100, random.gauss(20, 10))), 1),
    })

for cid, nb in classe_count.items():
    df_classes.loc[df_classes['ID_Classe'] == cid, 'Nb_Etudiants_Inscrits'] = nb

df_etudiants = pd.DataFrame(etudiants)
etu_ids = df_etudiants['ID_Etudiant'].tolist()

# ============================================================
# 5. MODULES
# ============================================================
print("Generating modules...")
modules_list = []
for i, nom in enumerate(NOMS_MODULES[:NB_MODULES], 1):
    eid = random.choice(ens_ids)
    modules_list.append({
        'ID_Module':      f'MOD{i:03d}',
        'Nom_Module':     nom,
        'ID_Enseignant':  eid,
        'Nom_Enseignant': ens_noms[eid],
        'ID_Classe':      random.choice(classes_ids),
        'Semestre':       random.choice(['S1', 'S2']),
        'Credits':        random.choice([2, 3, 4, 6]),
        'Heures_Total':   random.choice([15, 20, 24, 30, 45]),
        'Coefficient':    random.choice([1, 2, 3]),
        'Type_Cours':     random.choice(TYPES_COURS),
    })

df_modules = pd.DataFrame(modules_list)

# ============================================================
# 6. EMPLOI DU TEMPS
# ============================================================
print("Generating emploi du temps...")
edt_list = []
ens_heures = {eid: 0 for eid in ens_ids}
salle_resa_count = {sid: 0 for sid in salles_ids}

for i in range(1, NB_EDT_ENTREES + 1):
    mod      = random.choice(modules_list)
    eid      = mod['ID_Enseignant']
    sid      = random.choice(salles_ids)
    creneau  = random.choice(CRENEAUX)
    d        = rand_weekday()
    jour     = JOURS_SEMAINE[d.weekday()]
    statut   = random.choices(
        ['Planifie', 'Realise', 'Annule', 'Reporte'],
        weights=[40, 45, 8, 7]
    )[0]

    ens_heures[eid] = ens_heures.get(eid, 0) + 2
    salle_resa_count[sid] = salle_resa_count.get(sid, 0) + 1

    edt_list.append({
        'ID_EDT':           f'EDT{i:04d}',
        'ID_Module':        mod['ID_Module'],
        'Nom_Module':       mod['Nom_Module'],
        'ID_Enseignant':    eid,
        'Nom_Enseignant':   ens_noms[eid],
        'ID_Classe':        mod['ID_Classe'],
        'ID_Salle':         sid,
        'Jour':             jour,
        'Heure_Debut':      creneau[0],
        'Heure_Fin':        creneau[1],
        'Type_Cours':       mod['Type_Cours'],
        'Semestre':         mod['Semestre'],
        'Semaine':          random.randint(1, 32),
        'Date_Seance':      d.strftime('%Y-%m-%d'),
        'Statut':           statut,
    })

df_edt = pd.DataFrame(edt_list)

# Mise a jour volume horaire enseignants
for eid, h in ens_heures.items():
    df_enseignants.loc[df_enseignants['ID_Enseignant'] == eid, 'Volume_Horaire_Total'] = h

nb_cours_ens = df_edt.groupby('ID_Enseignant').size().to_dict()
df_enseignants['Nb_Cours_Assignes'] = df_enseignants['ID_Enseignant'].map(nb_cours_ens).fillna(0).astype(int)

# ============================================================
# 7. RESERVATIONS
# ============================================================
print("Generating reservations...")
reservations = []

for i in range(1, NB_RESERVATIONS + 1):
    role    = random.choices(['etudiant', 'enseignant'], weights=[40, 60])[0]
    eid     = random.choice(ens_ids)
    etuid   = random.choice(etu_ids)
    sid     = random.choice(salles_ids)
    creneau = random.choice(CRENEAUX)
    d       = rand_weekday()
    statut  = random.choices(STATUTS_DEMANDE, weights=[25, 60, 15])[0]
    mod     = random.choice(modules_list)

    salle_resa_count[sid] = salle_resa_count.get(sid, 0) + 1

    reservations.append({
        'ID_Reservation':    f'RES{i:04d}',
        'ID_Salle':          sid,
        'ID_Demandeur':      eid if role == 'enseignant' else etuid,
        'Role_Demandeur':    role,
        'Nom_Demandeur':     ens_noms[eid] if role == 'enseignant' else f'Etudiant-{etuid}',
        'ID_Module':         mod['ID_Module'],
        'Nom_Module':        mod['Nom_Module'],
        'Filiere':           random.choice(FILIERES),
        'Date_Reservation':  d.strftime('%Y-%m-%d'),
        'Heure_Debut':       creneau[0],
        'Heure_Fin':         creneau[1],
        'Jour_Semaine':      JOURS_SEMAINE[d.weekday()],
        'Statut':            statut,
        'Date_Soumission':   (d - timedelta(days=random.randint(1, 14))).strftime('%Y-%m-%d'),
        'Date_Traitement':   d.strftime('%Y-%m-%d') if statut != 'en_attente' else None,
        'Motif':             fake.sentence(nb_words=8),
        'Commentaire_Admin': fake.sentence(nb_words=6) if statut != 'en_attente' else None,
    })

# Mise a jour nb reservations salles
for sid, nb in salle_resa_count.items():
    df_salles.loc[df_salles['ID_Salle'] == sid, 'Nb_Reservations'] = nb

# Calcul taux occupation
total_creneaux = len(JOURS_SEMAINE[:5]) * len(CRENEAUX) * 32
for idx in df_salles.index:
    nb = df_salles.at[idx, 'Nb_Reservations']
    df_salles.at[idx, 'Taux_Occupation'] = round(min((nb / total_creneaux) * 100, 100.0), 2)

df_reservations = pd.DataFrame(reservations)

# ============================================================
# 8. CONFLITS
# ============================================================
print("Generating conflits...")
conflits = []
for i in range(1, NB_CONFLITS + 1):
    d       = rand_weekday()
    creneau = random.choice(CRENEAUX)
    resolu  = random.choices([True, False], weights=[70, 30])[0]

    conflits.append({
        'ID_Conflit':        f'CONF{i:03d}',
        'Type_Conflit':      random.choice(TYPES_CONFLIT),
        'ID_Salle':          random.choice(salles_ids),
        'ID_Enseignant':     random.choice(ens_ids),
        'Date_Conflit':      d.strftime('%Y-%m-%d'),
        'Heure_Debut':       creneau[0],
        'Heure_Fin':         creneau[1],
        'Jour_Semaine':      JOURS_SEMAINE[d.weekday()],
        'Description':       fake.sentence(nb_words=10),
        'Resolu':            resolu,
        'Date_Resolution':   (d + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d') if resolu else None,
        'Mode_Resolution':   random.choice(['Changement salle', 'Changement horaire', 'Annulation']) if resolu else None,
    })

df_conflits = pd.DataFrame(conflits)

# ============================================================
# 9. MODIFICATIONS EDT
# ============================================================
print("Generating modifications...")
modifications = []
for i in range(1, NB_MODIFICATIONS + 1):
    edt_item   = random.choice(edt_list)
    d_orig     = datetime.strptime(edt_item['Date_Seance'], '%Y-%m-%d')
    d_new      = d_orig + timedelta(days=random.randint(1, 14))
    creneau_n  = random.choice(CRENEAUX)
    type_modif = random.choice(['Report', 'Annulation', 'Changement de salle', 'Decalage horaire'])

    modifications.append({
        'ID_Modification':       f'MODIF{i:04d}',
        'ID_EDT_Original':       edt_item['ID_EDT'],
        'ID_Module':             edt_item['ID_Module'],
        'Nom_Module':            edt_item['Nom_Module'],
        'ID_Enseignant':         edt_item['ID_Enseignant'],
        'Nom_Enseignant':        edt_item['Nom_Enseignant'],
        'Type_Modification':     type_modif,
        'Motif':                 random.choice(MOTIFS_MODIF),
        'Date_Originale':        edt_item['Date_Seance'],
        'Heure_Debut_Originale': edt_item['Heure_Debut'],
        'Heure_Fin_Originale':   edt_item['Heure_Fin'],
        'Salle_Originale':       edt_item['ID_Salle'],
        'Date_Nouvelle':         d_new.strftime('%Y-%m-%d') if type_modif != 'Annulation' else None,
        'Heure_Debut_Nouvelle':  creneau_n[0]               if type_modif != 'Annulation' else None,
        'Heure_Fin_Nouvelle':    creneau_n[1]               if type_modif != 'Annulation' else None,
        'Salle_Nouvelle':        random.choice(salles_ids)  if type_modif in ['Changement de salle', 'Report'] else None,
        'Delai_Notification_J':  random.randint(0, 7),
        'Date_Saisie':           (d_orig - timedelta(days=random.randint(1, 10))).strftime('%Y-%m-%d'),
    })

df_modifications = pd.DataFrame(modifications)

# ============================================================
# EXPORT
# ============================================================
print("Exporting...")

output_dir  = os.path.dirname(os.path.abspath(__file__))
output_xlsx = os.path.join(output_dir, 'eduhestim_dataset.xlsx')

with pd.ExcelWriter(output_xlsx, engine='openpyxl') as writer:
    df_salles.to_excel(writer,        sheet_name='Salles',         index=False)
    df_enseignants.to_excel(writer,   sheet_name='Enseignants',    index=False)
    df_etudiants.to_excel(writer,     sheet_name='Etudiants',      index=False)
    df_classes.to_excel(writer,       sheet_name='Classes',        index=False)
    df_modules.to_excel(writer,       sheet_name='Modules',        index=False)
    df_edt.to_excel(writer,           sheet_name='EmploiDuTemps',  index=False)
    df_reservations.to_excel(writer,  sheet_name='Reservations',   index=False)
    df_conflits.to_excel(writer,      sheet_name='Conflits',       index=False)
    df_modifications.to_excel(writer, sheet_name='Modifications',  index=False)

# CSV individuels
csv_dir = os.path.join(output_dir, 'csv')
os.makedirs(csv_dir, exist_ok=True)
for name, df in [
    ('salles', df_salles), ('enseignants', df_enseignants),
    ('etudiants', df_etudiants), ('classes', df_classes),
    ('modules', df_modules), ('emploi_du_temps', df_edt),
    ('reservations', df_reservations), ('conflits', df_conflits),
    ('modifications', df_modifications),
]:
    df.to_csv(os.path.join(csv_dir, f'{name}.csv'), index=False, encoding='utf-8-sig')

# ============================================================
# RESUME
# ============================================================
print("\n" + "="*60)
print("  Dataset EduHestim genere avec succes !")
print("="*60)
print(f"  Excel : {output_xlsx}")
print(f"  CSV   : {csv_dir}/")
print("="*60)
print(f"  Salles             : {len(df_salles)}")
print(f"  Enseignants        : {len(df_enseignants)}")
print(f"  Etudiants          : {len(df_etudiants)}")
print(f"  Classes            : {len(df_classes)}")
print(f"  Modules            : {len(df_modules)}")
print(f"  Emploi du Temps    : {len(df_edt)}")
print(f"  Reservations       : {len(df_reservations)}")
print(f"  Conflits           : {len(df_conflits)}")
print(f"  Modifications EDT  : {len(df_modifications)}")
print("="*60)
print("\nKPIs rapides :")
print(f"  Taux occupation moyen salles    : {df_salles['Taux_Occupation'].mean():.1f}%")
print(f"  Volume horaire moyen enseignant : {df_enseignants['Volume_Horaire_Total'].mean():.1f}h")
print(f"  Taux absence moyen etudiants    : {df_etudiants['Taux_Absence'].mean():.1f}%")
print(f"  Reservations approuvees         : {(df_reservations['Statut']=='approuve').sum()}/{len(df_reservations)}")
print(f"  Conflits resolus                : {df_conflits['Resolu'].sum()}/{len(df_conflits)}")
print(f"  Annulations EDT                 : {(df_modifications['Type_Modification']=='Annulation').sum()}")
print("="*60)