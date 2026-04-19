const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
require('dotenv').config();

const User = require('./models/User');
const Salle = require('./models/Salle');
const Classe = require('./models/Classe');
const EmploiDuTemps = require('./models/EmploiDuTemps');

async function seed() {
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ MongoDB connecté');

    // Vider les collections
    await User.deleteMany();
    await Salle.deleteMany();
    await Classe.deleteMany();
    await EmploiDuTemps.deleteMany();

    // Créer les users
    const users = await User.insertMany([
        { nom: 'ALLIMAN', prenom: 'Maurane', email: 'maurane.alliman@hestim.ma', password: await bcrypt.hash('123456', 10), role: 'etudiant', classe: '3A-INFO', departement: 'Génie Informatique', annee: '3ème année' },
        { nom: 'BETHIO', prenom: 'Maurane', email: 'maurane.bethio@hestim.ma', password: await bcrypt.hash('123456', 10), role: 'enseignant', departement: 'Informatique', matiere: 'POO' },
        { nom: 'ADMIN', prenom: 'Principal', email: 'admin@hestim.ma', password: await bcrypt.hash('admin123', 10), role: 'administrateur', departement: 'Administration' },
    ]);

    // Créer les salles
    await Salle.insertMany([
        { nom: 'Ghandi S01', batiment: 'Ghandi', type: 'Normale', capacite: 30, equipements: ['Projecteur', 'Tableau'] },
        { nom: 'Ghandi S05', batiment: 'Ghandi', type: 'Normale', capacite: 25, equipements: ['Projecteur', 'Tableau', 'Climatisation'] },
        { nom: 'Ghandi Info 1', batiment: 'Ghandi', type: 'Informatique', capacite: 40, equipements: ['40 PC', 'Projecteur', 'Climatisation'] },
        { nom: 'Stendhal Amphi C', batiment: 'Stendhal', type: 'Amphithéâtre', capacite: 120, equipements: ['Projecteur', 'Sonorisation', 'Climatisation'] },
    ]);

    // Créer les classes
    const etudiant = users.find(u => u.role === 'etudiant');
    await Classe.insertMany([
        { code: '1A-INFO', nom: '1ère Année Informatique', niveau: '1A', filiere: 'Génie Informatique', effectif: 45 },
        { code: '2A-INFO', nom: '2ème Année Informatique', niveau: '2A', filiere: 'Génie Informatique', effectif: 42 },
        { code: '3A-INFO', nom: '3ème Année Informatique', niveau: '3A', filiere: 'Génie Informatique', effectif: 38, etudiants: [etudiant._id] },
    ]);

    // Créer emploi du temps
    const enseignant = users.find(u => u.role === 'enseignant');
    await EmploiDuTemps.create({
        classeCode: '3A-INFO',
        jour: 'Lundi',
        heureDebut: '08:00',
        heureFin: '10:00',
        matiere: 'Statistiques',
        enseignantId: enseignant._id,
        enseignantNom: `Prof. ${enseignant.nom} ${enseignant.prenom}`,
        salle: 'Stendhal Amphi C',
        type: 'CM'
    });

    console.log('🌱 Base de données peuplée avec succès !');
    console.log('👤 Comptes créés :');
    console.log('   Étudiant  → maurane.alliman@hestim.ma / 123456');
    console.log('   Enseignant→ maurane.bethio@hestim.ma  / 123456');
    console.log('   Admin     → admin@hestim.ma           / admin123');
    
    mongoose.disconnect();
}

seed().catch(console.error);
