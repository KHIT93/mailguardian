<template>
<mg-page>
    <div class="justify-center flex pt-8">
        <div class="w-full max-w-md">
            <form @submit.prevent="submit" class="bg-white shadow-md sm:rounded px-8 pt-6 pb-8 mb-4" method="POST">
                <h1 class="text-center mb-1">Reset Your Password</h1>
                <p class="text-center mb-4">Please choose your new password for the application</p>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="new_password1">
                        New Password
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.new_password1" class="form-input" name="new_password1" id="new_password1" type="password" placeholder="******************">
                        <p class="text-sm text-red-500 pt-1" v-if="form.errors.has('new_password1')">{{ form.errors.get('new_password1') }}</p>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="new_password2">
                        Confirm Password
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.new_password2" class="form-input" name="new_password2" id="new_password2" type="password" placeholder="******************">
                        <p class="text-sm text-red-500 pt-1" v-if="form.errors.has('new_password2')">{{ form.errors.get('new_password2') }}</p>
                    </div>
                </div>
                <div class="flex flex-row-reverse items-center justify-between">
                    <button class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded flex items-center" type="submit" :disabled="loading" :class="{'select-none cursor-not-allowed bg-blue-200 hover:bg-blue-200' : loading}">
                        <svg class="fill-current w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" v-if="loading">
                            <circle cx="50" cy="50" fill="none" stroke-linecap="round" r="40" stroke-width="4" stroke="#fff" stroke-dasharray="62.83185307179586 62.83185307179586" transform="rotate(66 50 50)">
                                <animateTransform attributeName="transform" type="rotate" calcMode="linear" values="0 50 50;360 50 50" keyTimes="0;1" dur="1s" begin="0s" repeatCount="indefinite"></animateTransform>
                            </circle>
                        </svg>
                        <mg-checkmark-icon class="w-4 h-4 mr-1" v-else></mg-checkmark-icon>
                        <span>Reset password</span>
                    </button>
                </div>
            </form>
        </div>
    </div>
</mg-page>
</template>

<script>
import Form from '../../classes/Form';
import router from '../../routing/router';
import { mapMutations, mapGetters } from 'vuex';
export default {
    props: ['uid', 'token'],
    data: () => {
        return {
            form: {},
            loading: false
        }
    },
    created() {
        this.form = new Form({
            uid: this.uid,
            token: this.token,
            new_password1: '',
            new_password2: ''
        })
    },
    mounted() {
        this.setInitializing(false);
        this.setLoading(false);
    },
    methods: {
        submit() {
            this.toggleLoading();
            this.form.post('/rest-auth/password/reset/confirm/').then(response => {
                this.toggleLoading();
                //Display success notification
                this.notify(this.createNotification('Password sucessfully reset', `${response.detail}`, 'success'));
                setTimeout(router.push('/login'), 5000);
            }).catch(error => {
                this.toggleLoading();
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            })
        },
        toggleLoading() {
            this.loading = !this.loading;
        },
        ...mapMutations(['notify', 'setLoading', 'setInitializing'])
    }
}
</script>