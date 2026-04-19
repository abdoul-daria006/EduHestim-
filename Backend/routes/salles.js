const router = require('express').Router();
const Salle = require('../models/Salle');
const authMiddleware = require('../middleware/auth');

router.get('/',        authMiddleware, async (req, res) => { try { res.json(await Salle.find()); } catch (err) { res.status(500).json({ message: err.message }); } });
router.get('/:id',     authMiddleware, async (req, res) => { try { const s = await Salle.findById(req.params.id); if (!s) return res.status(404).json({ message: 'Salle non trouvée' }); res.json(s); } catch (err) { res.status(500).json({ message: err.message }); } });
router.post('/',       authMiddleware, async (req, res) => { try { res.status(201).json(await Salle.create(req.body)); } catch (err) { res.status(500).json({ message: err.message }); } });
router.put('/:id',     authMiddleware, async (req, res) => { try { res.json(await Salle.findByIdAndUpdate(req.params.id, req.body, { new: true })); } catch (err) { res.status(500).json({ message: err.message }); } });
router.delete('/:id',  authMiddleware, async (req, res) => { try { await Salle.findByIdAndDelete(req.params.id); res.json({ message: 'Salle supprimée' }); } catch (err) { res.status(500).json({ message: err.message }); } });

module.exports = router;
