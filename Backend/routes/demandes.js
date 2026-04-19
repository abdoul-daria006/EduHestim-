const router = require('express').Router();
const Demande = require('../models/Demande');
const Notification = require('../models/Notification');
const authMiddleware = require('../middleware/auth');

// GET toutes les demandes
router.get('/', authMiddleware, async (req, res) => {
    try {
        const filter = req.query.statut ? { statut: req.query.statut } : {};
        res.json(await Demande.find(filter).sort({ createdAt: -1 }));
    } catch (err) { res.status(500).json({ message: err.message }); }
});

// GET demandes d'un user
router.get('/user/:userId', authMiddleware, async (req, res) => {
    try {
        res.json(await Demande.find({ userId: req.params.userId }).sort({ createdAt: -1 }));
    } catch (err) { res.status(500).json({ message: err.message }); }
});

// POST créer une demande
router.post('/', authMiddleware, async (req, res) => {
    try {
        const demande = await Demande.create(req.body);
        await Notification.create({
            userId: null,
            titre: 'Nouvelle demande de réservation',
            message: `${req.body.userName} demande ${req.body.salle} le ${req.body.date}`,
            type: 'info'
        });
        res.status(201).json(demande);
    } catch (err) { res.status(500).json({ message: err.message }); }
});

// PUT approuver
router.put('/:id/approuver', authMiddleware, async (req, res) => {
    try {
        const demande = await Demande.findByIdAndUpdate(req.params.id, {
            statut: 'approuve',
            dateTraitement: new Date(),
            traitePar: req.body.adminName,
            commentaireAdmin: req.body.commentaire || 'Demande approuvée'
        }, { new: true });

        await Notification.create({
            userId: demande.userId,
            titre: 'Demande approuvée ✅',
            message: `Votre réservation de ${demande.salle} pour le ${demande.date} a été approuvée`,
            type: 'success'
        });

        res.json(demande);
    } catch (err) { res.status(500).json({ message: err.message }); }
});

// PUT refuser
router.put('/:id/refuser', authMiddleware, async (req, res) => {
    try {
        const demande = await Demande.findByIdAndUpdate(req.params.id, {
            statut: 'refuse',
            dateTraitement: new Date(),
            traitePar: req.body.adminName,
            commentaireAdmin: req.body.commentaire
        }, { new: true });

        await Notification.create({
            userId: demande.userId,
            titre: 'Demande refusée ❌',
            message: `Votre réservation de ${demande.salle} a été refusée. Raison: ${req.body.commentaire}`,
            type: 'error'
        });

        res.json(demande);
    } catch (err) { res.status(500).json({ message: err.message }); }
});

// DELETE
router.delete('/:id', authMiddleware, async (req, res) => {
    try {
        await Demande.findByIdAndDelete(req.params.id);
        res.json({ message: 'Demande supprimée' });
    } catch (err) { res.status(500).json({ message: err.message }); }
});

module.exports = router;
