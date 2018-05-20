<template>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="bg-white border sm:rounded shadow p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            Email address*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.email" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="email" id="email" type="text" placeholder="JaneDoe@example.com" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            Name 
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <input v-model="form.first_name" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker mr-1" name="first_name" id="first_name" type="text" placeholder="Jane">
                        <input v-model="form.last_name" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="last_name" id="last_name" type="text" placeholder="Doe">
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="username">
                            Password
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <button type="button" class="cursor-pointer underline" @click.prevent="show_password_modal = true">Change password</button>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4" for="username">
                            <input v-model="form.is_staff" class="mr-2" type="checkbox" />
                            <span class="text-sm">This user is a member of the staff</span>
                        </label>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4" for="username">
                            <input v-model="form.is_domain_admin" class="mr-2" type="checkbox" />
                            <span class="text-sm">This user is the administrator of one or more domains</span>
                        </label>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="!form.is_staff">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <mw-user-domains :domains="form.domains" @submit="addDomain" @destroy="removeDomain"></mw-user-domains>
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
        <mw-change-password-modal @close="show_password_modal = false" @submit="show_password_modal = false" :show="show_password_modal" :user-id="entity.id"></mw-change-password-modal>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import router from '../../../routing/router';
import Form from '../../../classes/Form';
import UserDomainTable from '../../../components/UserDomainTable.vue';
import ChangePasswordModal from '../../../components/ChangePasswordModal.vue';
export default {
    props: ['id'],
    components: {
        'mw-user-domains': UserDomainTable,
        'mw-change-password-modal': ChangePasswordModal
    },
    data: () => {
        return {
            entity: {},
            form: {},
            show_password_modal: false
        }
    },
    mounted() {
        if (this.id) {
            this.get();
        }
        else {
            this.form = new Form({
                username: '',
                email: '',
                first_name: '',
                last_name: '',
                is_staff: false,
                is_domain_admin: false,
                domains: []
            });
        }
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        get() {
            axios.get('/api/users/'+this.id+'/').then(response => {
                this.entity = response.data;
                this.form = new Form({
                    id: response.data.id,
                    username: response.data.username,
                    email: response.data.email,
                    first_name: response.data.first_name,
                    last_name: response.data.last_name,
                    is_staff: response.data.is_staff,
                    is_domain_admin: response.data.is_domain_admin,
                    domains: []
                });
            })
            axios.get('/api/users/'+this.id+'/domains/').then(response => {
                this.form.domains = response.data;
            });
        },
        submit() {
            this.form.domains = this.form.domains.map(domain => domain.url);
            if (this.id) {
                this.update();
            }
            else {
                this.add();
            }
        },
        add() {
            this.form.post('/api/users/').then(data => {
                console.log(data);
                this.notify(this.createNotification('User added', `The user ${data.email} has been added`, 'success'));
                router.push('/admin/users');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        update() {
            this.form.put('/api/users/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('User updated', `The user ${data.email} has been updated`, 'success'));
                router.push('/admin/users');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        destroy() {
            this.form.delete('/api/users/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('User deleted', `The user ${this.entity.email} has been deleted`, 'success'));
                router.push('/admin/users');
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        addDomain(domain) {
            this.form.domains.push(domain);
        },
        removeDomain(domain) {
            this.form.domains.splice(this.form.domains.findIndex(d => d === domain), 1);
        },
        ...mapMutations(['notify'])
    }
}
</script>

<style>

</style>
