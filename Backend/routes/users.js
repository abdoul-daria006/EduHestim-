const router = require('express').Router();
const bcrypt = require('bcryptjs');
const User = require('../models/User');
const authMiddleware = require('../middleware/auth');

// GET /api/users
router.get('/', authMiddleware, async (req, res) => {
    try {
        const users = await User.find().select('-password');
        res.json(users);
    } catch (err) { res.status(500).json({ message: err.message }); }
});

// GET /api/users/stats
router.get('/stats', authMiddleware, async (req, res) => {
    try {
        const total = await User.countDocuments();
        const etudiants = await User.countDocuments({ role: 'etudiant' });
        const enseignants = await User.countDocuments({ role: 'enseignant' });
        const admins = await User.countDocuments({ role: 'administrateur' });
        res.json({ total, etudiants, enseignants, admins });
    } catch (err) { res.status(500).json({ message: err.message }); }
});

// GET /api/users/:id
router.get('/:id', authMiddleware, async (req, res) => {
    try {
        const user = await User.findById(req.params.id).select('-password');
        if (!user) return res.status(404).json({ message: 'Utilisateur non trouvé' });
        res.json(user);
    } catch (err) { res.status(500).json({ message: err.message }); }
});

// PUT /api/users/:id
router.put('/:id', authMiddleware, async (req, res) => {
    try {
        if (req.body.password) {
            req.body.password = await bcrypt.hash(req.body.password, 10);
        }
        const user = await User.findByIdAndUpdate(req.params.id, req.body, { new: true }).select('-password');
        res.json(user);
    } catch (err) { res.status(500).json({ message: err.message }); }
});

// DELETE /api/users/:id
router.delete('/:id', authMiddleware, async (req, res) => {
    try {
        await User.findByIdAndDelete(req.params.id);
        res.json({ message: 'Utilisateur supprimé' });
    } catch (err) { res.status(500).json({ message: err.message }); }
});

module.exports = router;
