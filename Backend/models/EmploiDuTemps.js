const mongoose = require('mongoose');

const EmploiDuTempsSchema = new mongoose.Schema({
    classeId:      { type: mongoose.Schema.Types.ObjectId, ref: 'Classe' },
    classeCode:    { type: String, required: true },
    jour:          { type: String, enum: ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'], required: true },
    heureDebut:    { type: String, required: true },
    heureFin:      { type: String, required: true },
    matiere:       { type: String, required: true },
    enseignantId:  { type: mongoose.Schema.Types.ObjectId, ref: 'User', default: null },
    enseignantNom: { type: String, default: null },
    salle:         { type: String, required: true },
    type:          { type: String, enum: ['CM', 'TD', 'TP'], default: 'CM' },
}, { timestamps: true });

module.exports = mongoose.model('EmploiDuTemps', EmploiDuTempsSchema);
