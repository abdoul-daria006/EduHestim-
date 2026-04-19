"""
Ajoute 100 lignes à la feuille Salles du dataset existant
eduhestim_dataset.xlsx : 25 → 125 salles
"""

from faker import Faker
import pandas as pd
import numpy as np
import random

fake = Faker('fr_FR')
random.seed(99)
Faker.seed(99)

FILE = 'eduhestim_dataset.xlsx'

# ── Chargement feuilles existantes ──────────────────────────
print("Chargement du fichier existant...")
sheets = pd.read_excel(FILE, sheet_name=None)  # charge toutes les feuilles

df_salles      = sheets['Salles']
df_reservations = sheets['Reservations']

print(f"  Salles actuelles       : {len(df_salles)}")
print(f"  Reservations actuelles : {len(df_reservations)}")

# ── Config ──────────────────────────────────────────────────
TYPES_SALLE = ['Normale', 'Informatique', 'Amphitheatre', 'Laboratoire']
BATIMENTS   = ['Batiment A', 'Batiment B', 'Batiment C', 'Batiment D']

cap_par_type = {
    'Normale':      [30, 35, 40],
    'Informatique': [20, 25, 30],
    'Amphitheatre': [100, 150, 200, 250],
    'Laboratoire':  [15, 20, 25],
}

# Numérotation à partir de 26
start_idx = len(df_salles) + 1  # 26

nouvelles_salles = []
for i in range(start_idx, start_idx + 100):
    t = random.choice(TYPES_SALLE)
    nouvelles_salles.append({
        'ID_Salle':        f'S{i:03d}',
        'Nom_Salle':       f'{t[:4]}-{i:02d}',
        'Batiment':        random.choice(BATIMENTS),
        'Type_Salle':      t,
        'Capacite':        random.choice(cap_par_type[t]),
        'Disponible':      random.choices([True, False], weights=[85, 15])[0],
        'Nb_Reservations': 0,
        'Taux_Occupation': 0.0,
    })

df_new = pd.DataFrame(nouvelles_salles)

# Recalcul Nb_Reservations pour les nouvelles salles
new_ids = df_new['ID_Salle'].tolist()
resa_count = df_reservations[df_reservations['ID_Salle'].isin(new_ids)].groupby('ID_Salle').size()

TOTAL_CRENEAUX = 640
for idx, row in df_new.iterrows():
    nb = resa_count.get(row['ID_Salle'], 0)
    df_new.at[idx, 'Nb_Reservations'] = nb
    df_new.at[idx, 'Taux_Occupation'] = round(min(nb / TOTAL_CRENEAUX * 100, 100.0), 2)

# ── Fusion ──────────────────────────────────────────────────
df_salles_final = pd.concat([df_salles, df_new], ignore_index=True)

print(f"\n  Nouvelles salles ajoutees : {len(df_new)}")
print(f"  Total salles finale       : {len(df_salles_final)}")

# ── Réécriture du fichier Excel (toutes feuilles conservées) ─
print("\nRéécriture du fichier Excel...")
with pd.ExcelWriter(FILE, engine='openpyxl') as writer:
    df_salles_final.to_excel(writer,          sheet_name='Salles',        index=False)
    sheets['Enseignants'].to_excel(writer,    sheet_name='Enseignants',   index=False)
    sheets['Etudiants'].to_excel(writer,      sheet_name='Etudiants',     index=False)
    sheets['Classes'].to_excel(writer,        sheet_name='Classes',       index=False)
    sheets['Modules'].to_excel(writer,        sheet_name='Modules',       index=False)
    sheets['EmploiDuTemps'].to_excel(writer,  sheet_name='EmploiDuTemps', index=False)
    sheets['Reservations'].to_excel(writer,   sheet_name='Reservations',  index=False)
    sheets['Conflits'].to_excel(writer,       sheet_name='Conflits',      index=False)
    sheets['Modifications'].to_excel(writer,  sheet_name='Modifications', index=False)

print("\n" + "="*50)
print("  Dataset mis a jour avec succes !")
print("="*50)
print(f"  Salles : {len(df_salles)} → {len(df_salles_final)}")
print(f"  Fichier : {FILE}")
print("="*50)

# Apercu des nouvelles salles
print("\nApercu des 5 premieres nouvelles salles :")
print(df_new.head().to_string(index=False))
