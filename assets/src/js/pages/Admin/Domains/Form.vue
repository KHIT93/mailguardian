<template>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="bg-white border sm:rounded shadow p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            Name*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.name" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="name" id="name" type="text" placeholder="example.com" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            Destination*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.destination" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="name" id="name" type="text" placeholder="mail.example.com" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            Relay type
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <div class="relative">
                            <select v-model="form.relay_type" class="block appearance-none w-full bg-grey-lighter hover:border-blue border border-grey-lighter text-grey-darker py-2 px-4">
                                <option value="">Select relay type</option>
                                <option value="smtp">Deliver to my email server (SMTP)</option>
                                <option value="smtps">Deliver to my email server (SMTP with SSL/TLS)</option>
                            </select>
                            <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="multi_node">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            Receive type
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <div class="relative">
                            <select v-model="form.receive_type" class="block appearance-none w-full bg-grey-lighter hover:border-blue border border-grey-lighter text-grey-darker py-2 px-4">
                                <option value="">Select Receive type</option>
                                <option value="load_balanced">Balance between nodes</option>
                                <option value="failover">Use the primary node and fail over if unavailable</option>
                            </select>
                            <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4" for="username">
                            <input v-model="form.active" class="mr-2" type="checkbox" />
                            <span class="text-sm">This domain is active</span>
                        </label>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="entity.active">
                    <div class="md:w-1/6"></div>
                    <div class="md:w-3/5 bg-grey-lighter p-1">
                        <h3 class="text-center p-1">DNS Configuration</h3>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Type</th>
                                    <th>Priority</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!hosts.length">
                                    <td>{{entity.name}}</td>
                                    <td>MX</td>
                                    <td>10</td>
                                    <td>{{app_info.mailguardian_host}}test</td>
                                </tr>
                                <tr v-else v-for="host in hosts" :key="host.id">
                                    <td>{{entity.name}}</td>
                                    <td>MX</td>
                                    <td>{{ entity.receive_type == 'load_balanced' ? 10 : host.priority }}</td>
                                    <td>{{host.hostname}}</td>
                                </tr>
                            </tbody>
                        </table>
                        <h4 class="text-center p-1 border-b">BIND Zone file example</h4>
                        <samp class="text-center">
                            <p v-if="!hosts.length">
                                {{entity.name}}. IN MX 10 {{app_info.mailguardian_host}}
                            </p>
                            <p v-else v-for="host in hosts" :key="host.id">
                                {{entity.name}}. IN MX {{ entity.receive_type == 'load_balanced' ? 10 : host.priority}} {{host.hostname}}
                            </p>
                        </samp>

                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            Allowed accounts*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.allowed_accounts" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="name" id="name" type="number" required min="-1">
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
import router from '../../../routing/router';
import Form from '../../../classes/Form';
export default {
    props: ['id'],
    data: () => {
        return {
            entity: {},
            form: {},
            hosts: []
        }
    },
    mounted() {
        if (this.id) {
            this.get();
        }
        else {
            this.form = new Form({
                name: '',
                destination: '',
                relay_type: '',
                active: '',
                allowed_accounts: null,
                receive_type: 'failover'
            });
        }
        this.getHosts();
    },
    computed: {
        multi_node() {
            return this.app_info.mailguardian_multi_node;
        },
        ...mapGetters(['user', 'app_info'])
    },
    methods: {
        get() {
            axios.get('/api/domains/'+this.id+'/').then(response => {
                this.entity = response.data;
                this.form = new Form({
                    id: response.data.id,
                    name: response.data.name,
                    destination: response.data.destination,
                    relay_type: response.data.relay_type,
                    active: response.data.active,
                    allowed_accounts: response.data.allowed_accounts,
                    receive_type: response.data.receive_type
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
        getHosts() {
            axios.get('/api/hosts/').then(response => {
                this.hosts = response.data.results;
            })
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
            this.form.post('/api/domains/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Domain created', `The domain ${data.name} has been created`, 'success'));
                router.push('/admin/domains');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        update() {
            this.form.put('/api/domains/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Domain updated', `The domain ${data.name} has been updated`, 'success'));
                router.push('/admin/domains');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        destroy() {
            this.form.delete('/api/domains/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Domain deleted', `The domain ${data.name} has been deleted`, 'success'));
                router.push('/admin/domains');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        ...mapMutations(['notify'])
    }
}
</script>

<style>

</style>
