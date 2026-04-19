const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    nom:          { type: String, required: true },
    prenom:       { type: String, required: true },
    email:        { type: String, required: true, unique: true },
    password:     { type: String, required: true },
    role:         { type: String, enum: ['etudiant', 'enseignant', 'administrateur'], required: true },
    classe:       { type: String, default: null },
    departement:  { type: String, default: null },
    annee:        { type: String, default: null },
    matiere:      { type: String, default: null },
}, { timestamps: true });

module.exports = mongoose.model('User', UserSchema);
