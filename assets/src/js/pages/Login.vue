<template>
    <div class="justify-center flex pt-8">
        <div class="w-full max-w-sm">
            <form @submit="submit" class="bg-white shadow-md sm:rounded px-8 pt-6 pb-8 mb-4" action="/api-auth/login/?next=/" method="POST">
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                        Email
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.email" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="username" id="username" type="text" placeholder="JaneDoe@example.com">
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="password">
                        Password
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.password" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="password" id="password" type="password" placeholder="******************">
                    </div>
                </div>
                <div class="flex flex-row-reverse items-center justify-between">
                    <input type='hidden' name='csrfmiddlewaretoken' :value="csrftoken"/>
                    <button class="bg-blue hover:bg-blue-dark text-white py-2 px-4 rounded" type="submit" :disabled="loading" :class="{'select-none cursor-not-allowed bg-blue-lightest hover:bg-blue-lightest' : loading}">
                        <svg class="fill-current w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" v-if="loading">
                            <circle cx="50" cy="50" fill="none" stroke-linecap="round" r="40" stroke-width="4" stroke="#fff" stroke-dasharray="62.83185307179586 62.83185307179586" transform="rotate(66 50 50)">
                                <animateTransform attributeName="transform" type="rotate" calcMode="linear" values="0 50 50;360 50 50" keyTimes="0;1" dur="1s" begin="0s" repeatCount="indefinite"></animateTransform>
                            </circle>
                        </svg>
                        <svg class="fill-current w-4 h-4" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" v-else>
                            <path d="M0 0h24v24H0z" fill="none"/>
                            <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                        </svg>
                        Sign In
                    </button>
                    <a class="inline-block align-baseline text-sm text-blue hover:text-blue-darker" href="#">
                        Forgot Password?
                    </a>
                </div>
            </form>
            <p class="text-center text-grey text-xs">
                &copy;2018 MailWare (@KHIT93). All rights reserved.
            </p>
        </div>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex';
    import router from '../routing/router';
    import Form from '../classes/Form';
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
                    console.log(error.response);
                })
            }
        }
    }
</script>
