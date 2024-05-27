const { PrismaClient } = require('@prisma/client')
const prisma = new PrismaClient()
const { response } = require('../util/response.util')
const { responseHelper } = require('../helper/response.helper')
const _ = require('lodash');

const createTodo = async (req, res) => {
    try {
        const { userId, title, description, status } = req.body
        const result = await prisma.todo.create({
            data: {
                title, description, status,
                user: { connect: { id: userId } },
            },
            select: {
                id: true, title: true, description: true, status: true, createdAt: true, updatedAt: true
            },
        })
        return res.status(response.insertDoc.code).json(responseHelper(response.insertDoc, result));
    } catch (error) {
        return res.status(response.insertErrorDoc.code).json(responseHelper(response.insertErrorDoc, { msg: error.message, error: error.stack }));
    }
}

const updateTodo = async (req, res) => {
    try {
        const { id, title, description, status } = req.body
        const findResult = await prisma.todo.findUnique({
            where: {
                id: id,
            },
        })
        if (_.isEqual(title, findResult.title) && _.isEqual(description, findResult.description) && _.isEqual(status, findResult.status)) {
            throw new Error("Cant update the same values!");
        }
        const result = await prisma.todo.update({
            where: {
                id: id,
            },
            data: {
                title, description, status
            },
            select: {
                id: true, title: true, description: true, status: true, createdAt: true, updatedAt: true
            },
        })

        return res.status(response.updateDoc.code).json(responseHelper(response.updateDoc, result));
    } catch (error) {
        return res.status(response.updateErrorDoc.code).json(responseHelper(response.updateErrorDoc, { msg: error.message, error: error.stack }));
    }
}

const readAllTodo = async (req, res) => {
    try {
        const { userId } = req.body
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 10;
        const status = req.query.status;
        var result = null;
        if (status === 'All') {
            result = await prisma.todo.findMany({
                where: {
                    userId: userId,
                },
                select: {
                    id: true, title: true, description: true, status: true, createdAt: true, updatedAt: true
                },
                skip: (page - 1) * limit,
                take: limit
            })
        } else {
            result = await prisma.todo.findMany({
                where: {
                    userId: userId,
                    status: status
                },
                select: {
                    id: true, title: true, description: true, status: true, createdAt: true, updatedAt: true
                },
                skip: (page - 1) * limit,
                take: limit
            })
        }
        return res.status(response.readAllDoc.code).json(responseHelper(response.readAllDoc, result));
    } catch (error) {
        return res.status(response.readAllErrorDoc.code).json(responseHelper(response.readAllErrorDoc, { msg: error.message, error: error.stack }));
    }
}

const deleteTodo = async (req, res) => {
    try {
        const { id } = req.body
        const result = await prisma.todo.delete({
            where: {
                id: id,
            },
            select: {
                id: true, title: true, description: true, status: true, createdAt: true, updatedAt: true
            },
        })
        return res.status(response.deleteDoc.code).json(responseHelper(response.deleteDoc, result));
    } catch (error) {
        return res.status(response.deleteErrorDoc.code).json(responseHelper(response.deleteErrorDoc, { msg: error.message, error: error.stack }));
    }
}

module.exports = {
    createTodo,
    updateTodo,
    readAllTodo,
    deleteTodo
}