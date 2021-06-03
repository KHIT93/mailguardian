<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <form @submit.prevent="update">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="email">
                            Email address*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <p v-text="user.email" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="name">
                            Name 
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <p v-text="user.first_name" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                        <p v-text="user.last_name" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="password">
                            Password
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <button type="button" class="cursor-pointer underline" @click.prevent="show_password_modal">Change password</button>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="password">
                            Two Factor Authentication
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                            <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-green-500': user.has_two_factor, 'bg-red-500': !user.has_two_factor }" >
                                {{ user.has_two_factor | yesno }}
                            </span>
                        </div>
                        <div v-if="user.has_two_factor">
                            <button type="button" class="cursor-pointer btn btn-red" @click.prevent="disable_two_factor">Disable 2FA</button>
                            <button type="button" class="cursor-pointer btn btn-orange" @click.prevent="get_backup_codes">Get 2FA Backup codes</button>
                        </div>
                        <button type="button" class="cursor-pointer btn btn-green" @click.prevent="enable_two_factor" v-else>Enable 2FA</button>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="user.is_staff">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="is_staff">
                            Are you a member of the staff?
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                            <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-green-500': user.is_staff, 'bg-gray-500': !user.is_staff }" >
                                {{ user.is_staff | yesno }}
                            </span>
                        </div>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="user.is_domain_admin || user.is_staff">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="is_domain_admin">
                            Are you an administrator of one or more domains?
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                            <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-green-500': user.is_domain_admin, 'bg-gray-500': !user.is_domain_admin }" >
                                {{ user.is_domain_admin | yesno }}
                            </span>
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
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="skip_scan">
                            Do not scan my email
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                            <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-red-500': user.skip_scan, 'bg-green-500': !user.skip_scan }" >
                                {{ user.skip_scan | yesno }}
                            </span>
                        </div>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="!user.skip_scan">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="custom_spam_score">
                            Spam score 
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <input v-model="form.custom_spam_score" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="custom_spam_score" id="custom_spam_score" type="number" placeholder="5.0">
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6" v-if="!form.skip_scan">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="custom_spam_highscore">
                            High Spam score 
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <input v-model="form.custom_spam_highscore" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" name="custom_spam_highscore" id="custom_spam_highscore" type="number" placeholder="15.0">
                    </div>
                </div>

                <div class="flex flex-row-reverse border-t pt-2">
                    <button type="submit" class="btn btn-blue shadow">
                        Submit
                    </button>
                </div>
            </form>
        </div>
    </div>
</mg-page>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex';
import router from '../routing/router';
import Form from '../classes/Form';
import UserDomainTable from '../components/UserDomainTable.vue';
import ChangePasswordModal from '../components/ChangePasswordModal.vue';
import Enable2FAModal from '../components/Enable2FAModal.vue';
import Show2FABackupCodesModal from '../components/Show2FABackupCodesModal.vue';
export default {
    data: () => {
        return {
            form: {}
        }
    },
    mounted() {
        this.setLoading(true);
        axios.post('/api/current-user/', {}).then(response => {
            this.form = new Form({
                id: response.data.id,
                daily_quarantine_report: response.data.daily_quarantine_report,
                weekly_quarantine_report: response.data.weekly_quarantine_report,
                monthly_quarantine_report: response.data.monthly_quarantine_report,
                custom_spam_score: response.data.custom_spam_score,
                custom_spam_highscore: response.data.custom_spam_highscore
            });
            this.setLoading(false);
        });
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        update() {
//            this.form.patch('/api/users/'+this.user.id+'/').then(data => {
            this.form.patch('/api/current-user/').then(data => {
                console.log(data);
                this.notify(this.createNotification('User updated', `The user ${data.email} has been updated`, 'success'));
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        enable_two_factor() {
            this.$modal.show(Enable2FAModal,{},
            {
                clickToClose: false,
                adaptive: true,
                height: 'auto'
            });
        },
        disable_two_factor() {
            this.$modal.show('dialog', {
                title: 'Disable 2FA?',
                text: `Are you sure that you want to disable Two-Factor Authentictation for your account?`,
                buttons: [
                    {
                        title: 'Yes',
                        handler: () => {
                            axios.delete('/api/two-factor/disable/').then(response => {
                                if (response.status == 204)
                                {
                                    this.getCurrentUser();
                                }
                            }).catch(error => {
                                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
                            });
                            this.$modal.hide('dialog');
                        },
                        default: true
                    },
                    {
                        title: 'No'
                    }
                ]
            });
        },
        get_backup_codes() {
            this.$modal.show(Show2FABackupCodesModal,{},
            {
                clickToClose: false,
                adaptive: true,
                height: 'auto'
            });
        },
        show_password_modal() {
            this.$modal.show(ChangePasswordModal,{},
            {
                clickToClose: false,
                adaptive: true,
                height: 'auto'
            });
        },
        ...mapMutations(['notify', 'setLoading']),
        ...mapActions(['getCurrentUser'])
    }
}
</script>