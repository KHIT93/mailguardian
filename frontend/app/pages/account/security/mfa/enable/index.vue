<script setup>
    import TopNavigation from '~/components/account/TopNavigation'
    import MainLayout from '~/components/MainLayout.vue'
    import QRCode from 'qrcode'
    import { totpSetupSchema } from '~/schemas/account.ts'

    const $auth = useAuth()
    const currentUser = useAuth().$state.user
    const { $backend } = useNuxtApp()

    const { data, status } = (await useApi('/totp/enable', {
        method: 'POST'
    }))

    const state = reactive({
        secret: data.value.secret,
        url: data.value.url,
        password: undefined,
        code: undefined,
        name: undefined
    })

    const userPassword = ref('')
    const verificationCode = ref('')
    const totpName = ref('')
    const loading = ref(false)

    let qr = await QRCode.toDataURL(data.value.url)

    async function onSubmit(event) {
        loading.value = true
        // form.value.clear()
        try {
            await $backend('/totp/enable/confirm', {
                method: 'POST',
                body: {
                    secret: state.value.secret,
                    url: state.value.url,
                    password: state.value.password,
                    code: state.value.code,
                    name: state.value.name,
                }
            })
            navigateTo('/account/security/mfa')
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
        <UForm :schema="totpSetupSchema" :state="state" class="space-y-8" @submit="onSubmit">
            <UCard>
                <div class="flex items-center p-12" v-if="status != 'success'">
                    <UProgress animation="carousel" />
                </div>
                <div class="flex justify-center" v-else="">
                    <div class="w-full md:w-1/2">
                        <img :src="qr" class="w-64 h-64"/>
                        <UFormField label="Name" name="name">
                            <UInput v-model="state.name" type="text" autcomplete="off" variant="outline" icon="i-heroicons-pencil" required />
                        </UFormField>

                        <UFormField label="Password" name="password">
                            <UInput v-model="state.password" type="password" autcomplete="current-password" variant="outline" icon="i-heroicons-lock-closed" required />
                        </UFormField>

                        <UFormField label="Verification Code" name="verification_code">
                            <UPinInput v-model="state.code" otp :length="6" variant="outline" size="lg" placeholder="123456" icon="i-heroicons-check-badge" required />
                        </UFormField>
                        <div class="flex flex-row-reverse mt-4">
                            <UButton type="submit" :loading="loading" icon="i-heroicons-lock-closed-solid">
                                Enable 2FA
                            </UButton>
                        </div>
                    </div>
                </div>
            </UCard>
        </UForm>
    </MainLayout>
</template>