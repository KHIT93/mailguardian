<template>
    <div class="justify-center flex pt-8">
        <div class="w-full max-w-sm">
            <form @submit.prevent="submit" class="bg-white shadow-md sm:rounded px-8 pt-6 pb-8 mb-4" method="POST">
                <mg-notification v-if="form.errors.has('non_field_errors')" :notification="{ title: 'Error during login', message: form.errors.get('non_field_errors'), type: 'error' }"></mg-notification>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="email">
                        Email
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.email" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="email" id="email" type="text" placeholder="JaneDoe@example.com" required>
                        <p class="text-sm text-red pt-1" v-if="form.errors.has('email')">{{ form.errors.get('email') }}</p>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="password">
                        Password
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.password" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="password" id="password" type="password" placeholder="******************" required>
                        <p class="text-sm text-red pt-1" v-if="form.errors.has('password')">{{ form.errors.get('password') }}</p>
                    </div>
                </div>
                <div class="flex flex-row-reverse items-center justify-between">
                    <input type='hidden' name='csrfmiddlewaretoken' :value="csrftoken"/>
                    <button class="bg-blue hover:bg-blue-dark text-white py-2 px-4 rounded flex items-center" type="submit" :disabled="loading" :class="{'select-none cursor-not-allowed bg-blue-lighter hover:bg-blue-lighter' : loading}">
                        <svg class="fill-current w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" v-if="loading">
                            <circle cx="50" cy="50" fill="none" stroke-linecap="round" r="40" stroke-width="4" stroke="#fff" stroke-dasharray="62.83185307179586 62.83185307179586" transform="rotate(66 50 50)">
                                <animateTransform attributeName="transform" type="rotate" calcMode="linear" values="0 50 50;360 50 50" keyTimes="0;1" dur="1s" begin="0s" repeatCount="indefinite"></animateTransform>
                            </circle>
                        </svg>
                        <mg-lock-icon class="w-4 h-4 mr-1" v-else></mg-lock-icon>
                        <span>Sign In</span>
                    </button>
                    <router-link class="inline-block align-baseline text-sm text-blue hover:text-blue-darker" to="/password-reset">
                        Forgot Password?
                    </router-link>
                </div>
            </form>
            <p class="text-center text-grey text-xs">
                &copy;2018 MailGuardian (@KHIT93). All rights reserved.
            </p>
        </div>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex';
    import router from '../routing/router';
    import Form from '../classes/Form';
    import Notification from '../components/Notification.vue';
    export default {
        data: () => {
            return {
                form: new Form({
                    email: '',
                    password: ''
                }),
                loading: false
            }
        },
        components: {
            'mg-notification': Notification
        },
        mounted() {
            if(this.isLoggedIn) {
                router.push('/');
            }
        },
        computed: {
            ...mapGetters(['isLoggedIn', 'csrftoken'])
        },
        methods: {
            submit() {
                this.loading = true;
                this.form.post('/rest-auth/login/').then(response => {
                    window.location.href = '/';
                }).catch(error => {
                    this.loading = false;
                })
            }
        }
    }
</script>
