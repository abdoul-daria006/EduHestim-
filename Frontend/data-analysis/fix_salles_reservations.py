"""
Génère des réservations pour les nouvelles salles S026-S125
et recalcule Nb_Reservations + Taux_Occupation dans la feuille Salles
"""

from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker('fr_FR')
random.seed(77)
Faker.seed(77)

FILE = 'eduhestim_dataset.xlsx'

# ── Chargement ──────────────────────────────────────────────
print("Chargement...")
sheets        = pd.read_excel(FILE, sheet_name=None)
df_salles     = sheets['Salles']
df_resa       = sheets['Reservations']
df_ens        = sheets['Enseignants']
df_modules    = sheets['Modules']

print(f"  Salles        : {len(df_salles)}")
print(f"  Reservations  : {len(df_resa)}")

# ── Nouvelles salles (S026 → S125) ──────────────────────────
new_salles_ids = df_salles[df_salles['ID_Salle'] >= 'S026']['ID_Salle'].tolist()
print(f"  Nouvelles salles à alimenter : {len(new_salles_ids)}")

# ── Config ──────────────────────────────────────────────────
JOURS_SEMAINE  = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
CRENEAUX       = [('08:00','10:00'), ('10:15','12:15'), ('14:00','16:00'), ('16:15','18:15')]
FILIERES       = ['Informatique', 'Management', 'Mathematiques', 'Physique', 'Langues', 'Droit']
STATUTS        = ['en_attente', 'approuve', 'refuse']
ANNEE_DEBUT    = datetime(2024, 9, 16)
ANNEE_FIN      = datetime(2025, 6, 30)
TOTAL_CRENEAUX = 640  # 5j × 4cr × 32 semaines

ens_ids   = df_ens['ID_Enseignant'].tolist()
ens_noms  = {r['ID_Enseignant']: f"{r['Prenom']} {r['Nom']}" for _, r in df_ens.iterrows()}
mod_list  = df_modules.to_dict('records')

def rand_weekday():
    delta = ANNEE_FIN - ANNEE_DEBUT
    d = ANNEE_DEBUT + timedelta(days=random.randint(0, delta.days))
    while d.weekday() >= 5:
        d = ANNEE_DEBUT + timedelta(days=random.randint(0, delta.days))
    return d

# ── Génération réservations pour nouvelles salles ───────────
# Chaque nouvelle salle reçoit entre 30 et 120 réservations
# (distribution réaliste, similaire aux salles existantes)
print("\nGénération des réservations...")

last_id = int(df_resa['ID_Reservation'].str.replace('RES','').astype(int).max())
nouvelles_resas = []

for sid in new_salles_ids:
    # Nb réservations aléatoire entre 30 et 120
    nb = random.randint(30, 120)
    for _ in range(nb):
        role    = random.choices(['etudiant','enseignant'], weights=[40,60])[0]
        eid     = random.choice(ens_ids)
        creneau = random.choice(CRENEAUX)
        d       = rand_weekday()
        statut  = random.choices(STATUTS, weights=[25, 60, 15])[0]
        mod     = random.choice(mod_list)
        last_id += 1

        nouvelles_resas.append({
            'ID_Reservation':    f'RES{last_id:04d}',
            'ID_Salle':          sid,
            'ID_Demandeur':      eid if role == 'enseignant' else f'ET{random.randint(1,250):04d}',
            'Role_Demandeur':    role,
            'Nom_Demandeur':     ens_noms[eid] if role == 'enseignant' else f'Etudiant-ET{random.randint(1,250):04d}',
            'ID_Module':         mod['ID_Module'],
            'Nom_Module':        mod['Nom_Module'],
            'Filiere':           random.choice(FILIERES),
            'Date_Reservation':  d.strftime('%Y-%m-%d'),
            'Heure_Debut':       creneau[0],
            'Heure_Fin':         creneau[1],
            'Jour_Semaine':      JOURS_SEMAINE[d.weekday()],
            'Statut':            statut,
            'Date_Soumission':   (d - timedelta(days=random.randint(1,14))).strftime('%Y-%m-%d'),
            'Date_Traitement':   d.strftime('%Y-%m-%d') if statut != 'en_attente' else None,
            'Motif':             fake.sentence(nb_words=8),
            'Commentaire_Admin': fake.sentence(nb_words=6) if statut != 'en_attente' else None,
        })

df_new_resas = pd.DataFrame(nouvelles_resas)
df_resa_final = pd.concat([df_resa, df_new_resas], ignore_index=True)

print(f"  Nouvelles réservations générées : {len(df_new_resas)}")
print(f"  Total réservations              : {len(df_resa_final)}")

# ── Recalcul Nb_Reservations + Taux_Occupation pour TOUTES les salles ──
print("\nRecalcul Nb_Reservations et Taux_Occupation...")

resa_count = df_resa_final.groupby('ID_Salle').size().reset_index(name='Nb_Resa_Calc')
df_salles_updated = df_salles.drop(columns=['Nb_Reservations','Taux_Occupation'], errors='ignore').merge(
    resa_count, on='ID_Salle', how='left'
).fillna({'Nb_Resa_Calc': 0})

df_salles_updated['Nb_Reservations'] = df_salles_updated['Nb_Resa_Calc'].astype(int)
df_salles_updated['Taux_Occupation'] = (df_salles_updated['Nb_Resa_Calc'] / TOTAL_CRENEAUX * 100).round(2)
df_salles_updated = df_salles_updated.drop(columns=['Nb_Resa_Calc'])

# Vérification
new_zeros = df_salles_updated[df_salles_updated['Nb_Reservations'] == 0]
print(f"  Salles encore à 0 réservations : {len(new_zeros)}")
print(f"  Taux occupation moyen          : {df_salles_updated['Taux_Occupation'].mean():.1f}%")
print(f"  Taux occupation max            : {df_salles_updated['Taux_Occupation'].max():.1f}%")
print(f"  Taux occupation min            : {df_salles_updated['Taux_Occupation'].min():.1f}%")

# ── Réécriture Excel ────────────────────────────────────────
print("\nRéécriture du fichier Excel...")
with pd.ExcelWriter(FILE, engine='openpyxl') as writer:
    df_salles_updated.to_excel(writer,        sheet_name='Salles',        index=False)
    sheets['Enseignants'].to_excel(writer,    sheet_name='Enseignants',   index=False)
    sheets['Etudiants'].to_excel(writer,      sheet_name='Etudiants',     index=False)
    sheets['Classes'].to_excel(writer,        sheet_name='Classes',       index=False)
    sheets['Modules'].to_excel(writer,        sheet_name='Modules',       index=False)
    sheets['EmploiDuTemps'].to_excel(writer,  sheet_name='EmploiDuTemps', index=False)
    df_resa_final.to_excel(writer,            sheet_name='Reservations',  index=False)
    sheets['Conflits'].to_excel(writer,       sheet_name='Conflits',      index=False)
    sheets['Modifications'].to_excel(writer,  sheet_name='Modifications', index=False)

print("\n" + "="*55)
print("  Dataset mis à jour avec succès !")
print("="*55)
print(f"  Salles        : {len(df_salles)} → {len(df_salles_updated)}")
print(f"  Reservations  : {len(df_resa)} → {len(df_resa_final)}")
print("="*55)
print("\nAperçu nouvelles salles avec réservations :")
print(df_salles_updated[df_salles_updated['ID_Salle'] >= 'S026'][
    ['ID_Salle','Nom_Salle','Type_Salle','Nb_Reservations','Taux_Occupation']
].head(10).to_string(index=False))
