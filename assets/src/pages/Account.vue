<template>
    <MainLayout>
        <div class="bg-white p-4 shadow border rounded-md space-y-8 sm:space-y-5 divide-y divide-gray-200">
            <div class="px-4 sm:px-6 md:px-0">
                <h1 class="text-3xl font-extrabold text-gray-900">Settings</h1>
            </div>
            <div class="px-4 sm:px-6 md:px-0">
                <div class="py-6">
                    <TabGroup>
                        <TabList class="flex p-1 space-x-1 rounded-xl">
                            <Tab as="template" v-slot="{ selected }">
                                <button
                                    :class="[
                                    'w-full py-2.5 border-b-2 text-sm leading-5 font-medium text-blue-500 transition-all',
                                    'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                                    selected
                                        ? 'border-blue-500 hover:bg-blue-500/[0.12]'
                                        : 'border-transparent text-blue-300 hover:bg-gray-300/[0.12] hover:text-blue-400',
                                    ]"
                                >
                                    General
                                </button>
                            </Tab>
                            <Tab as="template" v-slot="{ selected }">
                                <button
                                    :class="[
                                    'w-full py-2.5 border-b-2 text-sm leading-5 font-medium text-blue-500 transition-all',
                                    'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                                    selected
                                        ? 'border-blue-500 hover:bg-blue-500/[0.12]'
                                        : 'border-transparent text-blue-300 hover:bg-gray-300/[0.12] hover:text-blue-400',
                                    ]"
                                >
                                    Security
                                </button>
                            </Tab>
                            <Tab as="template" v-slot="{ selected }">
                                <button
                                    :class="[
                                    'w-full py-2.5 border-b-2 text-sm leading-5 font-medium text-blue-500 transition-all',
                                    'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                                    selected
                                        ? 'border-blue-500 hover:bg-blue-500/[0.12]'
                                        : 'border-transparent text-blue-300 hover:bg-gray-300/[0.12] hover:text-blue-400',
                                    ]"
                                >
                                    Email Filtering
                                </button>
                            </Tab>
                            <Tab as="template" v-slot="{ selected }" v-if="record.is_domain_admin">
                                <button
                                    :class="[
                                    'w-full py-2.5 border-b-2 text-sm leading-5 font-medium text-blue-500 transition-all',
                                    'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                                    selected
                                        ? 'border-blue-500 hover:bg-blue-500/[0.12]'
                                        : 'border-transparent text-blue-300 hover:bg-gray-300/[0.12] hover:text-blue-400',
                                    ]"
                                >
                                    Domains
                                </button>
                            </Tab>
                        </TabList>
                        <TabPanels class="mt-2">
                            <!-- General -->
                            <TabPanel :class="[
                                'bg-white rounded-xl p-3',
                                'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                            ]">
                                <div class="space-y-6 sm:px-6 lg:px-0 lg:col-span-9">
                                    <div class="space-y-8 sm:space-y-5 divide-y divide-gray-200 py-6 px-4 sm:p-6">
                                        <div>
                                            <h2 class="text-lg leading-6 font-medium text-gray-900">Who are you</h2>
                                            <p class="mt-1 text-sm text-gray-500">Update the information about you, such as your email used to log in to the system or your name</p>
                                        </div>

                                        <div class="pt-6 grid grid-cols-4 gap-6">
                                            <div class="col-span-4 sm:col-span-2">
                                                <FormInput inputId="first-name" label="First name" type="text" v-model="record.first_name"/>
                                            </div>

                                            <div class="col-span-4 sm:col-span-2">
                                                <FormInput inputId="last-name" label="Last name" type="text" v-model="record.last_name"/>
                                            </div>

                                            <div class="col-span-4 sm:col-span-2">
                                                <FormInput inputId="email" label="Email address" type="email" v-model="record.email"/>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex justify-end">
                                        <button type="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                            Save
                                        </button>
                                    </div>
                                </div>
                            </TabPanel>
                            <!-- Security -->
                            <TabPanel :class="[
                                'bg-white rounded-xl p-3',
                                'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                            ]">
                                <div class="mt-6">
                                    <dl class="divide-y divide-gray-200">
                                        <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
                                            <dt class="text-sm font-medium text-gray-500">
                                                Two-Factor Authentication
                                            </dt>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <span class="grow">{{ boolToHuman(record.has_two_factor) }}</span>
                                                <span class="ml-4 shrink-0">
                                                    <button type="button" v-if="!record.has_two_factor" @click="showMfaModal = true" class="bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                                        Enable
                                                    </button>
                                                    <button type="button" v-else-if="record.has_two_factor" @click="showMfaModal = true" class="bg-white rounded-md font-medium text-red-600 hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                                                        Disable
                                                    </button>
                                                    <button type="button" v-else-if="record.mfa_method_count > 1" class="bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                                        Manage
                                                    </button>
                                                </span>
                                            </dd>
                                        </div>
                                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:pt-5">
                                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                                Application Administrator
                                            </SwitchLabel>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <Switch v-model="record.is_staff" disabled :class="[record.is_staff ? 'bg-blue-300' : 'bg-gray-200', 'relative inline-flex shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-not-allowed transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                                    <span aria-hidden="true" :class="[record.is_staff ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                                </Switch>
                                            </dd>
                                        </SwitchGroup>
                                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:border-b sm:border-gray-200">
                                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                                Domain Administrator
                                            </SwitchLabel>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <Switch v-model="record.is_domain_admin" disabled :class="[record.is_domain_admin ? 'bg-blue-300' : 'bg-gray-200', 'relative inline-flex shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-not-allowed transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                                    <span aria-hidden="true" :class="[record.is_domain_admin ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                                </Switch>
                                            </dd>
                                        </SwitchGroup>
                                    </dl>
                                </div>
                            </TabPanel>
                            <!-- Email Filtering -->
                            <TabPanel :class="[
                                'bg-white rounded-xl p-3',
                                'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                            ]">
                                <div class="mt-6">
                                    <dl class="divide-y divide-gray-200">
                                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:pt-5">
                                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                                Daily Reports
                                            </SwitchLabel>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <svg v-if="dailyQuarantineReportToggle" class="relative inline-flex shrink-0 sm:ml-auto animate-spin mr-3 h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                </svg>
                                                <Switch v-else v-model="record.daily_quarantine_report" @click="toggleDailyReports" :class="[record.daily_quarantine_report ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                                    <span aria-hidden="true" :class="[record.daily_quarantine_report ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                                </Switch>
                                            </dd>
                                        </SwitchGroup>
                                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:border-b sm:border-gray-200">
                                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                                Weekly Reports
                                            </SwitchLabel>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <svg v-if="weeklyQuarantineReportToggle" class="relative inline-flex shrink-0 sm:ml-auto animate-spin mr-3 h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                </svg>
                                                <Switch v-else v-model="record.weekly_quarantine_report" @click="toggleWeeklyReports" :class="[record.weekly_quarantine_report ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                                    <span aria-hidden="true" :class="[record.weekly_quarantine_report ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                                </Switch>
                                            </dd>
                                        </SwitchGroup>
                                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:border-b sm:border-gray-200">
                                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                                Monthly Reports
                                            </SwitchLabel>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <svg v-if="monthlyQuarantineReportToggle" class="relative inline-flex shrink-0 sm:ml-auto animate-spin mr-3 h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                </svg>
                                                <Switch v-else v-model="record.monthly_quarantine_report" @click="toggleMonthlyReports" :class="[record.monthly_quarantine_report ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                                    <span aria-hidden="true" :class="[record.monthly_quarantine_report ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                                </Switch>
                                            </dd>
                                        </SwitchGroup>
                                    </dl>
                                </div>
                            </TabPanel>
                            <!-- Domains -->
                            <TabPanel :class="[
                                'bg-white rounded-xl p-3',
                                'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                            ]" v-if="record.is_domain_admin">
                                <table class="min-w-full divide-y divide-gray-200">
                                    <thead class="bg-white">
                                        <tr>
                                            <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                                Name
                                            </th>
                                            <th scope="col" class="relative px-6 py-3">
                                                <span class="sr-only">Delete</span>
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody class="bg-white">
                                        <template v-if="domains.length">
                                            <tr v-for="domain in domains" :key="domain.pk" class="cursor-pointer border-b transition duration-300 hover:shadow-lg hover:font-bold">
                                                <td class="px-6 py-2 whitespace-nowrap text-sm text-gray-700 truncate">
                                                    {{ domain.name }}
                                                </td>
                                                <td class="px-6 whitespace-nowrap text-right text-sm font-medium">
                                                    <button type="button" class="text-red-600 hover:text-red-900">
                                                        <TrashIcon class="w-4 h-4"/>
                                                    </button>
                                                </td>
                                            </tr>
                                        </template>
                                        <tr v-else>
                                            <td class="px-6 py-2 whitespace-nowrap" colspan="99">
                                                <span class="px-2 inline-flex text-xs leading-5 font-semibold">
                                                    No domains are currently linked
                                                </span>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </TabPanel>
                        </TabPanels>
                    </TabGroup>
                </div>
            </div>
            <div class="pt-5">
            </div>
        </div>
        <!--
            Modals go here
        -->
        <TransitionRoot appear :show="showMfaModal" as="template">
            <Dialog as="div" @close="closeMfaModal">
                <div class="fixed inset-0 z-10 overflow-y-auto">
                    <div class="min-h-screen px-4 text-center">
                        <TransitionChild
                            as="template"
                            enter="duration-300 ease-out"
                            enter-from="opacity-0"
                            enter-to="opacity-100"
                            leave="duration-200 ease-in"
                            leave-from="opacity-100"
                            leave-to="opacity-0"
                            >
                            <DialogOverlay class="fixed inset-0 bg-black opacity-30" />
                        </TransitionChild>
                        <span class="inline-block h-screen align-middle" aria-hidden="true">
                        &#8203;
                        </span>
                        <TransitionChild v-if="!record.has_two_factor"
                            as="template"
                            enter="duration-300 ease-out"
                            enter-from="opacity-0 scale-95"
                            enter-to="opacity-100 scale-100"
                            leave="duration-200 ease-in"
                            leave-from="opacity-100 scale-100"
                            leave-to="opacity-0 scale-95"
                            >
                            <EnableMfaDialog @close="closeMfaModal" />
                        </TransitionChild>
                        <TransitionChild v-else-if="record.has_two_factor && record.mfa_method_count == 1"
                            as="template"
                            enter="duration-300 ease-out"
                            enter-from="opacity-0 scale-95"
                            enter-to="opacity-100 scale-100"
                            leave="duration-200 ease-in"
                            leave-from="opacity-100 scale-100"
                            leave-to="opacity-0 scale-95"
                            >
                            <DisableMfaDialog @close="closeMfaModal" :method="record.mfa_methods[0].name" />
                        </TransitionChild>
                    </div>
                </div>
            </Dialog>
        </TransitionRoot>
    </MainLayout>
</template>

<script>
import MainLayout from '../components/MainLayout.vue'
import {
    Tab,
    TabGroup,
    TabList,
    TabPanels,
    TabPanel,
    Switch,
    SwitchGroup,
    SwitchLabel,
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogOverlay,
    DialogTitle,
} from '@headlessui/vue'
import { TrashIcon } from '@heroicons/vue/outline'
import { boolToHuman } from '../filters'
import { onMounted, ref } from '@vue/runtime-core'
import { useAuth } from '@websanova/vue-auth'
import FormInput from '../components/FormInput.vue'
import EnableMfaDialog from '../components/EnableMfaDialog.vue'
import DisableMfaDialog from '../components/DisableMfaDialog.vue'
export default {
    components: {
        MainLayout,
        Tab,
        TabGroup,
        TabList,
        TabPanels,
        TabPanel,
        SwitchLabel,
        SwitchGroup,
        Switch,
        TrashIcon,
        FormInput,
        TransitionRoot,
        TransitionChild,
        Dialog,
        DialogOverlay,
        DialogTitle,
        EnableMfaDialog,
        DisableMfaDialog,
    },
    setup(props) {
        const auth = useAuth()
        let record = ref({})
        let domains = ref([])
        let dailyQuarantineReportToggle = ref(false)
        let weeklyQuarantineReportToggle = ref(false)
        let monthlyQuarantineReportToggle = ref(false)
        let showNewDomainForm = ref(false)
        let showMfaModal = ref(false)

        onMounted(async () => {
            record.value = (await auth.fetch()).data
            domains.value = (await axios.get(`/api/users/${record.value.id}/domains/`)).data
        })

        return {
            record,
            domains,
            boolToHuman,
            showNewDomainForm,
            dailyQuarantineReportToggle,
            weeklyQuarantineReportToggle,
            monthlyQuarantineReportToggle,
            showMfaModal
        }
    },
    methods: {
        async toggleDailyReports() {
            console.log(this.record.id)
            this.dailyQuarantineReportToggle = true
            await axios.patch(`/api/users/${this.record.id}/`, {
                daily_quarantine_report: this.record.daily_quarantine_report
            })
            this.dailyQuarantineReportToggle = false
        },
        async toggleWeeklyReports() {
            this.weeklyQuarantineReportToggle = true
            await axios.patch(`/api/users/${this.record.id}/`, {
                weekly_quarantine_report: this.record.weekly_quarantine_report
            })
            this.weeklyQuarantineReportToggle = false
        },
        async toggleMonthlyReports() {
            this.monthlyQuarantineReportToggle = true
            await axios.patch(`/api/users/${this.record.id}/`, {
                monthly_quarantine_report: this.record.monthly_quarantine_report
            })
            this.monthlyQuarantineReportToggle = false
        },
        patchBasicData() {
            axios.patch(`/api/users/${this.record.id}`, {
                first_name: record.first_name,
                last_name: record.last_name,
                email: record.email
            })
        },
        closeMfaModal() {
            this.showMfaModal = false
        }
    }
}
</script>