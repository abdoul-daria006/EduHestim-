// ============================================================
//  EduHestim — api.js  v2
//  Couche d'accès au backend Node.js/Express sur localhost:5000
// ============================================================

const API_BASE = 'http://localhost:5000/api';

// ─────────────────────────────────────────────
//  Helpers HTTP
// ─────────────────────────────────────────────

function getToken() {
    return localStorage.getItem('eduhestim_token');
}

async function request(method, endpoint, body = null) {
    const headers = { 'Content-Type': 'application/json' };
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);

    const res = await fetch(`${API_BASE}${endpoint}`, options);
    const data = await res.json();

    if (!res.ok) throw new Error(data.message || `Erreur ${res.status}`);
    return data;
}

const get  = (endpoint)       => request('GET',    endpoint);
const post = (endpoint, body) => request('POST',   endpoint, body);
const put  = (endpoint, body) => request('PUT',    endpoint, body);
const del  = (endpoint)       => request('DELETE', endpoint);


// ─────────────────────────────────────────────
//  authSystem
// ─────────────────────────────────────────────

const authSystem = {

    async login(email, password) {
        const data = await post('/auth/login', { email, password });
        localStorage.setItem('eduhestim_token', data.token);
        localStorage.setItem('eduhestim_user',  JSON.stringify(data.user));
        return data.user;
    },

    // ✅ FIX déconnexion : vide le localStorage puis redirige
    logout() {
        localStorage.removeItem('eduhestim_token');
        localStorage.removeItem('eduhestim_user');

        // Trouve le chemin de base (fonctionne en file:// ET en Live Server)
        const path = window.location.pathname;
        const base = path.substring(0, path.lastIndexOf('/') + 1);
        window.location.href = base + 'Connexion_VRAIMENT_FIXED.html';
    },

    getCurrentUser() {
        try {
            const raw = localStorage.getItem('eduhestim_user');
            return raw ? JSON.parse(raw) : null;
        } catch {
            return null;
        }
    },

    // ✅ requireAuth : redirige si pas connecté ou mauvais rôle
    requireAuth(role = null) {
        const user  = this.getCurrentUser();
        const token = getToken();

        if (!user || !token) {
            const path = window.location.pathname;
            const base = path.substring(0, path.lastIndexOf('/') + 1);
            window.location.href = base + 'Connexion_VRAIMENT_FIXED.html';
            return null;
        }

        if (role && user.role !== role) {
            alert(`Accès refusé. Cette page est réservée aux ${role}s.`);
            const path = window.location.pathname;
            const base = path.substring(0, path.lastIndexOf('/') + 1);
            window.location.href = base + 'Connexion_VRAIMENT_FIXED.html';
            return null;
        }

        return user;
    },

    isLoggedIn() {
        return !!(this.getCurrentUser() && getToken());
    }
};


// ─────────────────────────────────────────────
//  dataManager
// ─────────────────────────────────────────────

const dataManager = {

    // ── USERS ──────────────────────────────────

    getUsers() {
        return get('/users');
    },

    getUserStats() {
        return get('/users/stats');
    },

    getUserById(id) {
        return get(`/users/${id}`);
    },

    addUser(data) {
        return post('/auth/register', data);
    },

    updateUser(id, data) {
        return put(`/users/${id}`, data);
    },

    deleteUser(id) {
        return del(`/users/${id}`);
    },

    async getUsersByRole(role) {
        const users = await get('/users');
        return users.filter(u => u.role === role);
    },


    // ── SALLES ─────────────────────────────────

    getSalles() {
        return get('/salles');
    },

    getSalleById(id) {
        return get(`/salles/${id}`);
    },

    addSalle(data) {
        return post('/salles', data);
    },

    updateSalle(id, data) {
        return put(`/salles/${id}`, data);
    },

    deleteSalle(id) {
        return del(`/salles/${id}`);
    },

    // Retourne uniquement les salles disponibles
    async getSallesDisponibles() {
        const salles = await get('/salles');
        return salles.filter(s => s.disponible !== false);
    },


    // ── CLASSES ────────────────────────────────

    getClasses() {
        return get('/classes');
    },

    getClasseById(id) {
        return get(`/classes/${id}`);
    },

    addClass(data) {
        return post('/classes', data);
    },

    updateClasse(id, data) {
        return put(`/classes/${id}`, data);
    },

    deleteClasse(id) {
        return del(`/classes/${id}`);
    },


    // ── EMPLOIS DU TEMPS ───────────────────────

    getEmploisDuTemps() {
        return get('/emplois');
    },

    getEmploisByClasse(classeCode) {
        return get(`/emplois/classe/${classeCode}`);
    },

    addEmploiDuTemps(data) {
        return post('/emplois', data);
    },

    updateEmploiDuTemps(id, data) {
        return put(`/emplois/${id}`, data);
    },

    deleteEmploiDuTemps(id) {
        return del(`/emplois/${id}`);
    },


    // ── DEMANDES ───────────────────────────────

    getDemandes(statut = null) {
        const qs = statut ? `?statut=${statut}` : '';
        return get(`/demandes${qs}`);
    },

    getDemandesByUser(userId) {
        return get(`/demandes/user/${userId}`);
    },

    addDemande(data) {
        return post('/demandes', data);
    },

    approuverDemande(id, data) {
        return put(`/demandes/${id}/approuver`, data);
    },

    refuserDemande(id, data) {
        return put(`/demandes/${id}/refuser`, data);
    },

    deleteDemande(id) {
        return del(`/demandes/${id}`);
    },


    // ── NOTIFICATIONS ──────────────────────────

    getNotificationsByUser(userId) {
        return get(`/notifications/user/${userId}`);
    },

    markNotificationAsRead(id) {
        return put(`/notifications/${id}/read`, {});
    },


    // ── HELPERS ────────────────────────────────

    formatDate(isoString) {
        if (!isoString) return '—';
        return new Date(isoString).toLocaleDateString('fr-FR');
    },

    formatDateTime(isoString) {
        if (!isoString) return '—';
        const d = new Date(isoString);
        return d.toLocaleDateString('fr-FR') + ' à ' +
               d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    },

    statutLabel(statut) {
        const map = { en_attente: 'En attente', approuve: 'Approuvée', refuse: 'Refusée' };
        return map[statut] || statut;
    }
};