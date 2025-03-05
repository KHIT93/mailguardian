<script setup>
    import TopNavigation from '~/components/account/TopNavigation'
    import MainLayout from '~/components/MainLayout.vue'
    import { changePasswordSchema } from '~/schemas/account.ts'

    const $auth = useAuth()
    const currentUser = useAuth().$state.user
    const { $backend } = useNuxtApp()

    const loading = ref(false)

    const form = ref()

    const state = ref({
        current_password: '',
        password: '',
        confirm_password: '',
        terminate_sessions: false
    })

    async function onSubmit(event) {
        loading.value = true
        // form.value.clear()
        try {
            await $backend('/me/password/change', {
                method: 'POST',
                body: {
                    current_password: state.value.current_password,
                    password: state.value.password,
                    confirm_password: state.value.confirm_password,
                    terminate_sessions: state.value.terminate_sessions
                }
            })
        } catch(error) {
            console.log(error.statusCode)
            console.log(error.data)
            console.log(error.message)
        }
        finally {
            loading.value = false
        }
    }
</script>

<template>
    <MainLayout page-title="My Account">
        <TopNavigation />
        <UForm :schema="changePasswordSchema" ref="form" :state="state" @submit="onSubmit">
            <UCard>
                <UFormField
                    name="current_password"
                    label="Change your password"
                    description="Confirm your current password be setting a new one."
                    required
                    class="grid grid-cols-2 gap-2 items-center"
                    >
                    <UInput
                        class="w-full"
                        v-model="state.current_password"
                        id="current_password"
                        type="password"
                        autocomplete="current-password"
                        placeholder="Current password"
                        required
                        size="md"
                    />
                </UFormField>
                <USeparator class="my-2" />
                <UFormField
                    name="password"
                    label="New password"
                    description="Enter your new password, twice"
                    required
                    class="grid grid-cols-2 gap-2 items-center"
                    >
                    <UInput
                        class="w-full"
                        v-model="state.password"
                        id="password"
                        type="password"
                        autocomplete="new-password"
                        placeholder="New password"
                        required
                        size="md"
                    />
                    <UInput
                        class="w-full ml-2"
                        v-model="state.confirm_password"
                        id="confirm_password"
                        type="password"
                        autocomplete="off"
                        placeholder="Confirm new password"
                        required
                        size="md"
                    />
                </UFormField>
                <USeparator class="my-2" />
                <UFormField
                    name="terminate_sessions"
                    label="Log out of other sessions"
                    description="Check this to log out of your account on all other devices than the current one"
                    class="grid grid-cols-2 gap-2 items-center"
                    >
                    <USwitch
                        v-model="state.terminate_sessions"
                        id="terminate_sessions"
                    />
                </UFormField>
                <template #footer>
                    <div class="flex flex-row-reverse">
                        <UButton :loading="loading" type="submit">
                            Change password
                        </UButton>
                    </div>
                </template>
            </UCard>
        </UForm>
    </MainLayout>
</template>