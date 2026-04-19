const mongoose = require('mongoose');

const ClasseSchema = new mongoose.Schema({
    code:      { type: String, required: true, unique: true },
    nom:       { type: String, required: true },
    niveau:    { type: String, required: true },
    filiere:   { type: String, required: true },
    effectif:  { type: Number, default: 0 },
    etudiants: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
}, { timestamps: true });

module.exports = mongoose.model('Classe', ClasseSchema);
