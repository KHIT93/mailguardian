import { z } from 'zod'

export const domainSchema = z.object({
    name: z.string(),
    destination: z.string(),
    relay_type: z.enum(['smtp', 'smtps']),
    reception_type: z.enum(['load_balanced', 'failover']),
    active: z.boolean()
})