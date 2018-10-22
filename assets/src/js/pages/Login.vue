<template>
    <div class="justify-center flex pt-8">
        <div class="w-full max-w-sm">
            <div>
                <mg-notification v-for="message in login_notifications" :key="message.id" :notification="{ title: message.title, message: message.body, type: 'info' }"/>
            </div>
            <form @submit.prevent="submit" class="bg-white shadow-md sm:rounded px-8 pt-6 pb-8 mb-4" method="POST">
                <mg-notification v-if="form.errors.has('non_field_errors')" :notification="{ title: 'Error during login', message: form.errors.get('non_field_errors'), type: 'error' }"></mg-notification>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="email">
                        Email
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.email" class="form-input" name="email" id="email" type="text" placeholder="JaneDoe@example.com" required>
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
                        <input v-model="form.password" class="form-input" name="password" id="password" type="password" placeholder="******************" required>
                        <p class="text-sm text-red pt-1" v-if="form.errors.has('password')">{{ form.errors.get('password') }}</p>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-2" v-if="form.errors.has('two_factor_token') && !use_backup_code">
                    <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="two_factor_token">
                        Two Factor Verification
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.two_factor_token" class="form-input" name="two_factor_token" id="two_factor_token" type="text" required>
                        <p class="text-sm text-red pt-1" v-if="form.errors.has('two_factor_token')">{{ form.errors.get('two_factor_token') }}</p>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="form.errors.has('two_factor_token') && !use_backup_code">
                    <div class="md:w-1/3"></div>
                    <div class="md:w-2/3">
                        <button type="button" class="inline-block align-baseline text-sm text-blue hover:text-blue-darker" @click.prevent="use_backup_code = true" v-if="form.errors.has('two_factor_token')">Use 2FA Backup code</button>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-2" v-if="form.errors.has('two_factor_token') && use_backup_code">
                    <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="backup_code">
                        2FA Backup Code
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.backup_code" class="form-input" name="backup_code" id="backup_code" type="text" required>
                        <p class="text-sm text-red pt-1" v-if="form.errors.has('backup_code')">{{ form.errors.get('backup_code') }}</p>
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
    import { mapGetters, mapMutations } from 'vuex';
    import router from '../routing/router';
    import Form from '../classes/Form';
    import Notification from '../components/Notification.vue';
    export default {
        data: () => {
            return {
                form: new Form({
                    email: '',
                    password: '',
                    two_factor_token: null,
                    backup_code: ''
                }),
                loading: false,
                login_notifications: [],
                use_backup_code: false
            }
        },
        components: {
            'mg-notification': Notification
        },
        created() {
            if(this.isLoggedIn) {
                router.push('/');
            }
            this.setLoading(false);
            axios.get('/api/notifications/login/').then(response => {
                this.login_notifications = response.data;
            }).catch(error => {
            });
            this.setInitializing(false);
        },
        mounted() {
            if(this.isLoggedIn) {
                router.push('/');
            }
            this.setLoading(false);
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
            },
            ...mapMutations(['setLoading', 'setInitializing'])
        }
    }
</script>
