<template>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="bg-white border sm:rounded shadow p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="hostname">
                            Hostname*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.hostname" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="hostname" id="hostname" type="text" placeholder="mailnode-01.example.com" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="ip_address">
                            IP Address*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.ip_address" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="ip_address" id="ip_address" type="text" placeholder="1.1.1.1" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4" for="use_tls">
                            <input v-model="form.use_tls" class="mr-2" type="checkbox" />
                            <span class="text-sm">Communicate with this host using SSL/TLS encryption</span>
                        </label>
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
            form: {}
        }
    },
    mounted() {
        if (this.id) {
            this.get();
        }
        else {
            this.form = new Form({
                hostname: '',
                ip_address: '',
                use_tls: true
            });
        }
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        get() {
            axios.get('/api/hosts/'+this.id+'/').then(response => {
                this.entity = response.data;
                this.form = new Form({
                    id: response.data.id,
                    hostname: response.data.hostname,
                    ip_address: response.data.ip_address,
                    use_tls: response.data.use_tls
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
        submit() {
            if (this.id) {
                this.update();
            }
            else {
                this.add();
            }
        },
        add() {
            this.form.post('/api/hosts/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Host created', `The Host ${data.name} has been created`, 'success'));
                router.push('/admin/hosts');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        update() {
            this.form.put('/api/hosts/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Host updated', `The Host ${data.name} has been updated`, 'success'));
                router.push('/admin/hosts');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        destroy() {
            this.form.delete('/api/hosts/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Host deleted', `The Host ${data.name} has been deleted`, 'success'));
                router.push('/admin/hosts');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        ...mapMutations(['notify'])
    }
}
</script>