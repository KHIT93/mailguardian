<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-6 pb-8">
        <div class="card p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="email">
                            Email address*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.email" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="email" id="email" type="text" placeholder="JaneDoe@example.com" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="first_name">
                            Name 
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <input v-model="form.first_name" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1 mr-1" name="first_name" id="first_name" type="text" placeholder="Jane">
                        <input v-model="form.last_name" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="last_name" id="last_name" type="text" placeholder="Doe">
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="password">
                            Password
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <button type="button" class="cursor-pointer underline" @click="show_password_modal">Change password</button>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4" v-if="user.is_staff">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="password">
                            Two Factor Authentication
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                            <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-green-500': entity.has_two_factor, 'bg-red-500': !entity.has_two_factor }" >
                                {{ entity.has_two_factor | yesno }}
                            </span>
                        </div>
                        <button type="button" class="cursor-pointer btn btn-red" @click.prevent="force_disable_two_factor" v-if="entity.has_two_factor">Force Disable 2FA</button>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <div class="text-gray-700 text-sm">
                            <label class="inline-flex items-center">
                                <input type="checkbox" class="form-checkbox h-4 w-4" v-model="form.is_staff" name="is_staff">
                                <span class="ml-2">This user is a member of the staff</span>
                            </label>
                        </div>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <div class="text-gray-700 text-sm">
                            <label class="inline-flex items-center">
                                <input type="checkbox" class="form-checkbox h-4 w-4" v-model="form.is_domain_admin" name="is_domain_admin">
                                <span class="ml-2">This user is the administrator of one or more domains</span>
                            </label>
                        </div>
                    </div>
                </div>

                <div class="md:flex md:items-center mb-2">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <h3 class="border-b pb-1">Spam settings</h3>
                    </div>
                </div>

                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <div class="text-gray-700 text-sm">
                            <label class="inline-flex items-center">
                                <input type="checkbox" class="form-checkbox h-4 w-4" v-model="form.daily_quarantine_report" name="daily_quarantine_report">
                                <span class="ml-2">Send daily quarantine reports</span>
                            </label>
                        </div>
                    </div>
                </div>

                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <div class="text-gray-700 text-sm">
                            <label class="inline-flex items-center">
                                <input type="checkbox" class="form-checkbox h-4 w-4" v-model="form.weekly_quarantine_report" name="weekly_quarantine_report">
                                <span class="ml-2">Send weekly quarantine reports</span>
                            </label>
                        </div>
                    </div>
                </div>

                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <div class="text-gray-700 text-sm">
                            <label class="inline-flex items-center">
                                <input type="checkbox" class="form-checkbox h-4 w-4" v-model="form.monthly_quarantine_report" name="monthly_quarantine_report">
                                <span class="ml-2">Send monthly quarantine reports</span>
                            </label>
                        </div>
                    </div>
                </div>

                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <div class="text-gray-700 text-sm">
                            <label class="inline-flex items-center">
                                <input type="checkbox" class="form-checkbox h-4 w-4" v-model="form.skip_scan" name="skip_scan">
                                <span class="ml-2">Do not scan email for this user</span>
                            </label>
                        </div>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="!form.skip_scan">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="custom_spam_score">
                            Spam score 
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <input v-model="form.custom_spam_score" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="custom_spam_score" id="custom_spam_score" type="text" placeholder="Doe">
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="!form.skip_scan">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="custom_spam_highscore">
                            High Spam score 
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <input v-model="form.custom_spam_highscore" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="custom_spam_highscore" id="custom_spam_highscore" type="text" placeholder="Doe">
                    </div>
                </div>

                <div class="md:flex md:items-center mb-1" v-if="!form.is_staff">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <h3>Domains</h3>
                    </div>
                </div>

                <div class="md:flex md:items-center mb-6" v-if="!form.is_staff">
                    <div class="md:w-1/4"></div>
                    <div class="md:w-1/2">
                        <mg-user-domains :domains="form.domains" @submit="addDomain" @destroy="removeDomain"></mg-user-domains>
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
import UserDomainTable from '../../../components/UserDomainTable.vue';
import ChangePasswordModal from '../../../components/ChangePasswordModal.vue';
export default {
    props: ['id'],
    components: {
        'mg-user-domains': UserDomainTable,
        'mg-change-password-modal': ChangePasswordModal
    },
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
                username: '',
                email: '',
                first_name: '',
                last_name: '',
                is_staff: false,
                is_domain_admin: false,
                custom_spam_score: 5.0,
                custom_spam_highscore: 15.0,
                skip_scan: false,
                domains: [],
                daily_quarantine_report: false,
                weekly_quarantine_report: false,
                monthly_quarantine_report: false
            });
        }
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        get() {
            this.setLoading(true);
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
                    custom_spam_score: response.data.custom_spam_score,
                    custom_spam_highscore: response.data.custom_spam_highscore,
                    skip_scan: response.data.skip_scan,
                    domains: [],
                    daily_quarantine_report: response.data.daily_quarantine_report,
                    weekly_quarantine_report: response.data.weekly_quarantine_report,
                    monthly_quarantine_report: response.data.monthly_quarantine_report
                });
                axios.get('/api/users/'+this.id+'/domains/').then(response => {
                    this.form.domains = response.data;
                }).catch(error => {
                    this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
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
        async submit() {
            this.form.domains = await this.form.domains.map(domain => domain.url);
            if (this.id) {
                this.update();
            }
            else {
                this.add();
            }
        },
        add() {
            this.setLoading(true);
            this.form.post('/api/users/').then(data => {
                console.log(data);
                this.notify(this.createNotification('User added', `The user ${data.email} has been added`, 'success'));
                this.setLoading(false);
                router.push('/admin/users');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        update() {
            this.setLoading(true);
            this.form.put('/api/users/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('User updated', `The user ${data.email} has been updated`, 'success'));
                this.setLoading(false);
                router.push('/admin/users');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        destroy() {
            this.$modal.show('dialog', {
                title: 'Delete user?',
                text: `Are you sure that you want to delete ${this.entity.email}?`,
                buttons: [
                    {
                        title: 'Yes',
                        handler: () => {
                            this.setLoading(true);
                            this.form.delete('/api/users/'+this.entity.id+'/').then(data => {
                                this.setLoading(false);
                                this.notify(this.createNotification('User deleted', `The user ${this.entity.email} has been deleted`, 'success'));
                            }).catch(error => {
                                this.setLoading(false);
                                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
                            });
                            this.$modal.hide('dialog');
                            router.push('/admin/users');
                        },
                        default: true
                    },
                    {
                        title: 'No'
                    }
                ]
            });
        },
        addDomain(domain) {
            this.form.domains.push(domain);
        },
        removeDomain(domain) {
            this.form.domains.splice(this.form.domains.findIndex(d => d === domain), 1);
        },
        show_password_modal() {
            this.$modal.show(ChangePasswordModal,{},
            {
                clickToClose: false,
                adaptive: true,
                height: 'auto'
            });
        },
        ...mapMutations(['notify', 'setLoading'])
    }
}
</script>

<style>

</style>
