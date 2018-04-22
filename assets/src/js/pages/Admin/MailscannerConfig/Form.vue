<template>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="bg-white border sm:rounded shadow p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="key">
                            Key*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.key" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="key" id="key" type="text" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="value">
                            Value
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.value" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="value" id="value" type="text">
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            File
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <div v-if="form.id" class="text-grey-light">{{ form.filepath }}</div>
                        <div class="relative" v-else>
                            <select v-model="form.filepath" class="block appearance-none w-full bg-grey-lighter hover:border-blue border border-grey-lighter text-grey-darker py-2 px-4">
                                <option value="">-- Select file --</option>
                                <option v-for="f in filepaths" :key="f.filepath" :value="f.filepath">{{ f.filepath }}</option>
                            </select>
                            <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex flex-row-reverse border-t pt-2">
                    <button type="submit" class="flex-no-shrink bg-blue hover:bg-blue-dark border-blue hover:border-blue-dark text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Submit
                    </button>
                    <button v-if="id" @click="destroy" type="button" class="mr-1 flex-no-shrink bg-red hover:bg-red-dark border-red hover:border-red-dark text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Delete
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
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
    mounted() {
        if (this.id) {
            this.get();
        }
        else {
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
            axios.get('/api/mailscanner-configuration/'+this.id+'/').then(response => {
                this.entity = response.data;
                this.form = new Form({
                    id: response.data.id,
                    key: response.data.key,
                    value: response.data.value,
                    filepath: response.data.filepath,
                });
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
            this.form.post('/api/mailscanner-configuration/').then(data => {
                console.log(data);
                router.push('/admin/mailscanner-configuration');
            })
        },
        update() {
            this.form.put('/api/mailscanner-configuration/'+this.entity.id+'/').then(data => {
                console.log(data);
                router.push('/admin/mailscanner-configuration');
            })
        },
        destroy() {
            this.form.delete('/api/mailscanner-configuration/'+this.entity.id+'/').then(data => {
                console.log(data);
                router.push('/admin/mailscanner-configuration');
            });
        }
    }
}
</script>