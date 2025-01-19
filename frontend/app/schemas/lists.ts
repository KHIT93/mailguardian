import { z } from 'zod'

export const listEntrySchema = z.object({
    from_address: z.string(),
    to_address: z.string(),
    listing_type: z.enum(['blocked', 'allowed']).optional()
})