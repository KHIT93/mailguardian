<template>
    <!-- Navigation -->
    <div>
        <div class="fixed z-10 w-full" v-if="isLoggedIn">
            <!-- Top nav -->
            <div class="bg-grey-darkest" :class="{ 'shadow-md' : hide, 'lg:shadow-md':!hide }">
                <div class="container mx-auto px-4">
                    <div class="flex items-center lg:justify-between py-2 md:py-0">
                        <div class="w-1/4 lg:hidden">
                            <div href="#" @click="hide = !hide">
                                <svg class="fill-current h-8 w-8 text-white text-5xl" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
                                </svg>
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
                                <svg class="fill-current h-6 w-6" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M10.09 15.59L11.5 17l5-5-5-5-1.41 1.41L12.67 11H3v2h9.67l-2.58 2.59zM19 3H5c-1.11 0-2 .9-2 2v4h2V5h14v14H5v-4H3v4c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="lg:flex">
            <!-- Secondary -->
            <div v-if="isLoggedIn" class="bg-grey-darkest lg:shadow-md lg:block lg:bg-white lg:border-b lg:w-1/5 pt-12 lg:pt-16 lg:h-screen" :class="{ 'hidden' : hide, 'shadow-md' : !hide }">
                <div class="container mx-auto px-4">
                    <div class="">
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                                </svg>
                                Dashboard
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/messages" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                </svg>
                                Messages
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/lists" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M15 17v2h2v-2h2v-2h-2v-2h-2v2h-2v2h2zm5-15H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM5 5h6v2H5V5zm15 15H4L20 4v16z"/>
                                </svg>
                                Lists
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/reports" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                </svg>
                                Reports
                            </router-link>
                        </div>
                        <div class="flex -mb-px" @click="hideMenu()">
                            <router-link to="/tools" exact active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path clip-rule="evenodd" d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>
                                </svg>
                                Tools
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/users" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
                                </svg>
                                Users
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/domains" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M20 13H4c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h16c.55 0 1-.45 1-1v-6c0-.55-.45-1-1-1zM7 19c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zM20 3H4c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h16c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1zM7 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/>
                                </svg>
                                Domains
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/mailscanner/configuration" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                </svg>
                                MailScanner Configuration
                            </router-link>
                        </div>
                        <div class="flex -mb-px mr-6" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/mailscanner/rules" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                                    <defs>
                                        <path d="M0 0h24v24H0V0z" id="a"/>
                                    </defs>
                                    <clipPath id="b">
                                        <use overflow="visible" xlink:href="#a"/>
                                    </clipPath>
                                    <path clip-path="url(#b)" d="M21 5c-1.11-.35-2.33-.5-3.5-.5-1.95 0-4.05.4-5.5 1.5-1.45-1.1-3.55-1.5-5.5-1.5S2.45 4.9 1 6v14.65c0 .25.25.5.5.5.1 0 .15-.05.25-.05C3.1 20.45 5.05 20 6.5 20c1.95 0 4.05.4 5.5 1.5 1.35-.85 3.8-1.5 5.5-1.5 1.65 0 3.35.3 4.75 1.05.1.05.15.05.25.05.25 0 .5-.25.5-.5V6c-.6-.45-1.25-.75-2-1zm0 13.5c-1.1-.35-2.3-.5-3.5-.5-1.7 0-4.15.65-5.5 1.5V8c1.35-.85 3.8-1.5 5.5-1.5 1.2 0 2.4.15 3.5.5v11.5z"/>
                                </svg>
                                MailScanner Rules
                            </router-link>
                        </div>
                        <div class="flex -mb-px" v-if="user.is_staff" @click="hideMenu()">
                            <router-link to="/admin/settings" active-class="no-underline opacity-100 text-white lg:text-blue-dark flex items-center py-4 lg:py-2" class="no-underline text-white opacity-50 lg:opacity-100 lg:text-grey-dark flex items-center py-4 lg:py-2 border-b border-transparent hover:opacity-75">
                                <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M19.43 12.98c.04-.32.07-.64.07-.98s-.03-.66-.07-.98l2.11-1.65c.19-.15.24-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1c-.52-.4-1.08-.73-1.69-.98l-.38-2.65C14.46 2.18 14.25 2 14 2h-4c-.25 0-.46.18-.49.42l-.38 2.65c-.61.25-1.17.59-1.69.98l-2.49-1c-.23-.09-.49 0-.61.22l-2 3.46c-.13.22-.07.49.12.64l2.11 1.65c-.04.32-.07.65-.07.98s.03.66.07.98l-2.11 1.65c-.19.15-.24.42-.12.64l2 3.46c.12.22.39.3.61.22l2.49-1c.52.4 1.08.73 1.69.98l.38 2.65c.03.24.24.42.49.42h4c.25 0 .46-.18.49-.42l.38-2.65c.61-.25 1.17-.59 1.69-.98l2.49 1c.23.09.49 0 .61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.65zM12 15.5c-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"/>
                                </svg>
                                Settings
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
            <div :class="{ 'pt-0 lg:pt-12' : !hide, 'pt-12': hide, 'w-full':!isLoggedIn, 'lg:w-4/5':isLoggedIn }">
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
            window.location.href = '/api-auth/logout?next=/';
        },
        hideMenu() {
            if (!this.hide) {
                this.hide = true;
            }
        }
    }
}
</script>