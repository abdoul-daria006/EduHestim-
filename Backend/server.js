const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors({ origin: '*' }));
app.use(express.json());

// Routes
app.use('/api/auth',        require('./routes/auth'));
app.use('/api/users',       require('./routes/users'));
app.use('/api/salles',      require('./routes/salles'));
app.use('/api/classes',     require('./routes/classes'));
app.use('/api/demandes',    require('./routes/demandes'));
app.use('/api/emplois',     require('./routes/emplois'));
app.use('/api/notifications', require('./routes/notifications'));
app.use('/api/analyse', require('./routes/analyse'));

// Route test
app.get('/', (req, res) => {
    res.json({ message: '✅ EduHestim API is running !' });
});

// Connexion MongoDB
mongoose.connect(process.env.MONGODB_URI)
    .then(() => {
        console.log('✅ MongoDB connecté');
        app.listen(process.env.PORT, () => {
            console.log(`🚀 Serveur lancé sur http://localhost:${process.env.PORT}`);
        });
    })
    .catch(err => {
        console.error('❌ Erreur MongoDB :', err.message);
    });
