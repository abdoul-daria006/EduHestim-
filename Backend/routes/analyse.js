// ============================================================
//  EduHestim — routes/analyse.js
//  7 KPIs : Occupation | Volume | Conflits | Créneau |
//           Modifications | Disponibilité salles | Séances/classe
// ============================================================
const router = require('express').Router();
const authMiddleware = require('../middleware/auth');

let Salle, EmploiDuTemps, Conflit, User, Demande, Modification, Classe;
try { Salle         = require('../models/Salle');          } catch(e) {}
try { EmploiDuTemps = require('../models/EmploiDuTemps');  } catch(e) {}
try { Conflit       = require('../models/Conflit');         } catch(e) {}
try { User          = require('../models/User');            } catch(e) {}
try { Demande       = require('../models/Demande');         } catch(e) {}
try { Modification  = require('../models/Modification');    } catch(e) {}
try { Classe        = require('../models/Classe');          } catch(e) {}

// ── Helpers ──────────────────────────────────────────────────
async function safeFind(Model, q = {}, p = {}) {
    if (!Model) return [];
    try { return await Model.find(q, p).lean(); } catch(e) { return []; }
}
async function safeCount(Model, q = {}) {
    if (!Model) return 0;
    try { return await Model.countDocuments(q); } catch(e) { return 0; }
}
async function safeAggregate(Model, pipeline) {
    if (!Model) return [];
    try { return await Model.aggregate(pipeline); } catch(e) { return []; }
}

// ── NETTOYAGE : réservations approuvées dédupliquées ─────────
// Clé de déduplication : salle + jourSemaine + heureDebut
// → élimine les doublons (même salle, même jour, même créneau)
async function getDemandesUniques() {
    if (!Demande) return [];
    const demandes = await Demande.find(
        { statut: { $in: ['approuve', 'approuvee'] } },
        { salle: 1, salleNom: 1, jourSemaine: 1, heureDebut: 1 }
    ).lean();
    const seen = new Set();
    return demandes.filter(d => {
        const key = `${d.salle || d.salleNom}|${d.jourSemaine}|${d.heureDebut}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
    });
}

// ============================================================
// AXE 1 — Occupation salles
// GET /api/analyse/occupation
// ============================================================
router.get('/occupation', authMiddleware, async (req, res) => {
    try {
        const TOTAL  = 640;
        const salles = await safeFind(Salle, {}, { nom:1, type:1, capacite:1, batiment:1 });
        const demandesUniques = await getDemandesUniques();

        const resByRoom = {};
        demandesUniques.forEach(d => {
            const key = d.salle ? d.salle.toString() : d.salleNom;
            resByRoom[key] = (resByRoom[key] || 0) + 1;
        });

        const data = salles.map(s => ({
            id: s._id, nom: s.nom || '—', type: s.type || 'Normale',
            capacite: s.capacite || 0, batiment: s.batiment || '—',
            nbResa: resByRoom[s._id.toString()] || 0,
            taux: parseFloat(((resByRoom[s._id.toString()] || 0) / TOTAL * 100).toFixed(1))
        }));

        const moy    = data.length ? data.reduce((s,r) => s + r.taux, 0) / data.length : 0;
        const parType = {};
        data.forEach(s => { parType[s.type] = (parType[s.type] || 0) + s.nbResa; });
        const top10 = [...data].sort((a,b) => b.taux - a.taux).slice(0, 10);

        res.json({
            kpi: {
                totalSalles: data.length,
                tauxMoyen:   parseFloat(moy.toFixed(1)),
                salleMax:    top10[0]?.nom  || '—',
                tauxMax:     top10[0]?.taux || 0,
                surcharge:   data.filter(s => s.taux > moy * 1.3).length,
                totalResaUniques: demandesUniques.length,
            },
            top10, parType, toutes: data
        });
    } catch(e) { res.status(500).json({ message: e.message }); }
});

// ============================================================
// AXE 2 — Volume horaire enseignants
// GET /api/analyse/volume-horaire
// ============================================================
router.get('/volume-horaire', authMiddleware, async (req, res) => {
    try {
        const ens = await safeFind(User, { role: 'enseignant' }, { nom:1, prenom:1, departement:1, grade:1 });
        const agg = await safeAggregate(EmploiDuTemps, [
            { $group: { _id: { $ifNull: ['$enseignantId', '$enseignant'] }, nb: { $sum: 1 } } }
        ]);
        const seances = {};
        agg.forEach(s => { if (s._id) seances[s._id.toString()] = s.nb; });

        const data = ens.map(e => {
            const nb = seances[e._id.toString()] || 0;
            return { id: e._id, nom: `${e.prenom ? e.prenom[0]+'. ' : ''}${e.nom || '—'}`,
                     dept: e.departement || 'N/A', grade: e.grade || '—',
                     nbSeances: nb, vol: nb * 2 };
        });

        const moy   = data.length ? data.reduce((s,e) => s + e.vol, 0) / data.length : 0;
        const std   = data.length ? Math.sqrt(data.reduce((s,e) => s + Math.pow(e.vol - moy, 2), 0) / data.length) : 0;
        const seuil = parseFloat((moy + std).toFixed(1));
        data.forEach(e => e.surcharge = e.vol > seuil);

        const parDeptMap = {};
        data.forEach(e => {
            if (!parDeptMap[e.dept]) parDeptMap[e.dept] = { tot: 0, n: 0 };
            parDeptMap[e.dept].tot += e.vol; parDeptMap[e.dept].n++;
        });
        const parDept = Object.entries(parDeptMap)
            .map(([d,v]) => ({ dept: d, moy: parseFloat((v.tot/v.n).toFixed(1)) }))
            .sort((a,b) => b.moy - a.moy);

        const nb = data.filter(e => e.surcharge).length;
        res.json({
            kpi: { totalEns: data.length, moyVol: parseFloat(moy.toFixed(1)), seuil,
                   nbSurcharge: nb, tauxSurcharge: data.length ? parseFloat((nb/data.length*100).toFixed(1)) : 0 },
            top15: [...data].sort((a,b) => b.vol - a.vol).slice(0, 15),
            parDept
        });
    } catch(e) { res.status(500).json({ message: e.message }); }
});

// ============================================================
// AXE 3 — Conflits
// GET /api/analyse/conflits
// ============================================================
router.get('/conflits', authMiddleware, async (req, res) => {
    try {
        const conflits = await safeFind(Conflit);
        const total    = conflits.length;
        const resolus  = conflits.filter(c => c.resolu === true || c.resolu === 'true').length;

        const parType = {}, resParType = {};
        const parJour    = { Lundi:0, Mardi:0, Mercredi:0, Jeudi:0, Vendredi:0, Samedi:0 };
        const parCreneau = { '08:00':0, '10:15':0, '14:00':0, '16:15':0 };

        conflits.forEach(c => {
            const t = c.typeConflit || c.type || 'Autre';
            parType[t] = (parType[t] || 0) + 1;
            const j = c.jourSemaine || c.jour;
            if (j && parJour[j] !== undefined) parJour[j]++;
            const h = c.heureDebut;
            if (h && parCreneau[h] !== undefined) parCreneau[h]++;
            if (!resParType[t]) resParType[t] = { r: 0, nr: 0 };
            (c.resolu === true || c.resolu === 'true') ? resParType[t].r++ : resParType[t].nr++;
        });

        res.json({
            kpi: {
                total, resolus, nonResolus: total - resolus,
                tauxResolution:    total ? parseFloat((resolus/total*100).toFixed(1)) : 0,
                tauxNonResolution: total ? parseFloat(((total-resolus)/total*100).toFixed(1)) : 0,
                typeMax: Object.entries(parType).sort((a,b) => b[1]-a[1])[0]?.[0] || '—',
                jourMax: Object.entries(parJour).sort((a,b) => b[1]-a[1])[0]?.[0] || '—',
            },
            parType, parJour, parCreneau, resParType
        });
    } catch(e) { res.status(500).json({ message: e.message }); }
});

// ============================================================
// AXE 4 — Créneau le plus demandé
// GET /api/analyse/creneaux
// ============================================================
router.get('/creneaux', authMiddleware, async (req, res) => {
    try {
        const demandes = await safeFind(Demande, {}, { jourSemaine:1, heureDebut:1, statut:1 });

        const jours    = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'];
        const creneaux = ['08:00','10:15','14:00','16:15'];
        const labCren  = { '08:00':'08h-10h','10:15':'10h15-12h15','14:00':'14h-16h','16:15':'16h15-18h15' };

        const heatmap = {};
        jours.forEach(j => { heatmap[j] = {}; creneaux.forEach(c => { heatmap[j][c] = 0; }); });
        const parCreneau = { '08:00':0,'10:15':0,'14:00':0,'16:15':0 };
        const parJour    = {};
        jours.forEach(j => { parJour[j] = 0; });

        demandes.forEach(d => {
            const j = d.jourSemaine, h = d.heureDebut;
            if (!j || !h) return;
            if (heatmap[j] && heatmap[j][h] !== undefined) heatmap[j][h]++;
            if (parCreneau[h] !== undefined) parCreneau[h]++;
            if (parJour[j] !== undefined) parJour[j]++;
        });

        const flat = [];
        jours.forEach(j => creneaux.forEach(c => {
            if (heatmap[j][c] > 0)
                flat.push({ label:`${j} ${labCren[c]}`, jour:j, creneau:c, count:heatmap[j][c] });
        }));
        flat.sort((a,b) => b.count - a.count);

        const maxCren = Object.entries(parCreneau).sort((a,b) => b[1]-a[1])[0];
        const maxJour = Object.entries(parJour).sort((a,b) => b[1]-a[1])[0];

        res.json({
            kpi: {
                creneauMax:   maxCren ? labCren[maxCren[0]] || maxCren[0] : '—',
                countMax:     maxCren?.[1] || 0,
                jourMax:      maxJour?.[0] || '—',
                countJourMax: maxJour?.[1] || 0,
                top1Label:    flat[0]?.label || '—',
                totalDemandes: demandes.length,
            },
            parCreneau, parJour, heatmap, top5: flat.slice(0,5), labCren
        });
    } catch(e) { res.status(500).json({ message: e.message }); }
});

// ============================================================
// AXE 5 — Taux de modification EDT
// GET /api/analyse/modifications
// ============================================================
router.get('/modifications', authMiddleware, async (req, res) => {
    try {
        const totalSeances  = await safeCount(EmploiDuTemps);
        const modifications = await safeFind(Modification);
        const total         = modifications.length;
        const taux          = totalSeances > 0 ? parseFloat((total / totalSeances * 100).toFixed(1)) : 0;

        const parType = {};
        modifications.forEach(m => {
            const t = m.typeModification || m.type || 'Autre';
            parType[t] = (parType[t] || 0) + 1;
        });

        const moisOrder = ['Sep','Oct','Nov','Déc','Jan','Fév','Mar','Avr','Mai','Jun'];
        const parMois   = {};
        moisOrder.forEach(m => { parMois[m] = 0; });
        modifications.forEach(m => {
            const d = m.dateModification || m.createdAt;
            if (!d) return;
            const date  = new Date(d);
            const label = date.toLocaleDateString('fr-FR', { month:'short' });
            const key   = label.charAt(0).toUpperCase() + label.slice(1, 3);
            if (parMois[key] !== undefined) parMois[key]++;
        });

        const parMotif = {};
        modifications.forEach(m => {
            const motif = m.motif || 'Non précisé';
            const key   = motif.length > 28 ? motif.substring(0,28)+'…' : motif;
            parMotif[key] = (parMotif[key] || 0) + 1;
        });
        const top5Motifs = Object.entries(parMotif)
            .sort((a,b) => b[1]-a[1]).slice(0,5)
            .map(([motif, count]) => ({ motif, count }));

        res.json({
            kpi: {
                totalSeances, totalModifs: total, taux,
                typeMax: Object.entries(parType).sort((a,b) => b[1]-a[1])[0]?.[0] || '—',
                moyParMois: moisOrder.length ? parseFloat((total / moisOrder.length).toFixed(1)) : 0,
            },
            parType, parMois, top5Motifs
        });
    } catch(e) { res.status(500).json({ message: e.message }); }
});

// ============================================================
// AXE 6 — Taux de disponibilité des salles
// GET /api/analyse/disponibilite
// ============================================================
router.get('/disponibilite', authMiddleware, async (req, res) => {
    try {
        const salles = await safeFind(Salle, {}, { nom:1, type:1, batiment:1, disponible:1, capacite:1 });

        const total       = salles.length;
        // Une salle est disponible si son champ disponible === true (ou absent = true par défaut)
        const disponibles = salles.filter(s => s.disponible !== false).length;
        const indispos    = total - disponibles;
        const taux        = total > 0 ? parseFloat((disponibles / total * 100).toFixed(1)) : 0;

        // Par bâtiment
        const parBatiment = {};
        salles.forEach(s => {
            const b = s.batiment || 'Inconnu';
            if (!parBatiment[b]) parBatiment[b] = { dispo: 0, total: 0 };
            parBatiment[b].total++;
            if (s.disponible !== false) parBatiment[b].dispo++;
        });
        const batimentData = Object.entries(parBatiment).map(([bat, v]) => ({
            batiment: bat,
            dispo:    v.dispo,
            indispo:  v.total - v.dispo,
            total:    v.total,
            taux:     parseFloat((v.dispo / v.total * 100).toFixed(1))
        })).sort((a,b) => b.taux - a.taux);

        // Par type
        const parType = {};
        salles.forEach(s => {
            const t = s.type || 'Normale';
            if (!parType[t]) parType[t] = { dispo: 0, total: 0 };
            parType[t].total++;
            if (s.disponible !== false) parType[t].dispo++;
        });

        res.json({
            kpi: {
                total,
                disponibles,
                indisponibles: indispos,
                tauxDisponibilite: taux,
                tauxIndisponibilite: parseFloat((100 - taux).toFixed(1)),
                batimentMin: batimentData[batimentData.length-1]?.batiment || '—',
            },
            batimentData, parType
        });
    } catch(e) { res.status(500).json({ message: e.message }); }
});

// ============================================================
// AXE 7 — Nombre moyen de séances par classe
// GET /api/analyse/seances-par-classe
// ============================================================
router.get('/seances-par-classe', authMiddleware, async (req, res) => {
    try {
        const classes = await safeFind(Classe, {}, { nom:1, code:1, filiere:1, niveau:1 });

        // Séances groupées par classeCode
        const agg = await safeAggregate(EmploiDuTemps, [
            { $group: { _id: '$classeCode', nbSeances: { $sum: 1 } } }
        ]);
        const seancesMap = {};
        agg.forEach(a => { if (a._id) seancesMap[a._id] = a.nbSeances; });

        // Total séances dans l'EDT
        const totalSeances = await safeCount(EmploiDuTemps);
        const totalClasses = classes.length;
        const moyGlobale   = totalClasses > 0 ? parseFloat((totalSeances / totalClasses).toFixed(1)) : 0;

        // Par classe
        const data = classes.map(c => ({
            id:       c._id,
            nom:      c.nom  || c.code || '—',
            code:     c.code || '—',
            filiere:  c.filiere || 'N/A',
            niveau:   c.niveau  || '—',
            nbSeances: seancesMap[c.code] || seancesMap[c._id?.toString()] || 0,
        })).sort((a,b) => b.nbSeances - a.nbSeances);

        // Par filière
        const parFiliereMap = {};
        data.forEach(c => {
            if (!parFiliereMap[c.filiere]) parFiliereMap[c.filiere] = { tot: 0, n: 0 };
            parFiliereMap[c.filiere].tot += c.nbSeances;
            parFiliereMap[c.filiere].n++;
        });
        const parFiliere = Object.entries(parFiliereMap)
            .map(([f,v]) => ({ filiere: f, moy: parseFloat((v.tot / v.n).toFixed(1)), total: v.tot }))
            .sort((a,b) => b.moy - a.moy);

        // Classe la plus chargée
        const classMax = data[0];

        res.json({
            kpi: {
                totalClasses,
                totalSeances,
                moyGlobale,
                classMax:    classMax?.nom      || '—',
                maxSeances:  classMax?.nbSeances || 0,
                classMin:    data[data.length-1]?.nom      || '—',
                minSeances:  data[data.length-1]?.nbSeances || 0,
            },
            parClasse:  data,
            parFiliere,
        });
    } catch(e) { res.status(500).json({ message: e.message }); }
});

module.exports = router;