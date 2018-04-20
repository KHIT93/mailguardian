<template>
    <!-- Navigation -->
    <div class="fixed z-10 w-full" v-if="isLoggedIn">
        <div>
            <!-- Top nav -->
            <div class="bg-blue-dark">
                <div class="container mx-auto px-4">
                    <div class="flex items-center lg:justify-between py-4">
                        <div class="w-1/4 lg:hidden">
                            <div href="#" @click="hide = !hide">
                                <svg class="fill-current h-8 w-8 text-white text-5xl" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
                                </svg>
                            </div>
                        </div>
                        <div class="w-1/2 lg:w-auto text-center text-white text-2xl font-medium">
                            MailWare
                        </div>
                        <mailware-usernav />
                    </div>
                </div>
            </div>
        </div>
        <!-- Secondary -->
        <div class="bg-blue-dark lg:block lg:bg-white lg:border-b" :class="{'hidden' : hide}">
            <div class="container mx-auto px-4">
                <div class="lg:flex">
                    <div class="flex -mb-px mr-6">
                        <router-link to="/" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 lg:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M0 0h24v24H0z" fill="none"/>
                                <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                            </svg>
                            Dashboard
                        </router-link>
                    </div>
                    <div class="flex -mb-px mr-6">
                        <router-link to="/messages" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 lg:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                                <path d="M0 0h24v24H0z" fill="none"/>
                            </svg>
                            Messages
                        </router-link>
                    </div>
                    <div class="flex -mb-px mr-6">
                        <router-link to="/lists" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 lg:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M0 0h24v24H0z" fill="none"/>
                                <path d="M15 17v2h2v-2h2v-2h-2v-2h-2v2h-2v2h2zm5-15H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM5 5h6v2H5V5zm15 15H4L20 4v16z"/>
                            </svg>
                            Lists
                        </router-link>
                    </div>
                    <div class="flex -mb-px mr-6">
                        <router-link to="/reports" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 lg:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                                <path d="M0 0h24v24H0z" fill="none"/>
                            </svg>
                            Reports
                        </router-link>
                    </div>
                    <div class="flex -mb-px mr-6">
                        <router-link to="/tools" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 lg:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path clip-rule="evenodd" d="M0 0h24v24H0z" fill="none"/>
                                <path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>
                            </svg>
                            Tools
                        </router-link>
                    </div>
                    <div class="flex -mb-px" v-if="user.is_staff">
                        <router-link to="/admin" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 lg:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/>
                                <path d="M0 0h24v24H0z" fill="none"/>
                            </svg>
                            Administration
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import UserMenu from './UserMenu.vue';
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
    components: {
        'mailware-usernav': UserMenu
    }
}
</script>
