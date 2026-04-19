# 🚀 GUIDE D'UTILISATION - SYSTÈME EDUHESTIM COMPLET

## 📋 FICHIERS CRÉÉS

### 1. Système de Données
- **eduhestim-data.js** - Base de données centralisée (localStorage)

### 2. Pages Admin Fonctionnelles
- **PagelistedesUtilisateurs_COMPLET.html** - Gestion utilisateurs avec filtres
- **ImporterEtudiants.html** - Import CSV/Excel (à créer)
- **GestionDemandes-Admin_AMELIORE.html** - Approuver/Refuser demandes (à créer)
- **admindash_AMELIORE.html** - Dashboard avec créer EDT (à créer)
- **CreerEmploiDuTemps.html** - Création EDT par classe (à créer)

## 🔄 COMMENT ÇA FONCTIONNE

### Interconnexion des Pages

```
ADMIN crée une demande → Sauvegardé dans eduhestim-data.js
                      ↓
              localStorage mis à jour
                      ↓
ÉTUDIANT/PROF voit la décision → Lu depuis eduhestim-data.js
```

### Exemple : Flux d'une Demande

1. **Étudiant** fait une demande (Fairedesdemandes.html)
   → `EduHestimData.addDemande({...})`
   
2. **Admin** voit la demande (GestionDemandes-Admin.html)
   → `EduHestimData.getDemandes()`
   
3. **Admin** approuve/refuse
   → `EduHestimData.approuverDemande(id)` ou `refuserDemande(id)`
   
4. **Étudiant** est notifié
   → `EduHestimData.getNotificationsByUser(userId)`

## 📝 UTILISATION

### 1. Inclure le système de données dans chaque page

```html
<script src="eduhestim-data.js"></script>
```

### 2. Exemples d'utilisation

#### Créer un utilisateur
```javascript
EduHestimData.addUser({
    nom: "DUPONT",
    prenom: "Jean",
    email: "jean.dupont@hestim.ma",
    password: "123456",
    role: "etudiant",
    classe: "2A-INFO",
    departement: "Génie Informatique",
    annee: "2ème année"
});
```

#### Approuver une demande
```javascript
EduHestimData.approuverDemande(demandeId, "Admin Principal", "Salle réservée");
```

#### Créer un cours dans l'EDT
```javascript
EduHestimData.addCours({
    classeId: 1,
    classeCode: "3A-INFO",
    jour: "Lundi",
    heureDebut: "08:00",
    heureFin: "10:00",
    matiere: "Programmation Web",
    enseignantNom: "Prof. MARTIN",
    salle: "Ghandi Info 1",
    type: "TP"
});
```

## ✅ PROCHAINES ÉTAPES

1. Créer ImporterEtudiants.html
2. Améliorer GestionDemandes-Admin.html
3. Améliorer admindash.html
4. Créer CreerEmploiDuTemps.html
5. Connecter toutes les pages existantes au système de données

## 🎯 FONCTIONNALITÉS IMPLÉMENTÉES

✅ Système de données centralisé  
✅ Gestion utilisateurs avec CRUD  
✅ Statistiques en temps réel  
✅ Filtrage et recherche  
✅ Gestion des demandes (approuver/refuser)  
✅ Système de notifications  
✅ Gestion des classes  
✅ Emplois du temps par classe  

## 🔐 DONNÉES DE TEST

**Admin:**
- Email: admin@hestim.ma
- Password: admin123

**Étudiant:**
- Email: maurane.alliman@hestim.ma
- Password: 123456

**Enseignant:**
- Email: maurane.bethio@hestim.ma
- Password: 123456
