const router = require('express').Router();
const EmploiDuTemps = require('../models/EmploiDuTemps');
const authMiddleware = require('../middleware/auth');

router.get('/',              authMiddleware, async (req, res) => { try { res.json(await EmploiDuTemps.find()); } catch (err) { res.status(500).json({ message: err.message }); } });
router.get('/classe/:code',  authMiddleware, async (req, res) => { try { res.json(await EmploiDuTemps.find({ classeCode: req.params.code })); } catch (err) { res.status(500).json({ message: err.message }); } });
router.post('/',             authMiddleware, async (req, res) => { try { res.status(201).json(await EmploiDuTemps.create(req.body)); } catch (err) { res.status(500).json({ message: err.message }); } });
router.put('/:id',           authMiddleware, async (req, res) => { try { res.json(await EmploiDuTemps.findByIdAndUpdate(req.params.id, req.body, { new: true })); } catch (err) { res.status(500).json({ message: err.message }); } });
router.delete('/:id',        authMiddleware, async (req, res) => { try { await EmploiDuTemps.findByIdAndDelete(req.params.id); res.json({ message: 'Cours supprimé' }); } catch (err) { res.status(500).json({ message: err.message }); } });

module.exports = router;
