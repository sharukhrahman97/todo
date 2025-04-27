const { body, query, param } = require('express-validator');

const loginValidator = () => [
    body('email').isEmail().normalizeEmail(),
    body('password').isString().isLength({ min: 4 }).trim()
]

const createAccountValidator = () => [
    body('name').isString().isLength({ min: 1 }).trim(),
    body('email').isEmail().normalizeEmail(),
    body('password').isString().isLength({ min: 4 }).trim()
]

const createTodoValidator = () => [
    body('title').isString().isLength({ min: 1 }).trim(),
    body('description').isString().isLength({ min: 1 }).trim(),
    body('status').isIn(['TODO', 'In_Progress', 'Done'])
]

const updateTodoValidator = () => [
    body('id').isUUID(),
    body('title').isString().isLength({ min: 1 }).trim(),
    body('description').isString().isLength({ min: 1 }).trim(),
    body('status').isIn([ 'TODO', 'In_Progress', 'Done'])
]

const deleteTodoValidator = () => [
    body('id').isUUID()
]

module.exports = {
    loginValidator, createAccountValidator, createTodoValidator, updateTodoValidator, deleteTodoValidator
}