const responseHelper = (status, result) => {
    const response = {
        code: status.code,
        message: status.message,
        result,
    };
    return response;
};

module.exports = { responseHelper }