import { z } from 'zod'

export const changePasswordSchema = z.object({
    current_password: z.string(),
    password: z.string(),
    confirm_password: z.string(),
    terminate_sessions: z.boolean().default(false)
})

export const totpSetupSchema = z.object({
    secret: z.string(),
    url: z.string().url(),
    password: z.string(),
    code: z.number().min(6, 'The verification code must be at least 6 digits'),
    name: z.string()
})

export const personalDetailsSchema = z.object({
    first_name: z.string(),
    last_name: z.string(),
    email: z.string().email()
})