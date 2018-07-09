<template>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="bg-white border sm:rounded shadow p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="name">
                            Rule*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <v-select class="w-5/6" v-model="form.name" label="name" :options="availableRules"></v-select>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="name">
                            Score*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.score" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="score" id="score" type="text" placeholder="4.57" required>
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
import { mapGetters, mapMutations } from 'vuex';
import router from '../../../../routing/router';
import Form from '../../../../classes/Form';
export default {
    props: ['id'],
    data: () => {
        return {
            entity: {},
            form: {},
            availableRules: []
        }
    },
    mounted() {
        if (this.id) {
            this.get();
        }
        else {
            this.form = new Form({
                name: '',
                score: 0.00,
            });
        }
        this.getAvailableRules();
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        get() {
            axios.get('/api/sa-rules/'+this.id+'/').then(response => {
                this.entity = response.data;
                this.form = new Form({
                    id: response.data.id,
                    name: response.data.name,
                    score: response.data.score,
                });
            }).catch(error => {
                if (error.response.status == 404) {
                    router.push({ name: 'not_found' });
                }
                else if (error.response.status == 403) {
                    router.push({ name: 'access_denied' });
                }
            });
        },
        getAvailableRules() {
            axios.get('/api/sa-rule-descriptions/available/').then(response => {
                this.availableRules = response.data;
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
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
            this.form.post('/api/sa-rules/').then(data => {
                console.log(data);
                this.notify(this.createNotification('SpamAssassin Rule created', `The SpamAssassin Rule ${data.name} has been created`, 'success'));
                router.push('/admin/spamassasin/rules');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        update() {
            this.form.put('/api/sa-rules/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('SpamAssassin Rule updated', `The SpamAssassin Rule ${data.name} has been updated`, 'success'));
                router.push('/admin/spamassassin/rules');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        destroy() {
            this.form.delete('/api/sa-rules/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('SpamAssassin Rule deleted', `The SpamAssassin Rule ${data.name} has been deleted`, 'success'));
                router.push('/admin/spamassassin/rules');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        ...mapMutations(['notify'])
    }
}
</script>