<template>
    <Disclosure as="nav" class="bg-white shadow border-b" v-slot="{ open }">
        <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <div class="transition duration-300 flex text-gray-400 text-2xl hover:text-gray-800 focus:text-gray-800">
                            <ShieldCheckIcon class="h-8 w-8 text-blue-500" aria-hidden="true"/>
                            <span class="">MailGuardian</span>
                        </div>
                    </div>
                </div>
                <div class="hidden md:block">
                    <div class="ml-4 flex items-center md:ml-6">
                        <button class="transition duration-300 bg-white p-1 rounded-full text-gray-400 hover:text-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-gray-800">
                            <span class="sr-only">View notifications</span>
                            <BellIcon class="h-6 w-6" aria-hidden="true" />
                        </button>

                        <!-- Profile dropdown -->
                        <Menu as="div" class="ml-3 relative">
                            <div>
                                <MenuButton class="transition duration-300 max-w-xs bg-white text-gray-400 hover:text-gray-800 rounded-full flex items-center text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white">
                                    <span class="sr-only">Open user menu</span>
                                    <UserCircleIcon class="h-8 w-8" aria-hidden="true" />
                                </MenuButton>
                            </div>
                            <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                                <MenuItems class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                                    <MenuItem v-for="item in profile" :key="item" v-slot="{ active }">
                                        <a href="#" :class="[active ? 'bg-gray-100' : '', 'transition duration-300 block px-4 py-2 text-sm text-gray-700']">{{ item }}</a>
                                    </MenuItem>
                                    <MenuItem v-for="item in profile" :key="item" v-slot="{ active }">
                                        <a href="#" @click="signOut" :class="[active ? 'bg-gray-100' : '', 'transition duration-300 block px-4 py-2 text-sm text-gray-700']">Sign out</a>
                                    </MenuItem>
                                </MenuItems>
                            </transition>
                        </Menu>
                    </div>
                </div>
                <div class="-mr-2 flex md:hidden">
                    <!-- Mobile menu button -->
                    <DisclosureButton class="transition duration-300 bg-white inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white">
                        <span class="sr-only">Open main menu</span>
                        <MenuIcon v-if="!open" class="block h-6 w-6" aria-hidden="true" />
                        <XIcon v-else class="block h-6 w-6" aria-hidden="true" />
                    </DisclosureButton>
                </div>
            </div>
        </div>
        <DisclosurePanel class="md:hidden">
            <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                <template v-for="item in navigation" :key="item.to">
                    <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
                    <router-link :to="item.to" :class="'transition duration-300 block px-4 py-2 text-sm text-gray-700'">{{ item.name }}</router-link>
                </template>
            </div>
            <div class="pt-4 pb-3 border-t border-gray-700">
                <div class="flex items-center px-5">
                    <div class="flex-shrink-0">
                        <UserCircleIcon class="h-10 w-10" aria-hidden="true" />
                    </div>
                    <div class="ml-3">
                        <div class="text-base font-medium leading-none text-white">Tom Cook</div>
                        <div class="text-sm font-medium leading-none text-gray-400">tom@example.com</div>
                    </div>
                    <button class="transition duration-300 ml-auto bg-white flex-shrink-0 p-1 rounded-full text-gray-400 hover:text-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-gray-800">
                        <span class="sr-only">View notifications</span>
                        <BellIcon class="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <div class="mt-3 px-2 space-y-1">
                    <router-link v-for="item in profile" :key="item.to" :to="item.to" class="transition duration-300 block px-3 py-2 rounded-md text-base font-medium text-gray-400 hover:text-white hover:bg-gray-700">{{ item.name }}</router-link>
                    <a href="#" @click="signOut" class="transition duration-300 block px-3 py-2 rounded-md text-base font-medium text-gray-400 hover:text-white hover:bg-gray-700">Sign out</a>
                </div>
            </div>
        </DisclosurePanel>
    </Disclosure>
</template>

<script>
import { ref } from 'vue'
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { BellIcon, MenuIcon, XIcon, ShieldCheckIcon, MailIcon, LockClosedIcon, ChartBarIcon, UserGroupIcon, GlobeIcon, ServerIcon, DocumentSearchIcon } from '@heroicons/vue/outline'
import { UserCircleIcon } from '@heroicons/vue/solid'
import navigation from '../data/menu'
import profile from '../data/profile'
export default {
    components: {
        Disclosure,
        DisclosureButton,
        DisclosurePanel,
        Menu,
        MenuButton,
        MenuItem,
        MenuItems,
        BellIcon,
        MenuIcon,
        XIcon,
        UserCircleIcon,
        ShieldCheckIcon,
        MailIcon,
        LockClosedIcon,
        ChartBarIcon,
        UserGroupIcon,
        GlobeIcon,
        ServerIcon,
        DocumentSearchIcon
    },
    setup(props) {
        let open = ref(false)
        // let navigation = ['Dashboard', 'Lists', 'Statistics', 'Users', 'Domains', 'Cluster', 'Audit', 'SpamAssassin Rules', 'Settings', 'Notification Manager']
        // let profile = ['Settings', 'Sign out']
        return {
            navigation,
            profile,
            open
        }
    },
    methods: {
        signOut() {
            this.$auth.logout()
        }
    }
}
</script>