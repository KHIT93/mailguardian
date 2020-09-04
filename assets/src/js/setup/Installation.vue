<template>
    <div>
        <template v-if="loading">
            <div class="text-center">
                <h1 class="text-2xl mb-2 text-center border-b pb-1">Installing</h1>
                <svg class="w-16 h-16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                    <circle cx="50" cy="50" fill="none" stroke-linecap="round" r="40" stroke-width="4" stroke="#000" stroke-dasharray="62.83185307179586 62.83185307179586" transform="rotate(66 50 50)">
                        <animateTransform attributeName="transform" type="rotate" calcMode="linear" values="0 50 50;360 50 50" keyTimes="0;1" dur="1s" begin="0s" repeatCount="indefinite"></animateTransform>
                    </circle>
                </svg>
                <p class="text-center">Please wait...</p>
            </div>
        </template>
        <div v-else-if="!loading && error" class="flex flex-col items-center">
            <h1 class="text-2xl mb-2 text-center border-b pb-1">Whoops! Something seems to have gone wrong</h1>
            <p class="py-2">{{getWizardPayload.errors}}</p>
            <button @click="submit" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 text-base rounded flex items-center" type="button">
                <span>Try again</span>
            </button>
        </div>
        <template v-else>
            <h1 class="text-2xl mb-2 text-center border-b pb-1">Confirm installation options</h1>
            <p class="text-center pb-1">
                Thank you for providing us wit the information necessary to customize the application to your liking.<br/>
                Please find below your selections and review them.<br/>
                If you need to go back and change some of the choices, please click the <code class="text-red-500 bg-gray-200 rounded p-1">Previous</code> button in the top right corner
            </p>
            <div>
                <h2 class="text-xl text-center border-b pb-1">Administrator details</h2>
                <div class="md:flex md:items-center mt-2">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="admin_email">
                        Email
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <p v-text="getWizardPayload.admin_email" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                    </div>
                </div>
                <div class="md:flex md:items-center mt-2">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="admin_password">
                        Password
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <p v-text="getWizardPayload.admin_password" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                    </div>
                </div>
                <h2 class="text-xl text-center border-b pb-1">Branding information</h2>
                <div class="md:flex md:items-center mt-2">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="branding_name">
                        Custom Application Name
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <p v-text="getWizardPayload.branding_name" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                    </div>
                </div>
                <div class="md:flex md:items-center mt-2">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="branding_tagline">
                        Custom Application Tagline
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <p v-text="getWizardPayload.branding_tagline" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                    </div>
                </div>
                <div class="md:flex md:items-center mt-2">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="branding_logo">
                        Custom Application Logo
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <p v-text="getWizardPayload.branding_logo" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                    </div>
                </div>
                <h2 class="text-xl text-center border-b pb-1">Quarantine settings</h2>
                <div class="md:flex md:items-center mt-2">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="quarantine_report_from">
                        Quarantine Email From
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <p v-text="getWizardPayload.quarantine_report_from" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                    </div>
                </div>
                <div class="md:flex md:items-center mt-2">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="quarantine_report_subject">
                        Quarantine Email Subject
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <p v-text="getWizardPayload.quarantine_report_subject" class="bg-gray-200 appearance-none border border-gray-200 rounded w-full py-2 px-4 text-gray-700"></p>
                    </div>
                </div>
                <div class="md:flex md:items-center mt-2">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="quarantine_report_daily">
                        Daily Quarantine Reports
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <label class="block">
                            <span class="text-sm" v-if="getWizardPayload.quarantine_report_daily">
                                Yes, allow users to get a daily quarantine report email from the application
                            </span>
                            <span class="text-sm" v-else>
                                No, do not allow users to get a daily quarantine report email from the application
                            </span>
                        </label>
                    </div>
                </div>
                <div class="md:flex md:items-center mt-2">
                    <div class="md:w-1/3">
                    <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="quarantine_report_non_spam_hide">
                        Hide clean email in the report?
                    </label>
                    </div>
                    <div class="md:w-2/3">
                        <label class="block">
                            <span class="text-sm" v-if="getWizardPayload.quarantine_report_non_spam_hide">
                                Yes, please hide messages, that are not stopped, from the email report
                            </span>
                            <span class="text-sm" v-else>
                                No, please show all messages in the email report
                            </span>
                        </label>
                    </div>
                </div>
                <div class="flex flex-row-reverse items-center justify-between pt-2">
                    <button @click="submit" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 text-base rounded flex items-center" type="button">
                        <span>Confirm</span>
                    </button>
                </div>
            </div>
        </template>
    </div>
</template>

<script>
import Form from '../classes/Form';
import { mapMutations, mapGetters } from 'vuex';
export default {
    data: () => {
        return {
            loading: false,
            error: false,
        }
    },
    computed: {
        ...mapGetters(['getWizardPayload'])
    },
    methods: {
        submit() {
            if (this.getWizardPayload instanceof Form) {
                this.loading = true;
                this.error = false;
                this.getWizardPayload.post('/api/setup/install/').then(response => {
                    this.setWizardPayload(null);
                    this.$emit('complete', { completed: true, action: 'auto' });
                }).catch(error => {
                    this.loading = false;
                    this.error = true;
                })
            }
        },
        ...mapMutations(['setWizardPayload'])
    }
}
</script>