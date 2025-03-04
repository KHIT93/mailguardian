<script setup>
    import { useTemplateRef } from 'vue'
    import { useFocus } from '@vueuse/core'
    import LoginLayout from '~/components/LoginLayout'
    import { loginFormSchema } from '~/schemas/auth.ts'
    
    const $auth = useAuth()
    const { $backend } = useNuxtApp()

    const loading = ref(false)

    const requiresPassword = ref(false)
    const requiresPasskey = ref(false)
    const requiresMfa = ref(false)
    const requiresEmailLink = ref(false)
    const authCheckCompleted = ref(false)

    const state = reactive({
        username: undefined,
        password: undefined,
        verification_code: undefined
    })
    async function onSubmit (event) {
        if (!authCheckCompleted.value) {
            console.debug('Skipping authentication as we have not yet been given any usable credentials')
            return
        }
        loading.value = true
        let formdata = new FormData()
        formdata.append('username', state.username)
        formdata.append('password', state.password)
        formdata.append('verification_code', state.verification_code)
        try {
                const response = await $auth.loginWith('local', {
                body: formdata
            })
            navigateTo('/')
        }
        catch ({ name, message, response }) {
            // TODO: Use form validation/processing library to properly display errors on the client
            
            loading.value = false
        }
        // finally {
        //     loading.value = false
        // }
    }

    async function check2faRequirement() {
        if (state.username) {
            if (!state.username.includes('@', 0)) {
                return
            }
            try {
                let params = (await $backend('/auth/params', {
                    method: 'POST',
                    body: {
                        username: state.username
                    }
                }))
                requiresEmailLink.value = params.email
                requiresMfa.value = params.mfa
                requiresPasskey.value = params.passkey
                requiresPassword.value = params.password
                authCheckCompleted.value = true
            }
            catch ({ name, message, response }) {
                console.log(message)
            }
            
        }
    }
</script>

<template>
    <LoginLayout>
        <UForm :schema="loginFormSchema" :state="state" class="space-y-8" @submit="onSubmit">
            <UFormField label="Email" name="username">
                <UInput v-model="state.username" type="email" :autofocus="!authCheckCompleted" autocomplete="email" variant="outline" size="lg" placeholder="johh.doe@example.com" icon="i-heroicons-envelope" @keyup.enter="check2faRequirement()" @blur="check2faRequirement()" />
            </UFormField>

            <UFormField label="Password" name="password" v-if="requiresPassword">
                <UInput v-model="state.password" type="password" :autofocus="requiresPassword" autcomplete="current-password" variant="outline" size="lg" icon="i-heroicons-lock-closed" :required="requiresPassword" />
            </UFormField>

            <UFormField label="Verification Code" name="verification_code" v-if="requiresMfa">
                <UPinInput v-model="state.verification_code" otp :length="6" variant="outline" size="lg" placeholder="123456" icon="i-heroicons-check-badge" :required="requiresMfa" />
            </UFormField>

            <div class="flex flex-row-reverse" v-if="requiresPassword || requiresEmailLink">
                <UButton type="submit" :loading="loading" size="lg" icon="i-heroicons-lock-closed-solid">
                    Log in
                </UButton>
            </div>

            <USeparator label="OR" v-if="requiresPasskey" />
            <UButton icon="i-heroicons-finger-print" :disabled="loading" size="lg" block v-if="requiresPasskey">Use passkey</UButton>
        </UForm>
    </LoginLayout>
</template>
