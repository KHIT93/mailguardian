import { z } from 'zod'

export const userSchema = z.object({
    email: z.string().email(),
    first_name: z.string(),
    last_name: z.string(),
    role: z.enum(['user', 'domain_admin', 'superuser']),
})