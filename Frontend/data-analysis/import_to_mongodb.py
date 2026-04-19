"""
╔══════════════════════════════════════════════════════════════╗
║     EduHestim — Import Dataset Faker → MongoDB               ║
║     Base : eduhestim  |  localhost:27017                     ║
║                                                              ║
║  Collections ciblées :                                       ║
║    salles, users, classes, emploiedutemps, demandes          ║
║    + conflits, modifications (nouvelles)                     ║
╚══════════════════════════════════════════════════════════════╝

Installation :
    pip install pymongo pandas openpyxl

Usage :
    python import_to_mongodb.py
"""

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import pandas as pd
from datetime import datetime
import sys

# ============================================================
# CONFIG
# ============================================================
MONGO_URI  = "mongodb://localhost:27017"
DB_NAME    = "eduhestim"
EXCEL_FILE = "eduhestim_dataset.xlsx"

# Mode : 'append' = ajoute sans supprimer | 'replace' = vide et réinsère
MODE = "append"

# ============================================================
# CONNEXION
# ============================================================
print("Connexion MongoDB...")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[DB_NAME]
    print(f"  Connecte a : {MONGO_URI}/{DB_NAME}")
except Exception as e:
    print(f"ERREUR connexion MongoDB : {e}")
    sys.exit(1)

# ============================================================
# CHARGEMENT EXCEL
# ============================================================
print("\nChargement du fichier Excel...")
try:
    df_salles  = pd.read_excel(EXCEL_FILE, sheet_name='Salles')
    df_ens     = pd.read_excel(EXCEL_FILE, sheet_name='Enseignants')
    df_etu     = pd.read_excel(EXCEL_FILE, sheet_name='Etudiants')
    df_classes = pd.read_excel(EXCEL_FILE, sheet_name='Classes')
    df_edt     = pd.read_excel(EXCEL_FILE, sheet_name='EmploiDuTemps')
    df_resa    = pd.read_excel(EXCEL_FILE, sheet_name='Reservations')
    df_conf    = pd.read_excel(EXCEL_FILE, sheet_name='Conflits')
    df_modif   = pd.read_excel(EXCEL_FILE, sheet_name='Modifications')
    print("  Fichier charge avec succes")
except Exception as e:
    print(f"ERREUR lecture Excel : {e}")
    sys.exit(1)

def clean_doc(d):
    """Nettoie un dict pour MongoDB : supprime NaN, convertit types."""
    result = {}
    for k, v in d.items():
        if pd.isna(v) if not isinstance(v, (list, dict, bool)) else False:
            result[k] = None
        elif isinstance(v, float) and v == int(v):
            result[k] = int(v)
        elif hasattr(v, 'item'):
            result[k] = v.item()
        else:
            result[k] = v
    result['createdAt'] = datetime.utcnow()
    result['updatedAt'] = datetime.utcnow()
    result['source']    = 'faker_dataset'
    return result

def insert_collection(col_name, docs, mode=MODE):
    col = db[col_name]
    if mode == 'replace':
        # Supprime uniquement les docs faker pour ne pas écraser les vrais
        col.delete_many({'source': 'faker_dataset'})
        print(f"  Collection '{col_name}' : anciens docs faker supprimes")
    if docs:
        try:
            result = col.insert_many(docs, ordered=False)
            print(f"  Collection '{col_name}' : {len(result.inserted_ids)} documents inseres")
        except BulkWriteError as bwe:
            print(f"  Collection '{col_name}' : {bwe.details['nInserted']} inseres, quelques erreurs ignorees")
    else:
        print(f"  Collection '{col_name}' : aucun document a inserer")

# ============================================================
# 1. SALLES
# ============================================================
print("\n--- Importation : salles ---")
salles_docs = []
for _, row in df_salles.iterrows():
    doc = clean_doc({
        'nom':          row['Nom_Salle'],
        'batiment':     row['Batiment'],
        'type':         row['Type_Salle'],
        'capacite':     int(row['Capacite']),
        'disponible':   bool(row['Disponible']),
        'faker_id':     row['ID_Salle'],
    })
    salles_docs.append(doc)

insert_collection('salles', salles_docs)

# Récupérer le mapping ID_Salle → ObjectId MongoDB
salle_map = {}
for doc in db['salles'].find({'source': 'faker_dataset'}, {'_id': 1, 'faker_id': 1}):
    salle_map[doc['faker_id']] = doc['_id']

# ============================================================
# 2. USERS (enseignants + étudiants)
# ============================================================
print("\n--- Importation : users (enseignants) ---")
users_docs = []

for _, row in df_ens.iterrows():
    doc = clean_doc({
        'nom':           row['Nom'],
        'prenom':        row['Prenom'],
        'email':         row['Email'],
        'telephone':     str(row['Telephone']),
        'role':          'enseignant',
        'grade':         row['Grade'],
        'departement':   row['Departement'],
        'anneesExperience': int(row['Annees_Experience']),
        'dateEmbauche':  str(row['Date_Embauche']),
        'volumeHoraireHebdo': int(row['Volume_Horaire_Hebdo']),
        'faker_id':      row['ID_Enseignant'],
        'password':      '$2b$10$faker.hashed.password',
        'statut':        'actif',
    })
    users_docs.append(doc)

print(f"  {len(df_ens)} enseignants prepares")

print("\n--- Importation : users (etudiants) ---")
for _, row in df_etu.iterrows():
    doc = clean_doc({
        'nom':            row['Nom'],
        'prenom':         row['Prenom'],
        'email':          row['Email'],
        'telephone':      str(row['Telephone']),
        'role':           'etudiant',
        'dateNaissance':  str(row['Date_Naissance']),
        'classeCode':     row['ID_Classe'],
        'filiere':        row['Filiere'],
        'niveau':         row['Niveau'],
        'statut':         row['Statut'].lower(),
        'dateInscription':str(row['Date_Inscription']),
        'boursier':       bool(row['Boursier']),
        'tauxAbsence':    float(row['Taux_Absence']),
        'faker_id':       row['ID_Etudiant'],
        'password':       '$2b$10$faker.hashed.password',
    })
    users_docs.append(doc)

print(f"  {len(df_etu)} etudiants prepares")
insert_collection('users', users_docs)

# Mapping enseignants → ObjectId
ens_map = {}
for doc in db['users'].find({'source': 'faker_dataset', 'role': 'enseignant'}, {'_id': 1, 'faker_id': 1}):
    ens_map[doc['faker_id']] = doc['_id']

# ============================================================
# 3. CLASSES
# ============================================================
print("\n--- Importation : classes ---")
classes_docs = []
for _, row in df_classes.iterrows():
    doc = clean_doc({
        'nom':              row['Nom_Classe'],
        'filiere':          row['Filiere'],
        'niveau':           row['Niveau'],
        'anneeScolaire':    row['Annee_Scolaire'],
        'nbEtudiantsMax':   int(row['Nb_Etudiants_Max']),
        'nbEtudiantsInscrits': int(row['Nb_Etudiants_Inscrits']),
        'faker_id':         row['ID_Classe'],
    })
    classes_docs.append(doc)

insert_collection('classes', classes_docs)

# Mapping classes → ObjectId
classe_map = {}
for doc in db['classes'].find({'source': 'faker_dataset'}, {'_id': 1, 'faker_id': 1}):
    classe_map[doc['faker_id']] = doc['_id']

# ============================================================
# 4. EMPLOI DU TEMPS
# ============================================================
print("\n--- Importation : emploiedutemps ---")
edt_docs = []
for _, row in df_edt.iterrows():
    ens_id  = ens_map.get(row['ID_Enseignant'])
    salle_id= salle_map.get(row['ID_Salle'])
    classe_id = classe_map.get(row['ID_Classe'])

    doc = clean_doc({
        'matiere':       row['Nom_Module'],
        'type':          row['Type_Cours'],
        'enseignant':    ens_id,
        'enseignantNom': row['Nom_Enseignant'],
        'salle':         salle_id,
        'salleNom':      row['ID_Salle'],
        'classe':        classe_id,
        'classeCode':    row['ID_Classe'],
        'jour':          row['Jour'],
        'heureDebut':    row['Heure_Debut'],
        'heureFin':      row['Heure_Fin'],
        'semestre':      row['Semestre'],
        'semaine':       int(row['Semaine']),
        'dateSeance':    str(row['Date_Seance']),
        'statut':        row['Statut'].lower(),
        'faker_id':      row['ID_EDT'],
    })
    edt_docs.append(doc)

insert_collection('emploiedutemps', edt_docs)

# Mapping EDT → ObjectId
edt_map = {}
for doc in db['emploiedutemps'].find({'source': 'faker_dataset'}, {'_id': 1, 'faker_id': 1}):
    edt_map[doc['faker_id']] = doc['_id']

# ============================================================
# 5. DEMANDES (réservations)
# ============================================================
print("\n--- Importation : demandes ---")
statut_map = {'approuve': 'approuvee', 'refuse': 'refusee', 'en_attente': 'en_attente'}
demandes_docs = []

for _, row in df_resa.iterrows():
    salle_id = salle_map.get(row['ID_Salle'])
    doc = clean_doc({
        'salle':             salle_id,
        'salleNom':          row['ID_Salle'],
        'demandeur':         row['ID_Demandeur'],
        'roleDemandeur':     row['Role_Demandeur'],
        'nomDemandeur':      row['Nom_Demandeur'],
        'module':            row['Nom_Module'],
        'filiere':           row['Filiere'],
        'dateReservation':   str(row['Date_Reservation']),
        'heureDebut':        row['Heure_Debut'],
        'heureFin':          row['Heure_Fin'],
        'jourSemaine':       row['Jour_Semaine'],
        'statut':            statut_map.get(row['Statut'], row['Statut']),
        'dateSoumission':    str(row['Date_Soumission']),
        'motif':             row['Motif'],
        'commentaireAdmin':  row.get('Commentaire_Admin'),
        'faker_id':          row['ID_Reservation'],
    })
    demandes_docs.append(doc)

insert_collection('demandes', demandes_docs)

# ============================================================
# 6. CONFLITS (nouvelle collection)
# ============================================================
print("\n--- Importation : conflits ---")
conflits_docs = []
for _, row in df_conf.iterrows():
    salle_id = salle_map.get(row['ID_Salle'])
    ens_id   = ens_map.get(row['ID_Enseignant'])
    doc = clean_doc({
        'typeConflit':    row['Type_Conflit'],
        'salle':          salle_id,
        'salleNom':       row['ID_Salle'],
        'enseignant':     ens_id,
        'dateConflit':    str(row['Date_Conflit']),
        'heureDebut':     row['Heure_Debut'],
        'heureFin':       row['Heure_Fin'],
        'jourSemaine':    row['Jour_Semaine'],
        'description':    row['Description'],
        'resolu':         bool(row['Resolu']),
        'dateResolution': str(row['Date_Resolution']) if pd.notna(row.get('Date_Resolution')) else None,
        'modeResolution': row.get('Mode_Resolution'),
        'faker_id':       row['ID_Conflit'],
    })
    conflits_docs.append(doc)

insert_collection('conflits', conflits_docs)

# ============================================================
# 7. MODIFICATIONS EDT (nouvelle collection)
# ============================================================
print("\n--- Importation : modifications ---")
modifs_docs = []
for _, row in df_modif.iterrows():
    edt_ref = edt_map.get(row['ID_EDT_Original'])
    doc = clean_doc({
        'edtOriginal':       edt_ref,
        'idEdtOriginal':     row['ID_EDT_Original'],
        'module':            row['Nom_Module'],
        'enseignant':        ens_map.get(row['ID_Enseignant']),
        'enseignantNom':     row['Nom_Enseignant'],
        'typeModification':  row['Type_Modification'],
        'motif':             row['Motif'],
        'dateOriginale':     str(row['Date_Originale']),
        'heureDebutOriginal':row['Heure_Debut_Originale'],
        'heureFinOriginal':  row['Heure_Fin_Originale'],
        'salleOriginale':    row['Salle_Originale'],
        'dateNouvelle':      str(row['Date_Nouvelle']) if pd.notna(row.get('Date_Nouvelle')) else None,
        'heureDebutNouvelle':row.get('Heure_Debut_Nouvelle'),
        'heureFinNouvelle':  row.get('Heure_Fin_Nouvelle'),
        'salleNouvelle':     row.get('Salle_Nouvelle'),
        'delaiNotifJours':   int(row['Delai_Notification_J']) if pd.notna(row.get('Delai_Notification_J')) else None,
        'dateSaisie':        str(row['Date_Saisie']),
        'faker_id':          row['ID_Modification'],
    })
    modifs_docs.append(doc)

insert_collection('modifications', modifs_docs)

# ============================================================
# RÉSUMÉ FINAL
# ============================================================
print("\n" + "="*55)
print("  IMPORTATION TERMINEE — EduHestim MongoDB")
print("="*55)
for col_name in ['salles','users','classes','emploiedutemps','demandes','conflits','modifications']:
    col = db[col_name]
    total    = col.count_documents({})
    from_faker = col.count_documents({'source': 'faker_dataset'})
    print(f"  {col_name:20s} : {total:>5} total  ({from_faker} faker)")
print("="*55)
print("\nPour supprimer uniquement les docs faker plus tard :")
print("  db.<collection>.deleteMany({ source: 'faker_dataset' })")
print("="*55)

client.close()
