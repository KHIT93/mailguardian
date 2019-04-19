<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="card p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="name">
                            Rule*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <v-select class="w-5/6" v-model="form.name" :options="availableRules"></v-select>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="score">
                            Score*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.score" class="form-input" name="score" id="score" type="text" placeholder="4.57" required>
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
import router from '../../../../routing/router';
import Form from '../../../../classes/Form';
export default {
    props: ['id'],
    data: () => {
        return {
            entity: {},
            form: {},
            availableRuleObjects: []
        }
    },
    created() {
        if (this.id) {
            this.get();
        }
        else {
            this.setLoading(false);
            this.form = new Form({
                name: '',
                score: 0.00,
            });
        }
        this.getAvailableRules();
    },
    computed: {
        availableRules() {
            let available =  this.availableRuleObjects.map((obj, index) => {
                return obj.key;
            })
            if (this.id && !available.includes(this.entity.name)) {
                available.push(this.entity.name);
            }
            return available;
        },
        ...mapGetters(['user'])
    },
    methods: {
        get() {
            this.setLoading(true);
            axios.get('/api/sa-rules/'+this.id+'/').then(response => {
                this.entity = response.data;
                this.form = new Form({
                    id: response.data.id,
                    name: response.data.name,
                    score: response.data.score,
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
            });
        },
        getAvailableRules() {
            this.setLoading(true);
            axios.get('/api/sa-rule-descriptions/available/').then(response => {
                this.availableRuleObjects = response.data;
                this.setLoading(false);
            }).catch(error => {
                this.setLoading(false);
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
            this.setLoading(true);
            this.form.post('/api/sa-rules/').then(data => {
                console.log(data);
                this.notify(this.createNotification('SpamAssassin Rule created', `The SpamAssassin Rule ${data.name} has been created`, 'success'));
                this.setLoading(false);
                router.push('/admin/spamassassin/rules');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        update() {
            this.setLoading(true);
            this.form.put('/api/sa-rules/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('SpamAssassin Rule updated', `The SpamAssassin Rule ${data.name} has been updated`, 'success'));
                this.setLoading(false);
                router.push('/admin/spamassassin/rules');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        destroy() {
            this.$modal.show('dialog', {
                title: 'Delete rule?',
                text: `Are you sure that you want to delete the ${this.entity.name} rule?`,
                buttons: [
                    {
                        title: 'Yes',
                        handler: () => {
                            this.setLoading(true);
                            this.form.delete('/api/sa-rules/'+this.entity.id+'/').then(data => {
                                this.setLoading(false);
                                this.notify(this.createNotification('SpamAssassin Rule deleted', `The SpamAssassin Rule ${data.name} has been deleted`, 'success'));
                            }).catch(error => {
                                this.setLoading(false);
                                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
                            });
                            this.$modal.hide('dialog');
                            router.push('/admin/spamassassin/rules');
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