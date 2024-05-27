import { z } from "zod"
import { todo_status } from "../lib/utils"

const todoSchema = z.object({
    title: z
        .string()
        .min(1, { message: "Enter a valid title" }),
    description: z.string().min(1, { message: "Enter a valid description" }),
    status: z.enum([todo_status.TODO, todo_status.In_Progress, todo_status.Done])
})

export { todoSchema }
