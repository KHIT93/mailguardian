<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-700">
                    <ShieldCheckIcon class="h-10 w-10 text-blue-500 inline-block" aria-hidden="true"/>
                    <span class="">MailGuardian</span>
                </h2>
            </div>
            <form class="mt-8 space-y-6" action="#" method="POST" @submit.prevent="signIn">

                <!-- <div class="shadow overflow-hidden sm:rounded-md" :class="{ 'animate-pulse': signingIn }">
                    <div class="px-4 py-5 bg-white space-y-8 sm:p-6"> -->
                <UCard :class="{ 'animate-pulse': signingIn }">
                    <div class="px-4 py-5 bg-white space-y-4 sm:p-6" v-if="login.ephemeral_token">
                        <p v-if="login.errors.has('non_field_errors')" class="text-red-500">
                            {{ login.errors.get('non_field_errors') }}
                        </p>
                        <p class="text-red-300 text-center">
                            Please enter your verifcation code for 2-factor Authentication
                        </p>
                        <UFormGroup label="Verification code" size="md" class="my-4">
                            <UInput id="mfa_code" type="text" v-model="login.mfa_code" autocomplete="one-time-code"/>
                            <p v-if="login.errors.has('mfa_code')" class="text-red-500 text-xs py-1">
                                {{ login.errors.get('mfa_code') }}
                            </p>
                        </UFormGroup>
                    </div>
                    <div class="px-4 py-5 bg-white space-y-4 sm:p-6" v-else>
                        <p v-if="login.errors.has('non_field_errors')" class="text-red-500">
                            {{ login.errors.get('non_field_errors') }}
                        </p>
                        <UFormGroup label="Email" size="md">
                            <UInput id="email-address" type="email" v-model="login.email" autocomplete="email"/>
                            <p v-if="login.errors.has('email')" class="text-red-500 text-xs py-1">
                                {{ login.errors.get('email') }}
                            </p>
                        </UFormGroup>
                        <UFormGroup label="Password" size="md">
                            <UInput id="password" type="password" v-model="login.password"/>
                            <p v-if="login.errors.has('password')" class="text-red-500 text-xs py-1">
                                {{ login.errors.get('password') }}
                            </p>
                        </UFormGroup>
                        <p v-if="login.errors.has('password')" class="text-red-500 text-xs py-1">
                            {{ login.errors.get('password') }}
                        </p>
                        
                    </div>
                    <template #footer>
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center">
                                <UCheckbox label="Remember me" id="remember" v-model="login.remember" name="remember"/>
                            </div>

                            <div class="text-sm">
                                <NuxtLink to="#" class="font-medium transition duration-300 text-blue-600 hover:text-blue-500">
                                Forgot your password?
                                </NuxtLink>
                            </div>
                        </div>
                        <UButton class="transition duration-300 shadow-md shadow-gray-400 hover:shadow-lg hover:shadow-gray-400" block leading :loading="signingIn" :disabled="signingIn" icon="i-heroicons-lock-closed-solid" type="submit" size="md">Sign in</UButton>
                    </template>
                </UCard>
                    <!-- </div>
                </div> -->
            </form>
        </div>
    </div>
</template>

<script setup>
import { ShieldCheckIcon } from '@heroicons/vue/24/outline'
import { ref, reactive } from 'vue'
import Form from '~/classes/Form'
definePageMeta({
    middleware: ['guest'],
})
useHead({
    title: 'MailGuardian - Sign In'
})
const login = reactive(new Form({
    email: '',
    password: '',
    mfa_code: '',
    ephemeral_token: '',
    remember: false
}))
const { $auth } = useNuxtApp()
const signingIn = ref(false)
function signIn() {
    if (login.ephemeral_token) {
        twoFactorSignIn()
    }
    else {
        signingIn.value = true;
        $auth().login({
            data: {
                username: login.email,
                password: login.password
            },
            fetchUser: false
        }).then(response => {
            console.log(response)
            if(response.ephemeral_token) {
                signingIn.value = false
                login.ephemeral_token = response.ephemeral_token
                console.error('Login requires 2FA')
                return
            }
            else {
                console.warn('Logged in!')
                $auth().fetch().then(() => {
                    navigateTo('/')
                })
            }
        })
        .catch(error => {
            signingIn.value = false
            console.log(error)
            login.errors.record(error.response.data)
        })
    }
}
function twoFactorSignIn()  {
    signingIn.value = true
    $auth().login({
        data: {
            ephemeral_token: login.ephemeral_token,
            code: login.mfa_code
        },
        fetchUser: false,
        url: '/rest-auth/login/code/'
    }).then(response => {
        console.warn('Logged in with 2FA!')
        $auth().fetch().then(response => {
            navigateTo('/')
        })
    })
    .catch(error => {
        signingIn.value = false
        console.log(error)
        login.errors.record(error.response.data)
    })
}
</script>