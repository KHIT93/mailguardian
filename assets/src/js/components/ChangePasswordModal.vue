<template>
        <form @submit.prevent="submit" class="h-full">
            <h2 class="p-2 text-center">Change password</h2>
            <div class="px-4">
                <div class="md:flex md:items-center mb-6 mt-4" v-if="userId">
                    <div class="md:w-1/3">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="old_password">
                            Current password*
                        </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.old_password" class="form-inputborder-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="old_password" id="old_password" type="password">
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/3">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="new_password1">
                            New password*
                        </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.new_password1" class="form-inputborder-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="new_password1" id="new_password1" type="password" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/3">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="new_password2">
                            Confirm new password*
                        </label>
                    </div>
                    <div class="md:w-2/3">
                        <input v-model="form.new_password2" class="form-inputborder-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="new_password2" id="new_password2" type="password" required>
                    </div>
                </div>
            </div>
            <div class="px-6 py-4 border-t bg-gray-100 rounded-b">
                <div class="flex flex-row-reverse">
                    <button type="button" @click.prevent="$emit('close')" class="btn btn-gray-lightest shadow">Cancel</button>
                    <button type="submit" class="btn btn-blue shadow mr-2">Save</button>
                </div>
            </div>
        </form>
</template>

<script>
import Form from '../classes/Form';
export default {
    props: ['userId'],
    data: () => {
        return {
            form: new Form({
                old_password: '',
                new_password1: '',
                new_password2: ''
            })
        }
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