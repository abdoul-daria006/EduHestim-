const mongoose = require('mongoose');

const SalleSchema = new mongoose.Schema({
    nom:         { type: String, required: true },
    batiment:    { type: String, required: true },
    type:        { type: String, enum: ['Normale', 'Informatique', 'Amphithéâtre', 'Laboratoire'], default: 'Normale' },
    capacite:    { type: Number, required: true },
    equipements: [{ type: String }],
    disponible:  { type: Boolean, default: true },
}, { timestamps: true });

module.exports = mongoose.model('Salle', SalleSchema);
