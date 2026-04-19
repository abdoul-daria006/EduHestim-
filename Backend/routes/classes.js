const router = require('express').Router();
const Classe = require('../models/Classe');
const authMiddleware = require('../middleware/auth');

router.get('/',       authMiddleware, async (req, res) => { try { res.json(await Classe.find().populate('etudiants', '-password')); } catch (err) { res.status(500).json({ message: err.message }); } });
router.get('/:id',    authMiddleware, async (req, res) => { try { const c = await Classe.findById(req.params.id).populate('etudiants', '-password'); if (!c) return res.status(404).json({ message: 'Classe non trouvée' }); res.json(c); } catch (err) { res.status(500).json({ message: err.message }); } });
router.post('/',      authMiddleware, async (req, res) => { try { res.status(201).json(await Classe.create(req.body)); } catch (err) { res.status(500).json({ message: err.message }); } });
router.put('/:id',    authMiddleware, async (req, res) => { try { res.json(await Classe.findByIdAndUpdate(req.params.id, req.body, { new: true })); } catch (err) { res.status(500).json({ message: err.message }); } });
router.delete('/:id', authMiddleware, async (req, res) => { try { await Classe.findByIdAndDelete(req.params.id); res.json({ message: 'Classe supprimée' }); } catch (err) { res.status(500).json({ message: err.message }); } });

module.exports = router;
