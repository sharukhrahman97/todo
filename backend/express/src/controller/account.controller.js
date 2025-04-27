const { PrismaClient } = require('@prisma/client')
const prisma = new PrismaClient()
const { response } = require('../util/response.util')
const { responseHelper } = require('../helper/response.helper')
const { createTokens } = require('../middleware/jwt.middleware')
const { generateSalt, hashPassword, verifyPassword } = require("../util/password.util")

const loginAccount = async (req, res) => {
    try {
        const { email, password } = req.body
        const user = await prisma.user.findUnique({
            where: { email: email },
        })
        if (!user) {
            throw new Error("Invalid email or password");
        }
        const verify = verifyPassword(password, user.salt, user.hashedPassword)
        if (!verify) {
            throw new Error("Invalid email or password");
        }
        const { accessToken, refreshToken } = createTokens(user.id)
        res.header('cl-x-token', accessToken);
        res.header('cl-x-refresh', refreshToken);
        return res.status(response.readDoc.code).json(responseHelper(response.readDoc, { name: user.name, email: user.email }));
    } catch (error) {
        return res.status(response.readErrorDoc.code).json(responseHelper(response.readErrorDoc, {msg: error.message,error:error.stack}));
    }
}

const createAccount = async (req, res) => {
    try {
        const { name, email, password } = req.body
        const { salt, hashedPassword } = hashPassword(password, generateSalt())
        const result = await prisma.user.create({
            data: {
                name,
                email,
                salt,
                hashedPassword,
                todos: {
                    create: [],
                },
            },
        })
        const { accessToken, refreshToken } = createTokens(result.id)
        res.header('cl-x-token', accessToken);
        res.header('cl-x-refresh', refreshToken);
        return res.status(response.insertDoc.code).json(responseHelper(response.insertDoc, { name: result.name, email: result.email }));
    } catch (error) {
        return res.status(response.insertErrorDoc.code).json(responseHelper(response.insertErrorDoc, {msg: error.message,error:error.stack}));
    }
}

const readAccount = async (req, res) => {
    try {
        const { userId } = req.body
        const result = await prisma.user.findUnique({
            where: { id: userId },
            select: { name: true, email: true }
        })
        return res.status(response.readDoc.code).json(responseHelper(response.readDoc, result));
    } catch (error) {
        return res.status(response.readErrorDoc.code).json(responseHelper(response.readErrorDoc, {msg: error.message,error:error.stack}));
    }
}

module.exports = {
    loginAccount,
    createAccount,
    readAccount,
}