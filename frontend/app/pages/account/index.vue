<script setup>
    import TopNavigation from '~/components/account/TopNavigation'
    import MainLayout from '~/components/MainLayout.vue'
    const endpoint = computed(() => `/me/personal`)

    const { status, data: state } = (await useApi(endpoint))

    const form = ref()

    async function onSubmit(event) {
        form.value.clear()
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
        <UForm ref="form" :state="state" @submit="onSubmit">
            <UCard>
                <UFormGroup
                    name="first_name"
                    label="First Name"
                    description="Will appear on receipts, invoices, and other communication."
                    required
                    class="grid grid-cols-2 gap-2 items-center"
                    >
                    <UInput
                        v-model="state.first_name"
                        autocomplete="off"
                        icon="i-heroicons-user"
                        size="md"
                    />
                </UFormGroup>
                <UDivider class="my-4" />
                <UFormGroup
                    name="last_name"
                    label="Last Name"
                    description="Will appear on receipts, invoices, and other communication."
                    required
                    class="grid grid-cols-2 gap-2 items-center"
                    >
                    <UInput
                        v-model="state.last_name"
                        autocomplete="off"
                        icon="i-heroicons-user"
                        size="md"
                    />
                </UFormGroup>
                <UDivider class="my-4" />
                <UFormGroup
                    name="email"
                    label="Email"
                    description="Used to sign in, for email receipts and product updates."
                    required
                    class="grid grid-cols-2 gap-2"
                    >
                    <UInput
                        v-model="state.email"
                        type="email"
                        autocomplete="off"
                        icon="i-heroicons-envelope"
                        size="md"
                    />
                </UFormGroup>
                <!-- <UDivider class="my-4" /> -->
                <!-- <UFormGroup
                    name="password"
                    label="Password"
                    description="Confirm your current password before setting a new one."
                    class="grid grid-cols-2 gap-2"
                    >
                    <UInput
                        id="password"
                        v-model="state.password_current"
                        type="password"
                        placeholder="Current password"
                        size="md"
                    />
                    <UInput
                        id="password_new"
                        v-model="state.password_new"
                        type="password"
                        placeholder="New password"
                        size="md"
                        class="mt-2"
                    />
                </UFormGroup> -->
                <template #footer>
                    <UButton type="submit">
                        Save
                    </UButton>
                </template>
            </UCard>
        </UForm>
    </MainLayout>
</template>