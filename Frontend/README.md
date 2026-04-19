# 🎓 EDUHESTIM - SYSTÈME DE GESTION ACADÉMIQUE

## ✅ PROJET COMPLET ET FONCTIONNEL POUR VIDÉO

---

## 📋 RÉSUMÉ RAPIDE

Ce projet est **100% fonctionnel** et **prêt pour la vidéo**. Tout fonctionne en local (localStorage), pas besoin de base de données.

### ✨ CE QUI FONCTIONNE :

✅ **3 comptes par défaut uniquement** au départ  
✅ **Admin peut créer de nouveaux comptes** qui peuvent se connecter  
✅ **Système de demandes complet** : Étudiant → Admin → Notification  
✅ **Gestion des salles** : Admin crée/supprime des salles  
✅ **Bouton déconnexion** sur tous les dashboards  
✅ **Statistiques réelles** (pas de fausses données)  
✅ **Notifications automatiques** quand admin traite une demande  

---

## 🔐 COMPTES PAR DÉFAUT

### 1. Administrateur
- **Email:** `admin@hestim.ma`
- **Mot de passe:** `admin123`
- **Rôle:** administrateur

### 2. Enseignant
- **Email:** `enseignant@hestim.ma`
- **Mot de passe:** `prof123`
- **Rôle:** enseignant

### 3. Étudiant
- **Email:** `etudiant@hestim.ma`
- **Mot de passe:** `etud123`
- **Rôle:** etudiant

---

## 🎬 SCÉNARIO POUR LA VIDÉO

### Étape 1 : Démonstration Comptes par Défaut
1. Ouvrir `Connexion.html`
2. Montrer qu'il n'y a que **3 comptes** au départ
3. Se connecter avec chaque compte pour montrer les dashboards

### Étape 2 : Admin Crée un Nouveau Compte
1. Se connecter en tant qu'admin
2. Aller sur "Créer Utilisateur"
3. Créer un nouvel étudiant :
   - Nom: NOUVEAU
   - Prénom: Étudiant
   - Email: nouveau@hestim.ma
   - Mot de passe: test123
   - Classe: 3ème année GI
4. Se déconnecter
5. **SE CONNECTER AVEC LE NOUVEAU COMPTE** pour prouver qu'il fonctionne !

### Étape 3 : Étudiant Fait une Demande
1. Connecté en tant qu'étudiant
2. Aller sur "Faire une Demande"
3. Remplir le formulaire :
   - Salle: Ghandi Salle 01
   - Date: (choisir une date)
   - Horaire: 14:00 - 16:00
   - Motif: "Réunion projet de fin d'études"
4. Soumettre
5. Aller sur "Mes Demandes" → La demande apparaît avec statut "En attente"

### Étape 4 : Admin Traite la Demande
1. Se déconnecter
2. Se connecter en tant qu'admin
3. Aller sur "Gestion des Demandes"
4. Voir la demande de l'étudiant
5. **Approuver** la demande avec un commentaire : "Salle réservée, bonne réunion !"

### Étape 5 : Étudiant Voit la Réponse
1. Se déconnecter
2. Se reconnecter en tant qu'étudiant
3. Aller sur "Mes Demandes"
4. **La demande est marquée "Approuvée"** avec le commentaire de l'admin !

### Étape 6 : Admin Gère les Salles
1. Se connecter en admin
2. Aller sur "Gestion des Salles"
3. **Créer une nouvelle salle** :
   - Nom: Ghandi Salle 20
   - Type: Normale
   - Capacité: 35
   - Bâtiment: Ghandi
4. Montrer que la salle apparaît
5. **Supprimer une salle** pour montrer que ça fonctionne

---

## 📁 FICHIERS ESSENTIELS

### 🔑 Fichiers JavaScript (TOUJOURS INCLURE)
- **`auth-system.js`** - Gestion des comptes et authentification
- **`data-manager.js`** - Gestion centralisée des données

### 🌐 Pages HTML Principales
- **`Connexion.html`** - Page de connexion
- **`admindash.html`** - Dashboard admin
- **`Etudiantdash.html`** - Dashboard étudiant
- **`Enseignantdash.html`** - Dashboard enseignant (si tu en as besoin)

### 📋 Pages Admin
- **`FormulaireCreation.html`** - Créer des utilisateurs
- **`GestiondesalleAdmin.html`** - Gérer les salles
- **`GestionDemandes-Admin.html`** - Gérer les demandes

### 👨‍🎓 Pages Étudiant
- **`Fairedesdemandes.html`** - Faire une demande
- **`Mesreservations.html`** - Voir mes demandes

---

## 🚀 INSTALLATION ET UTILISATION

### Méthode Simple (Recommandée)
1. Télécharger TOUS les fichiers
2. Mettre tous les fichiers dans **le même dossier**
3. Ouvrir `Connexion.html` dans un navigateur
4. C'est tout ! ✅

### Structure des Fichiers
```
mon-projet/
├── auth-system.js          ← OBLIGATOIRE
├── data-manager.js         ← OBLIGATOIRE
├── Connexion.html
├── admindash.html
├── Etudiantdash.html
├── Fairedesdemandes.html
├── Mesreservations.html
├── FormulaireCreation.html
├── GestiondesalleAdmin.html
├── GestionDemandes-Admin.html
└── (autres fichiers...)
```

---

## 🔧 FONCTIONNALITÉS DÉTAILLÉES

### 1. SYSTÈME D'AUTHENTIFICATION
- ✅ 3 comptes par défaut au démarrage
- ✅ Admin peut créer des comptes enseignants/étudiants
- ✅ Les nouveaux comptes peuvent se connecter immédiatement
- ✅ Bouton déconnexion sur tous les dashboards
- ✅ Protection des pages (redirection si non connecté)

### 2. GESTION DES DEMANDES
- ✅ Étudiant fait une demande de réservation
- ✅ Demande apparaît dans "Mes Demandes" (étudiant)
- ✅ Demande apparaît dans "Gestion Demandes" (admin)
- ✅ Admin peut approuver/refuser avec commentaire
- ✅ Étudiant reçoit notification du statut
- ✅ Statuts : En attente / Approuvée / Refusée

### 3. GESTION DES SALLES
- ✅ Liste de 10 salles par défaut
- ✅ Admin peut créer des salles
- ✅ Admin peut modifier des salles
- ✅ Admin peut supprimer des salles
- ✅ Les salles apparaissent dans les formulaires de demande

### 4. STATISTIQUES EN TEMPS RÉEL
- ✅ Nombre d'étudiants (compte réel)
- ✅ Nombre d'enseignants (compte réel)
- ✅ Nombre de salles (compte réel)
- ✅ Nombre de demandes en attente (compte réel)
- ✅ Plus de fausses données !

---

## 💾 STOCKAGE DES DONNÉES

Toutes les données sont stockées en **localStorage** :
- `auth_accounts` - Liste des comptes utilisateurs
- `eduhestim_salles` - Liste des salles
- `eduhestim_demandes` - Liste des demandes
- `eduhestim_notifications` - Notifications

### Réinitialiser les Données
Pour recommencer à zéro :
1. Ouvrir la console du navigateur (F12)
2. Taper : `localStorage.clear()`
3. Recharger la page

---

## ⚠️ POINTS IMPORTANTS POUR LA VIDÉO

### ✅ À FAIRE :
1. **Toujours commencer par Connexion.html**
2. **Montrer les 3 comptes par défaut**
3. **Créer un nouveau compte et SE CONNECTER AVEC**
4. **Faire une demande complète** (étudiant → admin → étudiant)
5. **Montrer la création/suppression de salle**

### ❌ À ÉVITER :
1. Ne pas oublier de se déconnecter entre les comptes
2. Ne pas ouvrir directement un dashboard sans se connecter
3. Ne pas oublier les fichiers .js (sinon rien ne marche)

---

## 🐛 DÉPANNAGE

### Problème : "authSystem is not defined"
**Solution :** Vérifier que `auth-system.js` est bien dans le même dossier

### Problème : "dataManager is not defined"
**Solution :** Vérifier que `data-manager.js` est bien dans le même dossier

### Problème : Les statistiques affichent 0
**Solution :** C'est normal au début ! Créer des comptes et des demandes pour voir les vrais chiffres

### Problème : Impossible de se connecter
**Solution :** Vérifier :
- Email exact : `admin@hestim.ma`
- Mot de passe exact : `admin123`
- Sélectionner le bon rôle : "Administrateur"

---

## 🎯 CHECKLIST AVANT LA VIDÉO

- [ ] Tous les fichiers sont dans le même dossier
- [ ] `auth-system.js` est présent
- [ ] `data-manager.js` est présent
- [ ] Navigateur à jour (Chrome/Firefox recommandé)
- [ ] localStorage vide (pour démarrer proprement)
- [ ] Liste des 3 comptes par défaut à portée de main

---

## 📞 AIDE RAPIDE

### Comptes par Défaut
```
Admin:      admin@hestim.ma      / admin123
Enseignant: enseignant@hestim.ma / prof123
Étudiant:   etudiant@hestim.ma   / etud123
```

### Console Debug
Ouvrir la console (F12) et taper :
```javascript
// Voir toutes les données
showEduHestimData()

// Voir les comptes
authSystem.getAllAccounts()

// Voir les demandes
dataManager.getDemandes()

// Réinitialiser tout
localStorage.clear()
location.reload()
```

---

## ✨ RÉSUMÉ EN 3 POINTS

1. **3 comptes par défaut** → Admin peut en créer d'autres
2. **Demandes fonctionnelles** → Étudiant demande → Admin traite → Étudiant notifié
3. **Gestion complète** → Salles, classes, utilisateurs, tout fonctionne !

---

## 🎬 PRÊT POUR LA VIDÉO !

Tout est prêt, tout fonctionne, aucune erreur. Suis le scénario et ça sera parfait ! 🚀

**Bonne chance pour ta vidéo ! 🎉**
