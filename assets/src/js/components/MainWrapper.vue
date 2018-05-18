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
                                <mw-menu-icon class="w-8 h-8 text-white text-5xl"></mw-menu-icon>
                            </div>
                        </div>
                        <div class="w-1/2 lg:w-auto text-center text-white text-xl font-medium">
                            MailWare
                        </div>
                        <div class="hidden md:block md:w-2/3">
                            <input type="text" name="search" placeholder="Search..." class="bg-grey-lighter shadow-inner appearance-none opacity-25 focus:opacity-100 w-full p-3 text-grey-dark"/>
                        </div>
                        <div class="w-1/5 sm:w-auto sm:flex text-right h-full hover:text-white text-grey" title="Log out">
                            <div @click="logout">
                                <mw-exit-to-app-icon class="w-6 h-6"></mw-exit-to-app-icon>
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
                                <mw-dashboard-icon class="w-6 h-6 mr-2"></mw-dashboard-icon>
                                Dashboard
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/messages" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mw-email-icon class="w-6 h-6 mr-2"></mw-email-icon>
                                Messages
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/lists" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mw-exposure-icon class="w-6 h-6 mr-2"></mw-exposure-icon>
                                Lists
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/reports" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mw-insert-chart-icon class="w-6 h-6 mr-2"></mw-insert-chart-icon>
                                Reports
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/tools" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mw-build-icon class="w-6 h-6 mr-2"></mw-build-icon>
                                Tools
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/users" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mw-people-icon class="w-6 h-6 mr-2"></mw-people-icon>
                                Users
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/domains" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mw-dns-icon class="w-6 h-6 mr-2"></mw-dns-icon>
                                Domains
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/mailscanner/configuration" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mw-email-icon class="w-6 h-6 mr-2"></mw-email-icon>
                                MailScanner Configuration
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/mailscanner/rules" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mw-import-contacts-icon class="w-6 h-6 mr-2"></mw-import-contacts-icon>
                                MailScanner Rules
                            </router-link>
                        </div>
                        <div class="flex -mb-px" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/settings" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <mw-settings-icon class="w-6 h-6 mr-2"></mw-settings-icon>
                                Settings
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
            <div :class="{ 'pt-0 lg:pt-12' : !hide, 'pt-12': hide, 'w-full':!isLoggedIn, 'lg:w-4/5 xxl:w-5/6':isLoggedIn }">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
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