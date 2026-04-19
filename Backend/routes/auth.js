const router = require('express').Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

// POST /api/auth/login
router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        const user = await User.findOne({ email });
        if (!user) return res.status(400).json({ message: 'Email ou mot de passe incorrect' });

        const valid = await bcrypt.compare(password, user.password);
        if (!valid) return res.status(400).json({ message: 'Email ou mot de passe incorrect' });

        const token = jwt.sign(
            { id: user._id, role: user.role },
            process.env.JWT_SECRET,
            { expiresIn: process.env.JWT_EXPIRE }
        );

        res.json({
            token,
            user: { id: user._id, nom: user.nom, prenom: user.prenom, email: user.email, role: user.role }
        });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// POST /api/auth/register
router.post('/register', async (req, res) => {
    try {
        const { nom, prenom, email, password, role, classe, departement, annee, matiere } = req.body;
        const exists = await User.findOne({ email });
        if (exists) return res.status(400).json({ message: 'Email déjà utilisé' });

        const hashed = await bcrypt.hash(password, 10);
        const user = await User.create({ nom, prenom, email, password: hashed, role, classe, departement, annee, matiere });

        res.status(201).json({ message: 'Utilisateur créé', user });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;
