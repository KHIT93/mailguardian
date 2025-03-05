<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    import { listEntrySchema } from '~/schemas/lists.ts'
    const { uuid } = useRoute().params
    const pageTitle = computed(() =>  `Sender Details (${uuid})`)
    const { status, data: state } = (await useApi(`/allowlist/${uuid}`))

    const submissionEndpoint = computed(() => {
        if (state.value.listing_type == 'allowed') {
            return `/allowlist/${uuid}`
        }
        else if (state.value.listing_type == 'blocked') {
            return `/blocklist/${uuid}`
        }
        else {
            return undefined
        }
    })

    const form = ref()

    async function onSubmit(event) {
        form.value.clear()
        try {
            const response = await useApi(submissionEndpoint, {
                method: 'PATCH',
                body: state
            })
        } catch(error) {
            if (error.statusCode == 422) {
                console.log(error.data)
                form.value.setErrors(error.data.detail.map((err) => ({
                    message: err.msg,
                    path: err.loc
                })))
            }
        }
        
    }
</script>

<template>
    <MainLayout :page-title="pageTitle">
        <UForm ref="form" :schema="listEntrySchema" :state="state" @submit="onSubmit">
            <UCard>
                <UFormField label="Senders address" name="from_address" size="md" class="my-4">
                    <UInput class="w-full" id="from_address" type="text" v-model="state.from_address"/>
                </UFormField>
                <UFormField label="Recipient address" name="to_address" size="md" class="my-4">
                    <UInput class="w-full" id="to_address" type="text" v-model="state.to_address"/>
                </UFormField>

                <template #footer>
                    <UButton type="submit">
                        Save
                    </UButton>
                </template>
            </UCard>
        </UForm>
    </MainLayout>
</template>