const express = require("express");
const { verifyTokens } = require("../middleware/jwt.middleware");
const { loginAccount, createAccount, readAccount } = require('../controller/account.controller');
const { validate } = require('../middleware/validate.middleware');
const { loginValidator, createAccountValidator } = require('../helper/validate.helper');

const router = express.Router();

router.post("/loginAccount", loginValidator(), validate, loginAccount);
router.post("/createAccount", createAccountValidator(), validate, createAccount);
router.get("/readAccount", verifyTokens, readAccount);

module.exports = router;
