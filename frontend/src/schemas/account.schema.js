import { z } from "zod"

const loginAccountSchema = z.object({
    email: z
        .string()
        .min(1, { message: "Enter a valid email" })
        .email("This is not a valid email."),
    password: z.string().min(4),
})

const createAccountSchema = z.object({
    name: z.string().min(1, { message: "Enter a valid name" }),
    email: z
        .string()
        .min(1, { message: "This field has to be filled." })
        .email("This is not a valid email."),
    password: z.string().min(4),
})

export { loginAccountSchema, createAccountSchema }
