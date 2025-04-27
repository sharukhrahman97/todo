const crypto = require('crypto');

function generateSalt(length=128){
    return crypto.randomBytes(length).toString('hex');
}

function hashPassword(password, salt) {
    const hash = crypto.createHmac('sha256', salt);
    hash.update(password);
    const hashedPassword = hash.digest('hex');
    return {
        salt,
        hashedPassword
    };
}

function verifyPassword(password, storedSalt, storedHashedPassword) {
    const result = hashPassword(password, storedSalt);
    return result.hashedPassword === storedHashedPassword;
}

module.exports = { generateSalt, hashPassword, verifyPassword }