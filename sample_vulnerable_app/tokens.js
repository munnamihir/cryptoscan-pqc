const crypto = require('crypto');
const jwt = require('jsonwebtoken');

// signs JWTs with RSA
function sign(payload, key) {
  return jwt.sign(payload, key, { algorithm: 'RS256' });
}

function encryptLegacy(buf, key, iv) {
  return crypto.createCipheriv('aes-128-cbc', key, iv);
}

function digest(s) {
  return crypto.createHash('sha1').update(s).digest('hex');
}
