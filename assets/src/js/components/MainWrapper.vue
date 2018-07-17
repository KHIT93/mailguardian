<template>
    <!-- Navigation -->
    <div>
        <div class="fixed z-10 w-full" v-if="isLoggedIn">
            <!-- Top nav -->
            <div class="bg-grey-darkest" :class="{ 'shadow-md' : hide, 'lg:shadow-md':!hide }">
                <div class="mx-auto px-4">
                    <div class="flex items-center lg:justify-between py-2 md:py-0">
                        <div class="w-1/4 lg:hidden">
                            <div href="#" @click="hide = !hide">
                                <mg-menu-icon class="w-8 h-8 text-white text-5xl"></mg-menu-icon>
                            </div>
                        </div>
                        <div class="w-1/2 lg:w-auto text-center text-white text-xl font-medium">
                            {{appName}}
                        </div>
                        <div class="hidden md:block md:w-2/3">
                            <input type="text" name="search" placeholder="Search..." class="bg-grey-lighter shadow-inner appearance-none opacity-25 focus:opacity-100 w-full p-3 text-grey-dark"/>
                        </div>
                        <div class="w-1/5 sm:w-auto sm:flex text-right h-full text-grey" title="Log out">
                            <router-link to="/profile" class="text-grey hover:text-white pr-2">
                                <mg-account-circle-icon class="w-6 h-6"></mg-account-circle-icon>
                            </router-link>
                            <div class="hover:text-white cursor-pointer" @click="logout">
                                <mg-exit-to-app-icon class="w-6 h-6"></mg-exit-to-app-icon>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="lg:flex">
            <!-- Secondary -->
            <div v-if="isLoggedIn" class="bg-grey-darkest lg:shadow-md lg:block lg:bg-white lg:border-b lg:w-1/5 xxl:w-1/6 pt-12 lg:pt-16 lg:h-screen" :class="{ 'hidden' : hide, 'shadow-md' : !hide }">
                <div class="container mx-auto px-4">
                    <div class="">
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-dashboard-icon class="w-6 h-6 mr-2"></mg-dashboard-icon>
                                Dashboard
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/messages" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-email-icon class="w-6 h-6 mr-2"></mg-email-icon>
                                Messages
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/lists" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-exposure-icon class="w-6 h-6 mr-2"></mg-exposure-icon>
                                Lists
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/reports" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-insert-chart-icon class="w-6 h-6 mr-2"></mg-insert-chart-icon>
                                Reports
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/tools" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-build-icon class="w-6 h-6 mr-2"></mg-build-icon>
                                Tools
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/users" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-people-icon class="w-6 h-6 mr-2"></mg-people-icon>
                                Users
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/domains" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-dns-icon class="w-6 h-6 mr-2"></mg-dns-icon>
                                Domains
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/hosts" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-device-hub-icon class="w-6 h-6 mr-2"></mg-device-hub-icon>
                                Hosts
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/smtp-relays" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-verified-user-icon class="w-6 h-6 mr-2"></mg-verified-user-icon>
                                SMTP Relays
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/mailscanner/configuration" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-email-icon class="w-6 h-6 mr-2"></mg-email-icon>
                                MailScanner Configuration
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/spamassassin/rules" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-import-contacts-icon class="w-6 h-6 mr-2"></mg-import-contacts-icon>
                                SpamAssassin Rules
                            </router-link>
                        </div>
                        <div class="flex -mb-px" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/settings" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mg-settings-icon class="w-6 h-6 mr-2"></mg-settings-icon>
                                Settings
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
            <div :class="{ 'pt-0 lg:pt-12' : !hide, 'pt-12': hide, 'w-full':!isLoggedIn, 'lg:w-4/5 xxl:w-5/6':isLoggedIn }">
                <transition name="fade">
                    <slot></slot>
                </transition>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    props: ['appName', 'appLogo'],
    data: () => {
        return {
            hide: true,
        }
    },
    computed: {
        computeClasses() {
            return (this.hide) ? "hidden" : "";
        },
        ...mapGetters(['isLoggedIn', 'user'])
    },
    methods: {
        logout() {
            axios.post('/rest-auth/logout/', {}).then(response => {
                window.location.href = '/';
            })
        },
        hideMenu() {
            if (!this.hide) {
                this.hide = true;
            }
        }
    }
}
</script>