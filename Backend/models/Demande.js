const mongoose = require('mongoose');

const DemandeSchema = new mongoose.Schema({
    userId:            { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    userName:          { type: String, required: true },
    userRole:          { type: String, required: true },
    salle:             { type: String, required: true },
    date:              { type: String, required: true },
    heureDebut:        { type: String, required: true },
    heureFin:          { type: String, required: true },
    motif:             { type: String, required: true },
    statut:            { type: String, enum: ['en_attente', 'approuve', 'refuse'], default: 'en_attente' },
    dateTraitement:    { type: Date, default: null },
    commentaireAdmin:  { type: String, default: null },
    traitePar:         { type: String, default: null },
}, { timestamps: true });

module.exports = mongoose.model('Demande', DemandeSchema);
