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
                                                <label for="first-name" class="block text-sm font-medium text-gray-700">First name</label>
                                                <input type="text" name="first-name" id="first-name" v-model="record.first_name" autocomplete="cc-given-name" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-gray-900 focus:border-gray-900 sm:text-sm" />
                                            </div>

                                            <div class="col-span-4 sm:col-span-2">
                                                <label for="last-name" class="block text-sm font-medium text-gray-700">Last name</label>
                                                <input type="text" name="last-name" id="last-name" v-model="record.last_name" autocomplete="cc-family-name" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-gray-900 focus:border-gray-900 sm:text-sm" />
                                            </div>

                                            <div class="col-span-4 sm:col-span-2">
                                                <label for="email-address" class="block text-sm font-medium text-gray-700">Email address</label>
                                                <input type="email" name="email-address" id="email-address" v-model="record.email" autocomplete="email" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-gray-900 focus:border-gray-900 sm:text-sm" />
                                            </div>
                                        </div>
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
                                                <span class="flex-grow">{{ boolToHuman(record.has_two_factor) }}</span>
                                                <span class="ml-4 flex-shrink-0">
                                                <button type="button" class="bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                                    Enable
                                                </button>
                                                </span>
                                            </dd>
                                        </div>
                                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:pt-5">
                                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                                Application Administrator
                                            </SwitchLabel>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <Switch v-model="record.is_staff" :class="[record.is_staff ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                                <span aria-hidden="true" :class="[record.is_staff ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                                </Switch>
                                            </dd>
                                        </SwitchGroup>
                                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:border-b sm:border-gray-200">
                                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                                Domain Administrator
                                            </SwitchLabel>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <Switch v-model="record.is_domain_admin" :class="[record.is_domain_admin ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
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
                                                <Switch v-model="record.daily_quarantine_report" :class="[record.daily_quarantine_report ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                                <span aria-hidden="true" :class="[record.daily_quarantine_report ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                                </Switch>
                                            </dd>
                                        </SwitchGroup>
                                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:border-b sm:border-gray-200">
                                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                                Weekly Reports
                                            </SwitchLabel>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <Switch v-model="record.weekly_quarantine_report" :class="[record.weekly_quarantine_report ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
                                                <span aria-hidden="true" :class="[record.weekly_quarantine_report ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                                                </Switch>
                                            </dd>
                                        </SwitchGroup>
                                        <SwitchGroup as="div" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:border-b sm:border-gray-200">
                                            <SwitchLabel as="dt" class="text-sm font-medium text-gray-500" passive>
                                                Monthly Reports
                                            </SwitchLabel>
                                            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                                <Switch v-model="record.monthly_quarantine_report" :class="[record.monthly_quarantine_report ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-auto']">
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
                                <!-- CONTENT GOES HERE -->
                            </TabPanel>
                        </TabPanels>
                    </TabGroup>
                </div>
            </div>
            <div class="pt-5">
                <div class="flex justify-end">
                    <button type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                        Cancel
                    </button>
                    <button type="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                        Save
                    </button>
                </div>
            </div>
        </div>
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
} from '@headlessui/vue'
import { boolToHuman } from '../filters'
import { onMounted, ref } from '@vue/runtime-core'
import { useAuth } from '@websanova/vue-auth'
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
        Switch
    },
    setup(props) {
        const auth = useAuth()
        let record = ref({})

        onMounted(async () => {
            record.value = (await auth.fetch()).data
        })

        return {
            record,
            boolToHuman
        }
    }
}
</script>