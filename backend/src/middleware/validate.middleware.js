const { validationResult } = require('express-validator');
const { response } = require('../util/response.util')
const { responseHelper } = require('../helper/response.helper');

// Validate function to handle the validation result
const validate = (req, res, next) => {
    const errors = validationResult(req);
    if (errors.isEmpty()) {
        return next();
    }
    return res.status(response.validationError.code).json(responseHelper(response.validationError, errors.array()));
};

module.exports = {
    validate,
};