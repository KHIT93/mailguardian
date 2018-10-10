<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="card p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="ip_address">
                            IP Address*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.ip_address" class="form-input" name="ip_address" id="ip_address" type="text" placeholder="1.1.1.1/32" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="hostname">
                            Hostname*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.hostname" class="form-input" name="hostname" id="hostname" type="text" placeholder="mail.example.com" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4" for="active">
                            <input v-model="form.active" class="mr-2" type="checkbox" />
                            <span class="text-sm">This Relay is enabled and can send mail through our server(s)</span>
                        </label>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="comment">
                            Comment*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.comment" class="form-input" name="comment" id="comment" type="text" required>
                    </div>
                </div>
                <div class="flex flex-row-reverse border-t pt-2">
                    <button type="submit" class="btn btn-blue shadow">
                        Submit
                    </button>
                    <button v-if="id" @click="destroy" type="button" class="mr-1 flex-no-shrink bg-red hover:bg-red-dark border-red hover:border-red-dark text-sm border-4 text-white py-1 px-2 rounded shadow">
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
            form: {}
        }
    },
    created() {
        if (this.id) {
            this.get();
        }
        else {
            this.setLoading(false);
            this.form = new Form({
                ip_address: '',
                hostname: '',
                active: false,
                comment: ''
            });
        }
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        get() {
            this.setLoading(true);
            axios.get('/api/smtp-relays/'+this.id+'/').then(response => {
                this.entity = response.data;
                this.form = new Form({
                    id: response.data.id,
                    ip_address: response.data.ip_address,
                    hostname: response.data.hostname,
                    active: response.data.active,
                    comment: response.data.comment
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
            this.form.post('/api/smtp-relays/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Relay created', `The Relay ${data.ip_address} has been created`, 'success'));
                this.setLoading(false);
                router.push('/admin/smtp-relays');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        update() {
            this.setLoading(true);
            this.form.put('/api/smtp-relays/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Relay updated', `The Relay ${data.ip_address} has been updated`, 'success'));
                this.setLoading(false);
                router.push('/admin/smtp-relays');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        destroy() {
            this.$modal.show('dialog', {
                title: 'Delete relay?',
                text: `Are you sure that you want to delete ${this.entity.ip_address} from the list of hosts that are allowed to send email through us?`,
                buttons: [
                    {
                        title: 'Yes',
                        handler: () => {
                            this.setLoading(true);
                            this.form.delete('/api/smtp-relays/'+this.entity.id+'/').then(data => {
                                this.setLoading(false);
                                this.notify(this.createNotification('Relay deleted', `The Relay ${this.entity.ip_address} has been deleted`, 'success'));
                            }).catch(error => {
                                this.setLoading(false);
                                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
                            });
                            this.$modal.hide('dialog');
                            router.push('/admin/smtp-relays');
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