const router = require('express').Router();
const Notification = require('../models/Notification');
const authMiddleware = require('../middleware/auth');

router.get('/user/:userId', authMiddleware, async (req, res) => {
    try {
        const notifs = await Notification.find({
            $or: [{ userId: req.params.userId }, { userId: null }]
        }).sort({ createdAt: -1 });
        res.json(notifs);
    } catch (err) { res.status(500).json({ message: err.message }); }
});

router.put('/:id/read', authMiddleware, async (req, res) => {
    try {
        res.json(await Notification.findByIdAndUpdate(req.params.id, { lu: true }, { new: true }));
    } catch (err) { res.status(500).json({ message: err.message }); }
});

module.exports = router;
