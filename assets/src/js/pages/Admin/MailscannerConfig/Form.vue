<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-6 pb-8">
        <div class="card p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="key">
                            Key*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.key" class="form-input" name="key" id="key" type="text" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="value">
                            Value
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.value" class="form-input" name="value" id="value" type="text">
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            File
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <div v-if="form.id" class="text-gray-400">{{ form.filepath }}</div>
                        <div class="relative" v-else>
                            <select v-model="form.filepath" class="form-select">
                                <option value="">-- Select file --</option>
                                <option v-for="f in filepaths" :key="f.filepath" :value="f.filepath">{{ f.filepath }}</option>
                            </select>
                            <div class="form-select-icon">
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex flex-row-reverse border-t pt-2">
                    <button type="submit" class="btn btn-blue shadow">
                        Submit
                    </button>
                    <button v-if="id" @click="destroy" type="button" class="mr-1 flex-shrink-0 bg-red-500 hover:bg-red-600 border-red-500 hover:border-red-600 text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Delete
                    </button>
                </div>
            </form>
        </div>
    </div>
</mg-page>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import router from '../../../routing/router';
import Form from '../../../classes/Form';
export default {
    props: ['id'],
    data: () => {
        return {
            entity: {},
            form: {},
            filepaths: []
        }
    },
    created() {
        if (this.id) {
            this.get();
        }
        else {
            this.setLoading(false);
            this.form = new Form({
                key: '',
                value: '',
                filepath: '',
            });
        }
        this.get_filepaths();
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        get() {
            this.setLoading(true);
            axios.get('/api/mailscanner-configuration/'+this.id+'/').then(response => {
                this.entity = response.data;
                this.form = new Form({
                    id: response.data.id,
                    key: response.data.key,
                    value: response.data.value,
                    filepath: response.data.filepath,
                });
                this.setLoading(false);
            }).catch(error => {
                this.setLoading(false);
                if (error.response.status == 404) {
                    router.push({ name: 'not_found' });
                }
                else if (error.response.status == 403) {
                    router.push({ name: 'access_denied' });
                }
            })
        },
        get_filepaths() {
            let all = [];
            axios.get('/api/mailscanner-configuration-filepaths/').then(response => {
                this.filepaths = response.data;
            });
        },
        submit() {
            if (this.id) {
                this.update();
            }
            else {
                this.add();
            }
        },
        add() {
            this.setLoading(true);
            this.form.post('/api/mailscanner-configuration/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Configuration option added', `The configuration option ${data.key} has been added`, 'success'));
                this.setLoading(false);
                router.push('/admin/mailscanner-configuration');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        update() {
            this.setLoading(true);
            this.form.put('/api/mailscanner-configuration/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Configuration option updated', `The configuration option ${data.key} has been updated`, 'success'));
                this.setLoading(false);
                router.push('/admin/mailscanner-configuration');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        destroy() {
            this.$modal.show('dialog', {
                title: 'Delete configuration option?',
                text: `Are you sure that you want to delete ${this.entity.key}?`,
                buttons: [
                    {
                        title: 'Yes',
                        handler: () => {
                            this.setLoading(true);
                            this.form.delete('/api/mailscanner-configuration/'+this.entity.id+'/').then(data => {
                                this.setLoading(false);
                                this.notify(this.createNotification('Configuration option deleted', `The configuration option ${this.entity.key} has been deleted`, 'success'));
                            }).catch(error => {
                                this.setLoading(false);
                                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
                            });
                            this.$modal.hide('dialog');
                            router.push('/admin/mailscanner-configuration');
                        },
                        default: true
                    },
                    {
                        title: 'No'
                    }
                ]
            });
        },
        ...mapMutations(['notify', 'setLoading'])
    }
}
</script>