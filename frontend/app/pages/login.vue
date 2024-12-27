<template>
    <LoginLayout>
        <UForm :state="state" class="space-y-8" @submit="onSubmit">
            <UFormGroup label="Email" name="username">
                <UInput v-model="state.username" type="email" variant="outline" size="lg" placeholder="johh.doe@example.com" icon="i-heroicons-envelope" />
            </UFormGroup>

            <UFormGroup label="Password" name="password">
                <UInput v-model="state.password" type="password" variant="outline" size="lg" icon="i-heroicons-lock-closed" />
            </UFormGroup>

            <div class="flex flex-row-reverse">
                <UButton type="submit" :loading="loading" size="lg" icon="i-heroicons-lock-closed-solid">
                    Log in
                </UButton>
            </div>

            <UDivider label="OR" />
            <UButton icon="i-heroicons-finger-print" :disabled="loading" size="lg" block>Use passkey</UButton>
        </UForm>
    </LoginLayout>
</template>

<script setup>
    const $auth = useAuth()

    const loading = ref(false)

    const state = reactive({
        username: undefined,
        password: undefined
    })
    async function onSubmit (event) {
        loading.value = true
        let formdata = new FormData()
        formdata.append('username', state.username)
        formdata.append('password', state.password)
        try {
                const response = await $auth.loginWith('local', {
                body: formdata
            })
            navigateTo('/')
        }
        catch (err) {
            // TODO: Use form validation/processing library to properly display errors on the client
            console.log(err)
        }
        finally {
            loading.value = false
        }
    }
</script>