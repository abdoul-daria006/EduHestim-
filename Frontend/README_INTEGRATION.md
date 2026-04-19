# 📚 GUIDE D'INTÉGRATION COMPLÈTE - EDUHESTIM

## 🎯 OBJECTIF
Transformer votre projet statique en une application web dynamique et synchronisée avec gestion centralisée des données.

## 📦 FICHIERS FOURNIS

### Fichiers Core (Essentiels)
1. **data-manager.js** - Système de gestion centralisé
2. **GestionClasses.html** - Page de gestion des classes
3. **admindash.html** - Dashboard admin corrigé
4. **Fairedesdemandes_updated.html** - Formulaire de demande avec synchronisation

### Fichiers Documentation
5. **CORRECTIONS_RAPPORT.md** - Rapport détaillé des corrections
6. **README_INTEGRATION.md** - Ce fichier
7. **GUIDE_UTILISATION.md** - Guide d'utilisation pour la soutenance

## ⚡ INTÉGRATION RAPIDE (10 MINUTES)

### Étape 1: Copier les fichiers
```bash
# Copier data-manager.js dans votre répertoire principal
cp data-manager.js /votre/projet/

# Copier les fichiers HTML corrigés
cp admindash.html /votre/projet/
cp GestionClasses.html /votre/projet/
cp Fairedesdemandes_updated.html /votre/projet/Fairedesdemandes.html
```

### Étape 2: Ajouter data-manager.js dans TOUS les fichiers HTML

Ajoutez cette ligne AVANT la balise `</body>` dans chaque fichier HTML:
```html
<script src="data-manager.js"></script>
```

**Liste des fichiers à modifier**:
- [ ] Connexion.html
- [ ] admindash.html
- [ ] Etudiantdash.html
- [ ] Enseignantdash.html
- [ ] Emploiedutemps.html
- [ ] EmploiedutempsEnseignant.html
- [ ] Fairedesdemandes.html
- [ ] FairedesdemandesEnseignant.html
- [ ] GestionDemandes-Admin.html
- [ ] GestiondesalleAdmin.html
- [ ] GestionClasses.html
- [ ] Mesreservations.html
- [ ] MesreservationsEnseignant.html
- [ ] NotifAdmin.html
- [ ] NotifEnseignant.html
- [ ] NotifEtudiant.html
- [ ] PagelistedesUtilisateurs.html
- [ ] ProfilAdmin.html
- [ ] ProfilEnseignant.html
- [ ] Profiletudiant.html

### Étape 3: Modifier les 3 fichiers critiques

#### A. Modifier `Fairedesdemandes.html`
Remplacer la section de soumission du formulaire:

**AVANT**:
```javascript
form.addEventListener('submit', function(e) {
    e.preventDefault();
    // Code existant...
    alert('Demande envoyée');
});
```

**APRÈS**:
```javascript
form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const userName = sessionStorage.getItem('userName') || 'Étudiant';
    const userEmail = sessionStorage.getItem('userEmail') || 'etudiant@hestim.ma';
    
    dataManager.addDemande({
        demandeur: userName,
        demandeurEmail: userEmail,
        typeDemandeur: 'etudiant',
        salle: document.getElementById('salle').options[document.getElementById('salle').selectedIndex].text,
        salleId: parseInt(document.getElementById('salle').value),
        date: document.getElementById('dateReservation').value,
        heureDebut: document.getElementById('heureDebut').value,
        heureFin: document.getElementById('heureFin').value,
        motif: document.getElementById('motif').value
    });
    
    alert('✓ Demande envoyée avec succès!');
    form.reset();
});
```

#### B. Modifier `GestionDemandes-Admin.html`
Ajouter au chargement de la page:

```javascript
<script>
// Charger les demandes réelles
function loadDemandes() {
    const demandes = dataManager.getDemandes('en_attente');
    // Afficher les demandes dans l'interface
    console.log('Demandes en attente:', demandes);
}

// Fonction d'approbation
function handleApprove(demandeId) {
    dataManager.updateDemandeStatut(demandeId, 'approuvee');
    loadDemandes();
    alert('✓ Demande approuvée!');
}

// Fonction de refus
function handleReject(demandeId) {
    const commentaire = prompt('Motif du refus (optionnel):');
    dataManager.updateDemandeStatut(demandeId, 'refusee', commentaire);
    loadDemandes();
    alert('✗ Demande refusée');
}

// Charger au démarrage
loadDemandes();

// Recharger quand les données changent
window.addEventListener('eduHestimDataUpdated', loadDemandes);
</script>
```

#### C. Modifier les pages de notifications
Ajouter dans `NotifEtudiant.html`, `NotifEnseignant.html`, `NotifAdmin.html`:

```javascript
<script>
function loadNotifications() {
    const userRole = sessionStorage.getItem('userRole') || 'etudiants';
    const userEmail = sessionStorage.getItem('userEmail');
    
    const notifications = dataManager.getNotifications(userRole, userEmail);
    
    console.log('Notifications:', notifications);
    // Afficher les notifications dans l'interface
}

loadNotifications();
window.addEventListener('eduHestimDataUpdated', loadNotifications);
</script>
```

## 🔧 MODIFICATIONS AVANCÉES (Optionnel)

### Dashboard Admin avec stats réelles

```javascript
function updateStats() {
    const stats = dataManager.getStats();
    
    document.querySelector('.stat-etudiants').textContent = stats.totalEtudiants;
    document.querySelector('.stat-enseignants').textContent = stats.totalEnseignants;
    document.querySelector('.stat-salles').textContent = stats.totalSalles;
    document.querySelector('.stat-demandes').textContent = stats.demandesEnAttente;
    document.querySelector('.stat-conflits').textContent = stats.totalConflits;
}

updateStats();
window.addEventListener('eduHestimDataUpdated', updateStats);
```

### Détection automatique des conflits

Dans `admindash.html`:
```javascript
function detectAndShowConflits() {
    const conflits = dataManager.detectConflits();
    if (conflits.length > 0) {
        console.log('⚠️ Conflits détectés:', conflits);
        // Afficher les conflits dans l'interface
    }
}

detectAndShowConflits();
```

## 🎨 PERSONNALISATION DES DONNÉES INITIALES

Pour ajouter des données de démonstration, modifiez `data-manager.js`:

```javascript
initializeData() {
    if (!localStorage.getItem('eduHestim_initialized')) {
        const initialData = {
            users: {
                etudiants: [
                    {
                        id: 1,
                        nom: 'ALLIMAN',
                        prenom: 'Maurane',
                        email: 'maurane.alliman@hestim.ma',
                        classe: '3ème année GI'
                    }
                ],
                enseignants: [
                    {
                        id: 1,
                        nom: 'BETHIO',
                        prenom: 'Maurane',
                        email: 'bethio@hestim.ma',
                        specialite: 'POO'
                    }
                ],
                administrateurs: []
            },
            salles: this.getDefaultSalles(),
            // ... reste des données
        };
        
        localStorage.setItem('eduHestim_data', JSON.stringify(initialData));
        localStorage.setItem('eduHestim_initialized', 'true');
    }
}
```

## ✅ CHECKLIST DE VÉRIFICATION

### Avant la soutenance:

- [ ] data-manager.js est dans le répertoire racine
- [ ] Tous les fichiers HTML incluent `<script src="data-manager.js"></script>`
- [ ] Le formulaire de demandes utilise `dataManager.addDemande()`
- [ ] La gestion des demandes utilise `dataManager.updateDemandeStatut()`
- [ ] Les notifications utilisent `dataManager.getNotifications()`
- [ ] Le dashboard admin affiche les vraies statistiques
- [ ] Tester la synchronisation entre onglets:
  - [ ] Ouvrir admin dans onglet 1
  - [ ] Ouvrir étudiant dans onglet 2
  - [ ] Créer demande en tant qu'étudiant
  - [ ] Vérifier que la demande apparaît dans admin
  - [ ] Approuver la demande
  - [ ] Vérifier la notification chez l'étudiant

## 🚀 DÉMONSTRATION POUR LA SOUTENANCE

### Scénario complet à montrer:

1. **Connexion en tant qu'étudiant**
   - Aller sur Fairedesdemandes.html
   - Remplir une demande de salle
   - Soumettre

2. **Connexion en tant qu'admin**
   - Ouvrir admindash.html
   - Voir la nouvelle demande apparaître
   - Voir la notification
   - Voir les statistiques mises à jour

3. **Traitement de la demande**
   - Cliquer sur "Approuver"
   - Montrer que la réservation est créée automatiquement

4. **Retour à l'étudiant**
   - Ouvrir NotifEtudiant.html
   - Voir la notification d'approbation
   - Aller sur Mesreservations.html
   - Voir la réservation confirmée

5. **Détection de conflits** (Bonus)
   - Créer deux demandes pour la même salle au même moment
   - Montrer la détection automatique du conflit

## ⚠️ PROBLÈMES COURANTS ET SOLUTIONS

### Problème 1: Les données ne persistent pas
**Solution**: Vérifier que localStorage est activé dans le navigateur

### Problème 2: Les notifications n'apparaissent pas
**Solution**: Vérifier que sessionStorage contient bien userRole et userEmail

### Problème 3: La synchronisation ne fonctionne pas entre onglets
**Solution**: Utiliser l'événement storage de localStorage (à implémenter si nécessaire)

### Problème 4: Les salles ne s'affichent pas
**Solution**: Vérifier que data-manager.js est chargé AVANT le script de la page

## 📞 SUPPORT

En cas de problème:
1. Vérifier la console du navigateur (F12)
2. Vérifier que data-manager.js est bien chargé
3. Vérifier localStorage: `localStorage.getItem('eduHestim_data')`

## 🎓 POUR ALLER PLUS LOIN

Après la soutenance, vous pouvez:
- Ajouter une vraie base de données (Firebase, MongoDB)
- Implémenter WebSockets pour la synchronisation temps réel
- Ajouter l'authentification réelle
- Créer une API REST backend
- Ajouter des graphiques avec Chart.js
- Implémenter l'export PDF des emplois du temps

---


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


