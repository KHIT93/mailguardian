<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <div v-if="user.is_staff">
                <h2 class="p-1 pb-0 font-extralight text-lg text-gray-800">Import Domains</h2>
                <hr>
                <p class="prose-sm">
                    Use the form below to import domains for which to handle email.
                </p>
                <h3 class="p-1 font-extralight text-base text-gray-800">Import format</h3>
                <hr>
                <p class="prose-sm">
                    The data import has to follow these simply structural rules:
                    <ul class="list-disc pl-8">
                        <li>CSV-format</li>
                        <li>Semi-colon as field separator / delimiter</li>
                        <li><strong>"</strong> as the wrapper for text, otherwise known as the qoute character</li>
                    </ul>
                    Fields should be ordered like this:
                    <ol class="list-decimal pl-8">
                        <li>Domain</li>
                        <li>Mailserver</li>
                        <li>Delivery type</li>
                        <li>Active</li>
                        <li>Accounts limit (Commercial applications only. Set to 0 for no limit)</li>
                    </ol>
                    Replace either "To" or "From" with <strong>*</strong> to allow or deny everything that matches the other one
                    <form @submit.prevent="submit">
                        <div class="md:flex md:items-center mb-6 mt-4">
                            <div class="md:w-1/4">
                                <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="file">
                                    File*
                                </label>
                            </div>
                            <div class="md:w-1/2">
                                <input ref="file" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="file" id="file" type="file" @change="handleFileUpload">
                            </div>
                        </div>
                        <div class="flex flex-row-reverse border-t pt-2">
                            <button type="submit" class="btn btn-blue shadow">
                                Submit
                            </button>
                        </div>
                    </form>
                </p>
            </div>
        </div>
    </div>
</mg-page>
</template>
<script>
import { mapGetters } from 'vuex';
export default {
    data: () => {
        return {
            file: false
        }
    },
    mounted() {
        this.$store.commit('setLoading', false);
    },
    computed: {
        ...mapGetters(['isLoggedIn', 'user', 'loading', 'settings'])
    },
    methods: {
        handleFileUpload(){
            this.file = this.$refs.file.files[0];
        },
        submit() {
            let formData = new FormData();
            formData.append('file', this.file);
            formData.append('import_type', 'domain');
            axios.post('/api/data-import/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                console.log(response);
            }).catch(error => {
                console.error(error);
            })
        }
    }
}
</script>