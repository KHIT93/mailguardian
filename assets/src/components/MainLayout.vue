<template>
    <div class="text-sm h-screen flex overflow-hidden bg-gray-100">
        <TransitionRoot as="template" :show="open">
            <Dialog as="div" class="fixed inset-0 flex z-40 md:hidden" @close="open = false">
                <TransitionChild as="template" enter="transition-opacity ease-linear duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="transition-opacity ease-linear duration-300" leave-from="opacity-100" leave-to="opacity-0">
                    <DialogOverlay class="fixed inset-0 bg-gray-600 bg-opacity-75" />
                </TransitionChild>
                <TransitionChild as="template" enter="transition ease-in-out duration-300 transform" enter-from="-translate-x-full" enter-to="translate-x-0" leave="transition ease-in-out duration-300 transform" leave-from="translate-x-0" leave-to="-translate-x-full">
                    <div class="relative flex-1 flex flex-col max-w-xs w-full pt-5 pb-4 bg-white">
                        <TransitionChild as="template" enter="ease-in-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-300" leave-from="opacity-100" leave-to="opacity-0">
                            <div class="absolute top-0 right-0 -mr-12 pt-2">
                                <button class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white" @click="open = false">
                                    <span class="sr-only">Close sidebar</span>
                                    <XIcon class="h-6 w-6 text-white" aria-hidden="true" />
                                </button>
                            </div>
                        </TransitionChild>
                        <div class="flex-shrink-0 flex items-center px-4">
                            <ShieldCheckIcon class="h-8 w-8 text-blue-500" aria-hidden="true"/>
                            <span class="text-gray-400 text-2xl hover:text-gray-800 focus:text-gray-800">MailGuardian</span>
                        </div>
                        <div class="mt-5 flex-1 h-0 overflow-y-auto">
                            <nav class="px-2 space-y-1">
                                <router-link v-for="item in navigation" :key="item.path" :to="item.path" exact-active-class="font-bold bg-blue-200 text-blue-500 hover:bg-blue-300" class="text-gray-700 hover:bg-gray-200 hover:text-gray-900 group flex items-center px-2 py-2 text-base font-medium rounded-md">
                                    <component :is="item.icon" class="mr-4 flex-shrink-0 h-6 w-6" aria-hidden="true" />
                                    {{ item.name }}
                                </router-link>
                            </nav>
                        </div>
                    </div>
                </TransitionChild>
                <div class="flex-shrink-0 w-14" aria-hidden="true">
                    <!-- Dummy element to force sidebar to shrink to fit close icon -->
                </div>
            </Dialog>
        </TransitionRoot>
        <!-- Static sidebar for desktop -->
        <div class="hidden md:flex md:flex-shrink-0">
            <div class="flex flex-col w-64">
                <!-- Sidebar component, swap this element with another sidebar if you like -->
                <div class="flex flex-col flex-grow border-r border-gray-200 pt-5 pb-4 bg-white overflow-y-auto">
                    <div class="flex items-center flex-shrink-0 px-4">
                        <ShieldCheckIcon class="h-8 w-8 text-blue-500" aria-hidden="true"/>
                        <span class="text-gray-400 text-2xl hover:text-gray-800 focus:text-gray-800">MailGuardian</span>
                    </div>
                    <div class="mt-5 flex-grow flex flex-col">
                        <nav class="flex-1 pr-2 bg-white space-y-1">
                            <router-link v-for="item in navigation" :key="item.path" :to="item.path" exact-active-class="font-bold bg-blue-200 text-blue-500 hover:bg-blue-300" class="transition duration-300 flex items-center rounded-r-full text-gray-700 p-1 pl-6 hover:bg-blue-gray-200">
                                <component :is="item.icon" class="mr-4 flex-shrink-0 h-6 w-6" aria-hidden="true" />
                                {{ item.name }}
                            </router-link>
                        </nav>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex flex-col w-0 flex-1 overflow-hidden">
            <div class="relative z-10 flex-shrink-0 flex h-16 bg-white shadow">
                <button class="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white md:hidden" @click="open = true">
                    <span class="sr-only">Open sidebar</span>
                    <MenuAlt2Icon class="h-6 w-6" aria-hidden="true" />
                </button>
                <div class="flex-1 px-4 flex justify-between">
                    <div class="flex-1 flex">
                        <!-- PUT SEARCH FIELD HERE -->

                    </div>
                    <div class="ml-4 flex items-center md:ml-6">
                        <button class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white">
                            <span class="sr-only">View notifications</span>
                            <BellIcon class="h-6 w-6" aria-hidden="true" />
                        </button>
                        <Menu as="div" class="ml-3 relative">
                            <div>
                                <MenuButton class="transition duration-300 max-w-xs bg-white text-gray-400 hover:text-gray-800 flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white">
                                    <span class="sr-only">Open user menu</span>
                                    <UserCircleIcon class="h-8 w-8" aria-hidden="true" />
                                </MenuButton>
                            </div>
                            <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                                <MenuItems class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                                    <MenuItem v-for="item in profile" :key="item" v-slot="{ active }">
                                        <router-link :to="item.path" :class="[active ? 'bg-gray-100' : '', 'transition duration-300 block px-4 py-2 text-base md:text-sm text-gray-700']">{{ item.name }}</router-link>
                                    </MenuItem>
                                    <MenuItem v-for="item in profile" :key="item" v-slot="{ active }">
                                        <a href="#" @click="signOut" :class="[active ? 'bg-gray-100' : '', 'transition duration-300 block px-4 py-2 text-base md:text-sm text-gray-700']">Sign out</a>
                                    </MenuItem>
                                </MenuItems>
                            </transition>
                        </Menu>
                    </div>
                </div>
            </div>
            <main class="flex-1 relative overflow-y-auto focus:outline-none">
                <div class="py-6">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
                        <slot></slot>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'
import {
  Dialog,
  DialogOverlay,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import { MailIcon, LockClosedIcon, ChartBarIcon, UserGroupIcon, GlobeIcon, ServerIcon, DocumentSearchIcon, ShieldCheckIcon, XIcon, BellIcon, MenuAlt2Icon } from '@heroicons/vue/outline'
import { UserCircleIcon } from '@heroicons/vue/solid'
import navigation from '../data/menu'
import profile from '../data/profile'
export default {
    components: {
        Dialog,
        DialogOverlay,
        Menu,
        MenuButton,
        MenuItem,
        MenuItems,
        TransitionRoot,
        TransitionChild,
        MailIcon,
        LockClosedIcon,
        ChartBarIcon,
        UserGroupIcon,
        GlobeIcon,
        ServerIcon,
        DocumentSearchIcon,
        ShieldCheckIcon,
        XIcon,
        BellIcon,
        UserCircleIcon,
        MenuAlt2Icon
    },
    setup(props) {
        let open = ref(false)
        return {
            navigation,
            profile,
            open
        }
    }
}
</script>