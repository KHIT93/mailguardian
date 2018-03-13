<template>
<div>
    <div class="bg-blue-lightest sm:hidden shadow">
        <div class="container mx-auto px-4">
            <div class="flex items-center sm:justify-between py-4">
                <div class="w-1/4">
                    <div href="#" @click="hide = !hide">
                        <svg class="fill-current h-8 w-8 text-grey text-5xl" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0 0h24v24H0z" fill="none"/>
                            <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
                        </svg>
                    </div>
                </div>
                <div class="w-1/2 sm:w-auto text-center text-grey text-2xl font-medium">
                    Administration
                </div>
            </div>
        </div>
    </div>
    <div class="bg-blue-lightest sm:block sm:border-b shadow lg:h-screen" :class="{'hidden' : hide}">
        <div class="container mx-auto px-4">
            <div class="sm:flex lg:block">
                <div class="flex -mb-px mr-6">
                    <router-link to="/admin/users" active-class="no-underline opacity-100 text-black sm:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-black opacity-50 sm:opacity-100 sm:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75">
                        <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0 0h24v24H0z" fill="none"/>
                            <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
                        </svg>
                        User Management
                    </router-link>
                </div>
                <div class="flex -mb-px mr-6">
                    <router-link to="/admin/domains" active-class="no-underline opacity-100 text-black sm:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-black opacity-50 sm:opacity-100 sm:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75">
                        <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0 0h24v24H0z" fill="none"/>
                            <path d="M20 13H4c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h16c.55 0 1-.45 1-1v-6c0-.55-.45-1-1-1zM7 19c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zM20 3H4c-.55 0-1 .45-1 1v6c0 .55.45 1 1 1h16c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1zM7 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/>
                        </svg>
                        Domain Management
                    </router-link>
                </div>
                <div class="flex -mb-px mr-6">
                    <router-link to="/admin/mailscanner/configuration" active-class="no-underline opacity-100 text-black sm:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-black opacity-50 sm:opacity-100 sm:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75">
                        <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                            <path d="M0 0h24v24H0z" fill="none"/>
                        </svg>
                        MailScanner Configuration
                    </router-link>
                </div>
                <div class="flex -mb-px">
                    <router-link to="/admin/mailscanner/rules" active-class="no-underline opacity-100 text-black sm:text-blue-dark flex items-center py-4 border-b border-blue-dark" class="no-underline text-black opacity-50 sm:opacity-100 sm:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75">
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
            </div>
        </div>
    </div>
</div>
</template>
<script>
export default {
    data: () => {
        return {
            hide: true,
        }
    },
}
</script>