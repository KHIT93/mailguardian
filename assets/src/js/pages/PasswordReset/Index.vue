<template>
<mg-page>
    <div class="justify-center flex pt-8">
        <div class="w-full max-w-md">
            <form @submit.prevent="submit" class="bg-white shadow-md sm:rounded px-8 pt-6 pb-8 mb-4" method="POST">
                <h1 class="text-center mb-1">Reset Your Password</h1>
                <p class="text-center mb-4" v-if="!success">Please provide us with the email address registered for your application account</p>
                <p class="text-center mb-4" v-else>We have sent you an email with instructions on how to reset your password</p>
                <div class="md:flex md:items-center mb-6" v-if="!success">
                    <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="email">
                        Email
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <input :disabled="loading" v-model="form.email" class="form-input" name="email" id="email" type="email" placeholder="john@example.com">
                        <p class="text-sm text-red pt-1" v-if="form.errors.has('email')">{{ form.errors.get('email') }}</p>
                    </div>
                </div>
                <div class="flex flex-row-reverse items-center justify-between" v-if="!success">
                    <button class="bg-blue hover:bg-blue-dark text-white py-2 px-4 rounded flex items-center" type="submit" :disabled="loading" :class="{'select-none cursor-not-allowed bg-blue-lighter hover:bg-blue-lighter' : loading}">
                        <svg class="fill-current w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" v-if="loading">
                            <circle cx="50" cy="50" fill="none" stroke-linecap="round" r="40" stroke-width="4" stroke="#fff" stroke-dasharray="62.83185307179586 62.83185307179586" transform="rotate(66 50 50)">
                                <animateTransform attributeName="transform" type="rotate" calcMode="linear" values="0 50 50;360 50 50" keyTimes="0;1" dur="1s" begin="0s" repeatCount="indefinite"></animateTransform>
                            </circle>
                        </svg>
                        <mg-email-icon class="w-4 h-4 mr-1" v-else></mg-email-icon>
                        <span>Send confirmation email</span>
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
    data: () => {
        return {
            form: new Form({
                email: ''
            }),
            loading: false,
            success: false
        }
    },
    methods: {
        submit() {
            this.toggleLoading();
            this.form.post('/rest-auth/password/reset/').then(response => {
                this.toggleLoading();
                //Display success notification
                this.notify(this.createNotification('Password reset email has been sent', `${response.detail}`, 'success'));
                this.success = true;
            }).catch(error => {
                this.toggleLoading();
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            })
        },
        toggleLoading() {
            this.loading = !this.loading;
        },
        ...mapMutations(['notify'])
    }
}
</script>