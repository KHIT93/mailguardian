<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                    Sign in to your account
                </h2>
            </div>
            <form class="mt-8 space-y-6" action="#" method="POST" @submit.prevent="signIn">
                <div class="shadow overflow-hidden sm:rounded-md" :class="{ 'animate-pulse': signingIn }">
                    <div class="px-4 py-5 bg-white space-y-6 sm:p-6">
                        <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                            {{ form.errors.get('non_field_errors') }}
                        </p>
                        <input type="hidden" name="remember" value="true" />
                        <div>
                            <label for="email-address" class="text-sm">Email address</label>
                            <input id="email-address" v-model="form.email.value" name="email" type="email" autocomplete="email" required="" :class="{ 'border-red-600': form.errors.has('email') }" class="transition duration-300 appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="john@doe.com" />
                            <p v-if="form.errors.has('email')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('email') }}
                            </p>
                        </div>
                        <div>
                            <label for="password" class="text-sm">Password</label>
                            <input id="password" v-model="form.password.value" name="password" type="password" required="" autocomplete="current-password" :class="{ 'border-red-600': form.errors.has('password') }" class="transition duration-300 appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="************" />
                            <p v-if="form.errors.has('password')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('password') }}
                            </p>
                        </div>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center">
                                <input id="remember_me" v-model="form.remember" name="remember_me" type="checkbox" class="transition duration-300 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                                <label for="remember_me" class="ml-2 block text-sm text-gray-900">
                                Remember me
                                </label>
                            </div>

                            <div class="text-sm">
                                <router-link to="#" class="font-medium transition duration-300 text-blue-600 hover:text-blue-500">
                                Forgot your password?
                                </router-link>
                            </div>
                        </div>
                        <div>
                            <button type="submit" :disabled="signingIn" class="group relative w-full transition duration-300 flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500" :class="{ 'cursor-not-allowed bg-blue-300 hover:bg-blue-400': signingIn, 'bg-blue-600 hover:bg-blue-700': !signingIn}">
                                <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" v-if="signingIn">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <LockClosedIcon v-else class="h-5 w-5 text-blue-500 transition duration-300 group-hover:text-blue-400" aria-hidden="true" />
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

<script>
import { LockClosedIcon } from '@heroicons/vue/solid'
import { ref } from 'vue'
import Form from '../classes/Form'
export default {
    components: {
        LockClosedIcon
    },
    setup(props) {
        let form = new Form({
            email: ref(''),
            password: ref(''),
            remember: ref(false)
        })
        let signingIn = ref(false)
        return {
            form,
            signingIn
        }
    },
    methods: {
        signIn() {
            this.signingIn = true;
            this.$auth.login({
                data: {
                    email: this.form.email.value,
                    password: this.form.password.value
                }
            }).then(() => {
                console.warn('Logged in!')
            })
            .catch(error => {
                this.signingIn = false
                this.form.errors.record(error.response.data)
            })
        }
    }
}
</script>