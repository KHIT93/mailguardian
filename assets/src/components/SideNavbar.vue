<template>
    <aside class="hidden md:block md:w-1/4 xl:w-1/5 bg-blue-gray-100 pr-8 pt-6">
        <router-link to="/" class="transition duration-300 flex items-center rounded-r-full text-gray-700 font-bold p-1 pl-6 hover:bg-blue-gray-200" exact-active-class="bg-blue-200 text-blue-500 hover:bg-blue-300">
            <MailIcon class="h-6 w-6" aria-hidden="true" />
            <span class="pl-4 pr-2">Dashboard</span>
        </router-link>
        <router-link to="/lists" class="transition duration-300 flex items-center rounded-r-full text-gray-700 font-base p-1 pl-6 hover:bg-blue-gray-200" v-slot="{ isActive }" :class="{ 'FIXME': isActive }" active-class="bg-blue-200 text-blue-500 hover:bg-blue-300">
            <LockClosedIcon class="h-6 w-6" aria-hidden="true" />
            <span class="pl-4 pr-2">Allow/Deny lists</span>
        </router-link>
        <router-link to="/statistics" class="transition duration-300 flex items-center rounded-r-full text-gray-700 font-base p-1 pl-6 hover:bg-blue-gray-200" active-class="bg-blue-200 text-blue-500 hover:bg-blue-300">
            <ChartBarIcon class="h-6 w-6" aria-hidden="true" />
            <span class="pl-4 pr-2">Statistics</span>
        </router-link>
        <hr/>
        <h2 class="text-xs uppercase text-blue-gray-300 font-bold pl-3 pr-2 py-2">Management</h2>
        <router-link to="/users" class="transition duration-300 flex items-center rounded-r-full text-gray-700 font-base p-1 pl-6 hover:bg-blue-gray-200" active-class="bg-blue-200 text-blue-500 hover:bg-blue-300">
            <UserGroupIcon class="h-6 w-6" aria-hidden="true" />
            <span class="pl-4 pr-2">Users</span>
        </router-link>
        <router-link to="/domains" class="transition duration-300 flex items-center rounded-r-full text-gray-700 font-base p-1 pl-6 hover:bg-blue-gray-200" active-class="bg-blue-200 text-blue-500 hover:bg-blue-300">
            <GlobeIcon class="h-6 w-6" aria-hidden="true" />
            <span class="pl-4 pr-2">Domains</span>
        </router-link>
        <router-link to="/cluster" class="transition duration-300 flex items-center rounded-r-full text-gray-700 font-base p-1 pl-6 hover:bg-blue-gray-200" active-class="bg-blue-200 text-blue-500 hover:bg-blue-300">
            <ServerIcon class="h-6 w-6" aria-hidden="true" />
            <span class="pl-4 pr-2">Cluster</span>
        </router-link>
        <router-link to="/audit" class="transition duration-300 flex items-center rounded-r-full text-gray-700 font-base p-1 pl-6 hover:bg-blue-gray-200" active-class="bg-blue-200 text-blue-500 hover:bg-blue-300">
            <DocumentSearchIcon class="h-6 w-6" aria-hidden="true" />
            <span class="pl-4 pr-2">Audit</span>
        </router-link>
    </aside>
</template>

<script>
import { MailIcon, LockClosedIcon, ChartBarIcon, UserGroupIcon, GlobeIcon, ServerIcon, DocumentSearchIcon } from '@heroicons/vue/outline'
export default {
    components: {
        MailIcon,
        LockClosedIcon,
        ChartBarIcon,
        UserGroupIcon,
        GlobeIcon,
        ServerIcon,
        DocumentSearchIcon
    }
}
</script>