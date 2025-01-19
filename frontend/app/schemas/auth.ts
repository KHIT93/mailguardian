import { z } from 'zod'
export const loginFormSchema = z.object({
    username: z.string().email('The provided username is not a valid email address'),
    password: z.string(),
    verification_code: z.number().optional()
})