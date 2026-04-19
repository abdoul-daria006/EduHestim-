# 🎓 GUIDE DE PRÉSENTATION - SOUTENANCE EDUHESTIM

## 📋 PLAN DE PRÉSENTATION (15-20 MINUTES)

### 1. INTRODUCTION (2 minutes)
**À dire:**
"Bonjour, nous allons vous présenter EduHestim, une plateforme intelligente de gestion et réservation de salles pour établissements académiques. Notre solution permet la planification automatique des cours, la gestion des réservations et la synchronisation en temps réel des emplois du temps."

**Problématiques adressées:**
- ✅ Conflits d'horaires et double-réservations
- ✅ Gestion manuelle chronophage
- ✅ Manque de communication entre admin, enseignants et étudiants
- ✅ Difficulté à visualiser les disponibilités

### 2. ARCHITECTURE DU SYSTÈME (3 minutes)

**À montrer:**
```
┌─────────────────────────────────────┐
│      EDUHESTIM ARCHITECTURE         │
├─────────────────────────────────────┤
│                                     │
│  [Administrateur] [Enseignant] [Étudiant]
│         │              │           │
│         └──────────────┴───────────┘
│                   │
│         ┌─────────▼─────────┐
│         │   data-manager.js │  ← Système centralisé
│         │   (localStorage)  │
│         └───────────────────┘
│                   │
│         ┌─────────▼─────────┐
│         │  Synchronisation  │
│         │   automatique     │
│         └───────────────────┘
│
└─────────────────────────────────────┘
```

**Points clés:**
- Gestion centralisée avec localStorage
- Synchronisation automatique via événements
- Notifications en temps réel
- Détection automatique des conflits

### 3. DÉMONSTRATION PRATIQUE (10 minutes)

#### SCÉNARIO 1: Étudiant fait une demande (2 min)

**Actions à faire:**
1. Ouvrir `Connexion.html`
2. Se connecter en tant qu'étudiant
   - Email: etudiant@hestim.ma
   - Type: Étudiant
3. Aller sur "Faire une Demande"
4. Remplir le formulaire:
   - Salle: Ghandi Salle 08
   - Date: [demain]
   - Heure: 14:00 - 16:00
   - Motif: "Réunion projet fin d'études"
5. Soumettre

**À dire:**
"Lorsqu'un étudiant soumet une demande, celle-ci est instantanément enregistrée dans notre système centralisé et une notification est automatiquement envoyée à l'administrateur."

**Montrer dans la console (F12):**
```javascript
// Dans la console:
dataManager.getDemandes()
// Voir la demande qui vient d'être créée
```

#### SCÉNARIO 2: Admin traite la demande (3 min)

**Actions à faire:**
1. **Sans fermer l'onglet étudiant**, ouvrir un nouvel onglet
2. Ouvrir `Connexion.html` dans ce nouvel onglet
3. Se connecter en tant qu'admin
4. Aller sur le Dashboard Admin
5. Montrer la demande dans la section "Demandes Prioritaires"
6. Cliquer sur "✓ Approuver"

**À dire:**
"L'administrateur voit immédiatement la nouvelle demande. Lorsqu'il l'approuve, plusieurs actions automatiques se déclenchent:
- Création d'une réservation
- Envoi de notification à l'étudiant
- Mise à jour de la disponibilité de la salle
- Vérification des conflits potentiels"

**Montrer dans la console:**
```javascript
// Voir la réservation créée automatiquement
dataManager.getReservations()

// Voir la notification envoyée
dataManager.getNotifications('etudiants')
```

#### SCÉNARIO 3: Étudiant reçoit la confirmation (2 min)

**Actions à faire:**
1. Retourner sur l'onglet étudiant (sans rafraîchir)
2. Aller sur "Notifications"
3. Montrer la notification d'approbation
4. Aller sur "Mes Réservations"
5. Montrer la réservation confirmée

**À dire:**
"L'étudiant reçoit instantanément la notification d'approbation et peut voir sa réservation confirmée. Tout cela sans rafraîchir la page, grâce à notre système de synchronisation en temps réel."

#### SCÉNARIO 4: Détection de conflits (3 min)

**Actions à faire:**
1. Créer une 2ème demande pour la **même salle**, **même date**, **même heure**
2. Retourner sur admin
3. Approuver cette 2ème demande
4. Dans la console admin:

```javascript
const conflits = dataManager.detectConflits();
console.log('Conflits détectés:', conflits);
```

**À dire:**
"Notre système détecte automatiquement les conflits de réservation. Ici, nous voyons que deux cours ont été programmés dans la même salle au même moment. L'admin est immédiatement alerté et peut résoudre le problème."

### 4. FONCTIONNALITÉS CLÉS (3 minutes)

**Parcourir rapidement:**

#### A. Gestion des Classes
- Ouvrir `GestionClasses.html`
- Montrer l'interface de création de classe
- Créer une classe exemple:
  - Nom: "3ème année Génie Informatique - Groupe A"
  - Niveau: 3ème année
  - Spécialité: Génie Informatique
  - Effectif: 35
- Montrer la carte créée

#### B. Gestion des Salles
- Ouvrir `GestiondesalleAdmin.html`
- Montrer la liste des salles avec leur statut
- Expliquer le système de disponibilité

#### C. Emplois du Temps
- Ouvrir `Emploiedutemps.html` (étudiant)
- Montrer la vue semaine/jour/mois
- Expliquer les couleurs (CM, TD, TP)

### 5. POINTS TECHNIQUES FORTS (2 minutes)

**À mentionner:**

1. **Architecture Modulaire**
   - Séparation claire entre présentation et logique
   - Système de gestion centralisé réutilisable

2. **Synchronisation Temps Réel**
   ```javascript
   // Événement personnalisé
   window.dispatchEvent(new CustomEvent('eduHestimDataUpdated'));
   ```

3. **Gestion Intelligente des Données**
   - Validation côté client
   - Détection automatique des conflits
   - Statistiques en temps réel

4. **Interface Utilisateur**
   - Design responsive
   - Navigation intuitive
   - Feedback visuel immédiat

### 6. CONCLUSION & PERSPECTIVES (2 minutes)

**Réalisations:**
- ✅ Système complet et fonctionnel
- ✅ 3 interfaces utilisateurs (Admin, Enseignant, Étudiant)
- ✅ Gestion centralisée des données
- ✅ Synchronisation en temps réel
- ✅ Détection automatique des conflits
- ✅ 20+ pages interconnectées

**Perspectives d'amélioration:**
- 🔄 Base de données backend (Firebase/MongoDB)
- 🔄 API REST pour l'interconnexion
- 🔄 Authentification sécurisée
- 🔄 Export PDF des emplois du temps
- 🔄 Notifications push
- 🔄 Application mobile

## 📊 DONNÉES DE DÉMONSTRATION À AVOIR

Avant la soutenance, dans la console du navigateur:

```javascript
// Réinitialiser et charger les données de démo
localStorage.clear();

// Créer des utilisateurs de démo
dataManager.addUser('etudiants', {
    nom: 'ALLIMAN',
    prenom: 'Maurane',
    email: 'maurane.alliman@hestim.ma',
    classe: '3ème année GI'
});

dataManager.addUser('enseignants', {
    nom: 'BETHIO',
    prenom: 'Maurane',
    email: 'bethio@hestim.ma',
    specialite: 'POO'
});

// Créer une classe
dataManager.addClass({
    nom: '3ème année Génie Informatique',
    niveau: '3ème année',
    specialite: 'Génie Informatique',
    effectif: 35,
    responsable: 'Prof. NANA Cheikh',
    anneeAcademique: '2024-2025'
});

// Vérifier
console.log('Données prêtes:', dataManager.getData());
```

## ⚠️ CONSEILS IMPORTANTS

### AVANT LA SOUTENANCE:
1. Tester TOUT le scénario 2-3 fois
2. Avoir plusieurs onglets ouverts et prêts
3. Vider localStorage pour recommencer à zéro:
   ```javascript
   localStorage.clear();
   location.reload();
   ```

### PENDANT LA SOUTENANCE:
- Parler clairement et pas trop vite
- Montrer la console pour prouver que ça fonctionne vraiment
- Si quelque chose ne marche pas, expliquer ce qui devrait se passer
- Mettre en avant l'aspect "temps réel" et "synchronisé"

### QUESTIONS POTENTIELLES DU JURY:

**Q: Pourquoi localStorage et pas une vraie base de données?**
R: "Pour ce prototype, localStorage permet de démontrer toute la logique métier sans infrastructure serveur. Pour la production, nous migrerions vers Firebase ou MongoDB."

**Q: Comment gérez-vous la sécurité?**
R: "Actuellement, c'est un prototype de démonstration. En production, nous implémenterions JWT pour l'authentification, HTTPS obligatoire, et hachage des mots de passe avec bcrypt."

**Q: La synchronisation fonctionne-t-elle vraiment entre utilisateurs?**
R: "Dans ce prototype, elle fonctionne entre onglets du même navigateur grâce à localStorage. Pour une vraie synchronisation multi-utilisateurs, nous utiliserions WebSockets ou Firebase Realtime Database."

**Q: Avez-vous géré les cas d'erreur?**
R: "Oui, nous avons des try-catch, des validations de formulaire, et des messages d'erreur clairs. Par exemple..." [Montrer un exemple]

## 🎯 OBJECTIFS À ATTEINDRE

À la fin de la présentation, le jury doit:
- ✅ Comprendre l'architecture du système
- ✅ Avoir vu la synchronisation en action
- ✅ Être impressionné par la détection de conflits
- ✅ Reconnaître le travail de conception UI/UX
- ✅ Voir le potentiel du projet

## 🚀 PHRASE DE CONCLUSION

"En conclusion, EduHestim démontre qu'une gestion intelligente des ressources académiques est possible avec les technologies web modernes. Notre système résout les problématiques de planification, évite les conflits, et améliore la communication entre tous les acteurs. Merci pour votre attention, nous sommes prêts à répondre à vos questions."

---

**🎉 Vous êtes prêt! Bonne chance!**


# Les USER
eldak@hestim.ma ==> eldak123
abdoul@hestim.ma ==> Abdoul123
agba@hestim.ma ==> agba123

Pour lancer le serveur : node server.js

Sécurité : chaque document faker a source: "faker_dataset" — donc pour tout supprimer plus tard sans toucher à tes vraies données :
db.users.deleteMany({ source: "faker_dataset" })

# Pour lancer l'application :
Terminal 1 - Backend

C:\Users\adm\Desktop\Projet_Pacte_3A-IIIA\Backend
node server.js


Terminal 2 — Frontend
C:\Users\adm\Desktop\Projet_Pacte_3A-IIIA\Frontend
# Ouvre simplement le fichier dans le navigateur
start index.html
```
> Ou ouvre directement `index.html` avec **Live Server** dans VS Code (clic droit → Open with Live Server)

📁 Backend/   → node server.js        (port 5000)
📁 Frontend/  → Live Server / browser (port 5500)
🍃 MongoDB    → service Windows       (port 27017)

# Pour lancer Notebook Jupyter : 
cd C:\Users\adm\Desktop\Projet_Pacte_3A-IIIA\Frontend\data-analysis
jupyter notebook eduhestim_analyse.ipynb

