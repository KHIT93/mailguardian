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
                <div class="shadow overflow-hidden sm:rounded-md" :class="{ 'animate-pulse': signingIn }">
                    <div class="px-4 py-5 bg-white space-y-8 sm:p-6">
                        <template v-if="form.ephemeral_token">
                            <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                                {{ form.errors.get('non_field_errors') }}
                            </p>
                            <p class="text-red-300 text-center">
                                Please enter your verifcation code for 2-factor Authentication
                            </p>
                            <FormInput inputId="code" label="Verification code" type="text" autocomplete="off" v-model="form.mfa_code" class="my-4"/>
                            <p v-if="form.errors.has('email')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('email') }}
                            </p>
                        </template>
                        <template v-else>
                            <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                                {{ form.errors.get('non_field_errors') }}
                            </p>
                            <input type="hidden" name="remember" value="true" />
                            <FormInput inputId="email-address" label="Email address" type="email" v-model="form.email" class="my-4"/>
                            <p v-if="form.errors.has('email')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('email') }}
                            </p>
                            <FormInput inputId="password" label="Password" type="password" v-model="form.password" class="my-4"/>
                            <p v-if="form.errors.has('password')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('password') }}
                            </p>
                            <div class="flex items-center justify-between">
                                <div class="flex items-center">
                                    <input id="remember_me" v-model="form.remember" name="remember_me" type="checkbox" class="transition duration-300 h-4 w-4 text-blue-600 focus:ring-blue-500 border-2 border-gray-300 rounded" />
                                    <label for="remember_me" class="ml-2 block text-sm text-gray-900">
                                    Remember me
                                    </label>
                                </div>

                                <div class="text-sm">
                                    <NuxtLink to="#" class="font-medium transition duration-300 text-blue-600 hover:text-blue-500">
                                    Forgot your password?
                                    </NuxtLink>
                                </div>
                            </div>
                        </template>
                        <div>
                            <button type="submit" :disabled="signingIn" class="group relative w-full transition duration-300 flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:bg-blue-400 focus:shadow-none focus:ring-blue-400" :class="{ 'cursor-not-allowed bg-blue-300 hover:bg-blue-400': signingIn, 'bg-blue-500 hover:bg-blue-700 shadow-md shadow-gray-400 hover:shadow-lg hover:shadow-gray-400': !signingIn}">
                                <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" v-if="signingIn">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <LockClosedIcon v-else class="h-5 w-5 text-white transition duration-300 group-hover:text-blue-100" aria-hidden="true" />
                                </span>
                                Sign in
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { LockClosedIcon } from '@heroicons/vue/24/solid'
import { ShieldCheckIcon } from '@heroicons/vue/24/outline'
import { ref, reactive } from 'vue'
import Form from '~/classes/Form'
import FormInput from '~/components/FormInput.vue'
definePageMeta({
    middleware: ['guest']
})
const form = reactive(new Form({
    email: '',
    password: '',
    mfa_code: '',
    ephemeral_token: '',
    remember: false
}))
const { $auth } = useNuxtApp()
const signingIn = ref(false)
function signIn() {
    if (form.ephemeral_token) {
        twoFactorSignIn()
    }
    else {
        signingIn.value = true;
        $auth().login({
            data: {
                username: form.email,
                password: form.password
            },
            fetchUser: false
        }).then(response => {
            console.log(response)
            if(response.ephemeral_token) {
                signingIn.value = false
                form.ephemeral_token = response.ephemeral_token
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
            form.errors.record(error.response.data)
        })
    }
}
function twoFactorSignIn()  {
    signingIn.value = true
    $auth().login({
        data: {
            ephemeral_token: form.ephemeral_token,
            code: form.mfa_code
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
        form.errors.record(error.response.data)
    })
}
</script>