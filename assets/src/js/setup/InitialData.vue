<template>
    <div>
        <h1 class="text-2xl mb-2 text-center border-b pb-1">Initial Data Collection</h1>
        <p class="text-center pb-1">
            We new need to collect some important information so that we can configure the application to your liking.<br/>
            Please fill in the form below to do so
        </p>
        <form @submit.prevent="submit">
            <h2 class="text-xl text-center border-b pb-1">Administrator details</h2>
            <div class="md:flex md:items-center mt-2">
                <div class="md:w-1/3">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="admin_email">
                    Email
                </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.admin_email" class="form-input" name="admin_email" id="admin_email" type="email" placeholder="JaneDoe@example.com" required>
                    <p class="text-sm text-red pt-1" v-if="form.errors.has('admin_email')">{{ form.errors.get('admin_email') }}</p>
                </div>
            </div>
            <div class="md:flex md:items-center mt-2">
                <div class="md:w-1/3">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="admin_password">
                    Password
                </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.admin_password" class="form-input" name="admin_password" id="admin_password" type="password" placeholder="" required>
                    <p class="text-sm text-red pt-1" v-if="form.errors.has('admin_password')">{{ form.errors.get('admin_password') }}</p>
                </div>
            </div>
            <h2 class="text-xl text-center border-b pb-1">Branding information</h2>
            <p class="text-center pt-1">Here you can provide us some details if you want to brand the application in a specific way. You can leave the information is as, if you do not want to rebrand the application</p>
            <div class="md:flex md:items-center mt-2">
                <div class="md:w-1/3">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="branding_name">
                    Custom Application Name
                </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.branding_name" class="form-input" name="branding_name" id="branding_name" type="text">
                    <p class="text-sm text-red pt-1" v-if="form.errors.has('branding_name')">{{ form.errors.get('branding_name') }}</p>
                </div>
            </div>
            <div class="md:flex md:items-center mt-2">
                <div class="md:w-1/3">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="branding_tagline">
                    Custom Application Tagline
                </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.branding_tagline" class="form-input" name="branding_tagline" id="branding_tagline" type="text">
                    <p class="text-sm text-red pt-1" v-if="form.errors.has('branding_tagline')">{{ form.errors.get('branding_tagline') }}</p>
                </div>
            </div>
            <div class="md:flex md:items-center mt-2">
                <div class="md:w-1/3">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="branding_logo">
                    Custom Application Logo
                </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.branding_logo" class="form-input" name="branding_logo" id="branding_logo" type="text" placeholder="https://example.com/images/logo.svg">
                    <p class="text-xs pt-1"> Here you can provide us a link to a custom logo for the application</p>
                    <p class="text-sm text-red pt-1" v-if="form.errors.has('branding_logo')">{{ form.errors.get('branding_logo') }}</p>
                </div>
            </div>
            <h2 class="text-xl text-center border-b pb-1">Quarantine settings</h2>
            <div class="md:flex md:items-center mt-2">
                <div class="md:w-1/3">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="quarantine_report_from">
                    Quarantine Email From
                </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.quarantine_report_from" class="form-input" name="quarantine_report_from" id="quarantine_report_from" type="email" placeholder="postmaster@example.com" required>
                    <p class="text-sm text-red pt-1" v-if="form.errors.has('quarantine_report_from')">{{ form.errors.get('quarantine_report_from') }}</p>
                </div>
            </div>
            <div class="md:flex md:items-center mt-2">
                <div class="md:w-1/3">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="quarantine_report_subject">
                    Quarantine Email Subject
                </label>
                </div>
                <div class="md:w-2/3">
                    <input v-model="form.quarantine_report_subject" class="form-input" name="quarantine_report_subject" id="quarantine_report_subject" type="text">
                    <p class="text-sm text-red pt-1" v-if="form.errors.has('quarantine_report_subject')">{{ form.errors.get('quarantine_report_subject') }}</p>
                </div>
            </div>
            <div class="md:flex md:items-center mt-2">
                <div class="md:w-1/3">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="quarantine_report_daily">
                    Daily Quarantine Reports
                </label>
                </div>
                <div class="md:w-2/3">
                    <label class="block font-bold">
                        <input class="mr-2" type="checkbox" v-model="form.quarantine_report_daily">
                        <span class="text-sm">
                            Yes, allow users to get a daily quarantine report email from the application
                        </span>
                    </label>
                </div>
            </div>
            <div class="md:flex md:items-center mt-2">
                <div class="md:w-1/3">
                <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="quarantine_report_non_spam_hide">
                    Hide clean email in the report?
                </label>
                </div>
                <div class="md:w-2/3">
                    <label class="block font-bold">
                        <input class="mr-2" type="checkbox" v-model="form.quarantine_report_non_spam_hide">
                        <span class="text-sm">
                            Yes, please hide messages, that are not stopped, from the email report
                        </span>
                    </label>
                </div>
            </div>
            <div class="flex flex-row-reverse items-center justify-between pt-2">
                <button class="bg-blue hover:bg-blue-dark text-white py-2 px-4 text-base rounded flex items-center" type="submit">
                    <span>Save</span>
                </button>
            </div>
        </form>
    </div>
</template>

<script>
import Form from '../classes/Form';
import { mapMutations, mapGetters } from 'vuex';
export default {
    data: () => {
        return {
            form: new Form({
                admin_email: '',
                admin_password: '',
                branding_name: 'MailGuardian',
                branding_tagline: 'Securing your email',
                branding_logo: '',
                quarantine_report_from: '',
                quarantine_report_subject: 'MailGuardian Quarantine Report',
                quarantine_report_daily: false,
                quarantine_report_non_spam_hide: true
            })
        }
    },
    mounted() {
        if (this.getWizardPayload) {
            this.form = this.getWizardPayload;
        }
    },
    computed: {
        ...mapGetters(['getWizardPayload'])
    },
    methods: {
        submit() {
            this.setWizardPayload(this.form);
            this.$emit('complete', { completed: true, action: 'auto' })
        },
        ...mapMutations(['setWizardPayload'])
    }
}
</script>