<script setup>
    import TopNavigation from '~/components/account/TopNavigation'
    import MainLayout from '~/components/MainLayout.vue'

    const $auth = useAuth()
    const currentUser = useAuth().$state.user
    const { $backend } = useNuxtApp()

    const loading = ref(true)

    const hasPassword = ref(false)
    const hasPasskey = ref(false)
    const hasMfa = ref(false)
    const hasEmailLink = ref(false)

    async function check2faRequirement() {
        loading.value = true
        try {
            let params = (await $backend('/auth/params', {
                method: 'POST',
                body: {
                    username: currentUser.email
                }
            }))
            hasEmailLink.value = params.email
            hasMfa.value = params.mfa
            hasPasskey.value = params.passkey
            hasPassword.value = params.password
        }
        catch ({ name, message, response }) {
            console.log(message)
        }
        finally {
            loading.value = false
        }
    }

    async function terminateAllSessions() {
        loading.value = true
        try {
            // TODO: Find a way to prevent a 401
            await $backend('/me/sessions', {
                method: 'DELETE'
            })
            $auth.logout()
        }
        catch ({ name, message, response }) {
            console.log(message)
        }
    }

    onMounted(() => check2faRequirement())

</script>

<template>
    <MainLayout page-title="My Account">
        <TopNavigation />
        <UCard>
            <div class="flex items-center p-12" v-if="loading">
                <UProgress animation="carousel" />
            </div>
            <template v-else="">
                <USeparator class="my-4" />
                <UFormField
                    v-if="hasPassword"
                    name="manage_password"
                    label="Password"
                    description="Change the password for your account"
                    class="flex flex-wrap items-center justify-between gap-4"
                    >
                    <div>
                        <UButton to="/account/security/password" icon="i-heroicons-key-solid">
                            Change password
                        </UButton>
                    </div>
                </UFormField>
                <USeparator class="my-4" />
                <UFormField
                    v-if="hasPassword"
                    name="manage_mfa"
                    label="Multi-Factor Authentication"
                    description="Improve account security by enabling Multi-Factor Authentication"
                    class="flex flex-wrap items-center justify-between gap-4"
                    >
                    <div>
                        <UButton v-if="!hasMfa" to="/account/security/mfa/enable" color="success" icon="i-heroicons-check-badge-solid">
                            Enable 2FA
                        </UButton>
                        <UButton v-if="hasMfa" to="/account/security/mfa" icon="i-heroicons-check-badge-solid">
                            Manage 2FA
                        </UButton>
                    </div>
                </UFormField>
                <USeparator class="my-4" />
                <UFormField
                    name="enable_passkeys"
                    label="Passkeys"
                    description="Using passkeys, you do not have to use your password to log in. Simply enroll passkeys from your devices and you are ready"
                    class="flex flex-wrap items-center justify-between gap-4"
                    >
                    <div>
                        <UButton to="/account/security/passkeys" icon="i-heroicons-cpu-chip-solid">
                            Manage
                        </UButton>
                    </div>
                </UFormField>
                <USeparator class="my-4" />
                <UFormField
                    name="terminate_sessions"
                    label="Active sessions"
                    description="Logging out of all devices/sessions, will require you to log in again on all devices"
                    class="flex flex-wrap items-center justify-between gap-4"
                    >
                    <div>
                        <UButton color="error" icon="i-heroicons-exclamation-circle-solid" @click="terminateAllSessions()">
                            Log out
                        </UButton>
                    </div>
                </UFormField>
                <USeparator class="my-4" />
            </template>
        </UCard>
    </MainLayout>
</template>