const mongoose = require('mongoose');

const NotificationSchema = new mongoose.Schema({
    userId:  { type: mongoose.Schema.Types.ObjectId, ref: 'User', default: null },
    titre:   { type: String, required: true },
    message: { type: String, required: true },
    type:    { type: String, enum: ['info', 'success', 'error', 'warning'], default: 'info' },
    lu:      { type: Boolean, default: false },
}, { timestamps: true });

module.exports = mongoose.model('Notification', NotificationSchema);
