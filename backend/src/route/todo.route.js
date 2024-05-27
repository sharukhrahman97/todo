const express = require("express");
const { verifyTokens } = require("../middleware/jwt.middleware");
const { validate } = require('../middleware/validate.middleware');
const { createTodoValidator, updateTodoValidator, deleteTodoValidator } = require('../helper/validate.helper');
const { createTodo, readAllTodo, updateTodo, deleteTodo } = require('../controller/todo.controller');

const router = express.Router();

router.post("/createTodo", verifyTokens, createTodoValidator(), validate, createTodo);
router.put("/updateTodo", verifyTokens, updateTodoValidator(), validate, updateTodo);
router.get("/readAllTodo", verifyTokens, readAllTodo);
router.delete("/deleteTodo", verifyTokens, deleteTodoValidator(), validate, deleteTodo);

module.exports = router;
