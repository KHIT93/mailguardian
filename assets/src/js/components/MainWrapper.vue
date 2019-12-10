<template>
    <!-- Navigation -->
    <div>
        <div class="fixed z-10 w-full" v-if="isLoggedIn">
            <!-- Top nav -->
            <div class="bg-gray-800" :class="{ 'shadow-md' : hide, 'lg:shadow-md':!hide }">
                <div class="mx-auto px-4">
                    <div class="flex items-center lg:justify-between py-3">
                        <div class="w-1/4 lg:hidden">
                            <div href="#" @click="hide = !hide">
                                <mg-menu-icon class="w-8 h-8 text-white text-5xl"></mg-menu-icon>
                            </div>
                        </div>
                        <div class="w-1/2 lg:w-auto text-center text-white text-xl font-medium">
                            <img v-if="appLogo" :src="appLogo" class="max-h-full"/>
                            <template v-else>{{appName}}</template>
                        </div>
                        <div class="hidden md:block md:w-2/3">
                            <!-- <input type="text" name="search" placeholder="Search..." class="bg-gray-200 shadow-inner appearance-none opacity-25 focus:opacity-100 w-full p-3 text-gray-600"/> -->
                        </div>
                        <div class="w-1/4 sm:w-auto flex justify-end text-right h-full text-gray-500" title="Log out">
                            <a :href="config.app_support" class="text-gray-500 hover:text-white pr-3" target="_blank">
                                <mg-help-icon class="w-6 h-6"></mg-help-icon>
                            </a>
                            <a :href="config.app_feedback" class="text-gray-500 hover:text-white pr-3" target="_blank">
                                <mg-feedback-icon class="w-6 h-6"></mg-feedback-icon>
                            </a>
                            <router-link to="/profile" class="text-gray-500 hover:text-white pr-3">
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
            <div v-if="isLoggedIn" class="bg-gray-800 lg:block lg:bg-transparent lg:border-b lg:w-1/5 xxl:w-1/6 pt-12 lg:pt-16 lg:h-screen" :class="{ 'hidden' : hide, 'shadow-md' : !hide }">
                <div class="container mx-auto px-4">
                    <div class="">
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/" exact active-class="active" class="nav-link">
                                <mg-dashboard-icon class="w-6 h-6 mr-2"></mg-dashboard-icon>
                                Dashboard
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/messages" active-class="active" class="nav-link">
                                <mg-email-icon class="w-6 h-6 mr-2"></mg-email-icon>
                                Messages
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/lists" exact active-class="active" class="nav-link">
                                <mg-exposure-icon class="w-6 h-6 mr-2"></mg-exposure-icon>
                                Lists
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/reports" active-class="active" class="nav-link">
                                <mg-insert-chart-icon class="w-6 h-6 mr-2"></mg-insert-chart-icon>
                                Reports
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/tools" active-class="active" class="nav-link">
                                <mg-build-icon class="w-6 h-6 mr-2"></mg-build-icon>
                                Tools
                            </router-link>
                        </div>
                        <hr class="border-b" v-if="user.is_staff">
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/users" active-class="active" class="nav-link">
                                <mg-people-icon class="w-6 h-6 mr-2"></mg-people-icon>
                                Users
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/domains" active-class="active" class="nav-link">
                                <mg-dns-icon class="w-6 h-6 mr-2"></mg-dns-icon>
                                Domains
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/hosts" active-class="active" class="nav-link">
                                <mg-device-hub-icon class="w-6 h-6 mr-2"></mg-device-hub-icon>
                                Hosts
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/smtp-relays" active-class="active" class="nav-link">
                                <mg-verified-user-icon class="w-6 h-6 mr-2"></mg-verified-user-icon>
                                SMTP Relays
                            </router-link>
                        </div>
                        <!-- <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/mailscanner/configuration" active-class="active" class="nav-link">
                                <mg-email-icon class="w-6 h-6 mr-2"></mg-email-icon>
                                MailScanner Configuration
                            </router-link>
                        </div> -->
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/spamassassin/rules" active-class="active" class="nav-link">
                                <mg-import-contacts-icon class="w-6 h-6 mr-2"></mg-import-contacts-icon>
                                SpamAssassin Rules
                            </router-link>
                        </div>
                        <div class="flex -mb-px" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/settings" active-class="active" class="nav-link">
                                <mg-settings-icon class="w-6 h-6 mr-2"></mg-settings-icon>
                                Settings
                            </router-link>
                        </div>
                        <hr class="border-b" v-if="user.is_staff">
                        <div class="flex -mb-px" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/notifications" active-class="active" class="nav-link">
                                <mg-notification-icon class="w-6 h-6 mr-2"></mg-notification-icon>
                                Notification Manager
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
        config() {
            return window.mailguardian;
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