<script setup>
    import MainLayout from '~/components/MainLayout.vue'
    import { listEntrySchema } from '~/schemas/lists.ts'

    const listingTypes = [
        {
            value: 'allowed',
            label: 'Allow'
        },
        {
            value: 'blocked',
            label: 'Block'
        }
    ]

    const state = reactive({
        from_address: null,
        to_address: null,
        from_domain: null,
        to_domain: null,
        listing_type: null
    })

    const submissionEndpoint = computed(() => {
        console.log(state?.listing_type)
        if (state?.listing_type == 'allowed') {
            return `/allowlist`
        }
        else if (state?.listing_type == 'blocked') {
            return `/blocklist`
        }
        else {
            return 'shit'
        }
    })

    const form = ref()

    async function onSubmit(event) {
        form.value.clear()
        try {
            const response = await useApi(submissionEndpoint, {
                method: 'POST',
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
    <MainLayout page-title="Create sender">
        <UForm ref="form" :schema="listEntrySchema" :state="state" @submit="onSubmit">
            <UCard>
                    <UFormGroup label="Senders address" name="from_address" size="md" class="my-4">
                        <UInput id="from_address" type="text" v-model="state.from_address"/>
                    </UFormGroup>
                    <UFormGroup label="Recipient address" name="to_address" size="md" class="my-4">
                        <UInput id="to_address" type="text" v-model="state.to_address"/>
                    </UFormGroup>
                    <UFormGroup label="Action" name="listing_type" size="md" class="my-4">
                        <UInputMenu v-model="state.listing_type" :options="listingTypes" value-attribute="value" option-attribute="label" placeholder="Select action to take..."/>
                    </UFormGroup>

                <template #footer>
                    <UButton type="submit">
                        Save
                    </UButton>
                </template>
            </UCard>
        </UForm>
    </MainLayout>
</template>