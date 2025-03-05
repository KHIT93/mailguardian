<script setup>
    import TopNavigation from '~/components/account/TopNavigation'
    import MainLayout from '~/components/MainLayout.vue'
    import { personalDetailsSchema } from '~/schemas/account.ts'
    const endpoint = computed(() => `/me/personal`)

    const { status, data } = (await useApi(endpoint))

    const state = reactive({
        first_name: data.value.first_name,
        last_name: data.value.last_name,
        email: data.value.email
    })

    async function onSubmit(event) {
        try {
            const response = await useApi(endpoint, {
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
    <MainLayout page-title="My Account">
        <TopNavigation />
        <UForm :schema="personalDetailsSchema" :state="state" @submit="onSubmit">
            <UCard>
                <UFormField
                    name="first_name"
                    label="First Name"
                    description="Will appear on receipts, invoices, and other communication."
                    required
                    class="grid grid-cols-2 gap-2 items-center"
                    >
                    <UInput
                        class="w-full"
                        v-model="state.first_name"
                        autocomplete="off"
                        icon="i-heroicons-user"
                        size="md"
                    />
                </UFormField>
                <USeparator class="my-4" />
                <UFormField
                    name="last_name"
                    label="Last Name"
                    description="Will appear on receipts, invoices, and other communication."
                    required
                    class="grid grid-cols-2 gap-2 items-center"
                    >
                    <UInput
                        class="w-full"
                        v-model="state.last_name"
                        autocomplete="off"
                        icon="i-heroicons-user"
                        size="md"
                    />
                </UFormField>
                <USeparator class="my-4" />
                <UFormField
                    name="email"
                    label="Email"
                    description="Used to sign in, for email receipts and product updates."
                    required
                    class="grid grid-cols-2 gap-2"
                    >
                    <UInput
                        class="w-full"
                        v-model="state.email"
                        type="email"
                        autocomplete="off"
                        icon="i-heroicons-envelope"
                        size="md"
                    />
                </UFormField>
                <template #footer>
                    <div class="flex flex-row-reverse">
                        <UButton type="submit">
                            Save
                        </UButton>
                    </div>
                </template>
            </UCard>
        </UForm>
    </MainLayout>
</template>