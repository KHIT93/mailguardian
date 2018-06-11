<template>
    <mg-modal @close="cancel" @submit="submit" :show="show" modal-title="Change password">
        <form @submit.prevent="submit">
            <div class="md:flex md:items-center mb-6 mt-4" v-if="userId">
                <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                        Current password*
                    </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.old_password" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="old_password" id="old_password" type="password">
                </div>
            </div>
            <div class="md:flex md:items-center mb-6 mt-4">
                <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                        New password*
                    </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.new_password1" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="new_password1" id="new_password1" type="password" required>
                </div>
            </div>
            <div class="md:flex md:items-center mb-6 mt-4">
                <div class="md:w-1/3">
                    <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                        Confirm new password*
                    </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.new_password2" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="new_password2" id="new_password2" type="password" required>
                </div>
            </div>
        </form>
    </mg-modal>
</template>

<script>
import Modal from './Modal.vue';
import Form from '../classes/Form';
export default {
    props: ['show', 'userId'],
    data: () => {
        return {
            form: new Form({
                old_password: '',
                new_password1: '',
                new_password2: ''
            })
        }
    },
    components: {
        'mg-modal': Modal
    },
    methods: {
        submit() {
            let endpoint = (this.userId) ? '/api/users/'+this.userId+'/change-password/': '/rest-auth/password/change/';
            this.form.post(endpoint).then(response => {
                this.$emit('submit');            
            })
        },
        cancel() {
            this.$emit('close');
        }
    }
}
</script>