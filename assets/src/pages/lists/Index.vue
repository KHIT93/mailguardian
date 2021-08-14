<template>
    <MainLayout>
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
                        Blocked
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
                        Allowed
                    </button>
                </Tab>
            </TabList>
            <TabPanels class="mt-2">
                <TabPanel :class="[
                    'bg-white rounded-xl p-3',
                    'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                ]">
                    <ListEntryTable listing-type="block"/>
                </TabPanel>
                <TabPanel :class="[
                    'bg-white rounded-xl p-3',
                    'focus:outline-none ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                ]">
                    <ListEntryTable listing-type="allow"/>
                </TabPanel>
            </TabPanels>
        </TabGroup>
    </MainLayout>
</template>

<script>
import MainLayout from '../../components/MainLayout.vue'
import ListEntryTable from '../../components/ListEntryTable.vue'
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
export default {
    components: {
        MainLayout,
        ListEntryTable,
        TabGroup,
        TabList,
        Tab,
        TabPanels,
        TabPanel,
    }
}
</script>