<template>
    <!-- Navigation -->
    <div>
        <div>
            <!-- Top nav -->
            <div class="bg-blue-dark">
                <div class="container mx-auto px-4">
                    <div class="flex items-center sm:justify-between py-4">
                        <div class="w-1/4 sm:hidden">
                            <a href="#" @click="hide = !hide">
                                <svg class="fill-current h-8 w-8 text-white text-5xl" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
                                </svg>
                            </a>
                        </div>
                        <div class="w-1/2 sm:w-auto text-center text-white text-2xl font-medium">
                            MailWare
                        </div>
                        <div class="w-1/4 sm:w-auto sm:flex text-right">
                            <div>
                                <img class="h-8 w-8 inline-block rounded-full" src="https://avatars0.githubusercontent.com/u/8628945?s=460&v=4"/>
                            </div>
                            <div class="hidden sm:block sm:flex sm:items-center ml-2">
                                <span class="text-white text-sm mr-1">Kenneth Hansen</span>
                                <div>
                                    <svg class="fill-current text-white h-4 w-4 block opacity-50" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/>
                                        <path d="M0 0h24v24H0z" fill="none"/>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Secondary -->
        <div class="bg-blue-dark sm:block sm:bg-white sm:border-b" :class="computeClasses">
            <div class="container mx-auto px-4">
                <div class="sm:flex">
                    <div class="flex -mb-px mr-6">
                        <a href="#" class="no-underline text-white sm:text-blue-dark flex items-center py-4 border-b border-blue-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M0 0h24v24H0z" fill="none"/>
                                <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                            </svg>
                            Dashboard
                        </a>
                    </div>
                    <div class="flex -mb-px mr-6">
                        <a href="#" class="no-underline text-white opacity-50 sm:opacity-100 sm:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 sm:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                                <path d="M0 0h24v24H0z" fill="none"/>
                            </svg>
                            Messages
                        </a>
                    </div>
                    <div class="flex -mb-px mr-6">
                        <a href="#" class="no-underline text-white opacity-50 sm:opacity-100 sm:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 sm:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                                <path d="M0 0h24v24H0z" fill="none"/>
                            </svg>
                        Reports
                        </a>
                    </div>
                    <div class="flex -mb-px mr-6">
                        <a href="#" class="no-underline text-white opacity-50 sm:opacity-100 sm:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 sm:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path clip-rule="evenodd" d="M0 0h24v24H0z" fill="none"/>
                                <path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>
                            </svg>
                            Tools
                        </a>
                    </div>
                    <div class="flex -mb-px">
                        <a href="#" class="no-underline text-white opacity-50 sm:opacity-100 sm:text-grey-dark flex items-center py-4 border-b border-transparent hover:opacity-75 sm:hover:border-grey-dark">
                            <svg class="h-6 w-6 fill-current mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M0 0h24v24H0z" fill="none"/>
                                <path d="M19.43 12.98c.04-.32.07-.64.07-.98s-.03-.66-.07-.98l2.11-1.65c.19-.15.24-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1c-.52-.4-1.08-.73-1.69-.98l-.38-2.65C14.46 2.18 14.25 2 14 2h-4c-.25 0-.46.18-.49.42l-.38 2.65c-.61.25-1.17.59-1.69.98l-2.49-1c-.23-.09-.49 0-.61.22l-2 3.46c-.13.22-.07.49.12.64l2.11 1.65c-.04.32-.07.65-.07.98s.03.66.07.98l-2.11 1.65c-.19.15-.24.42-.12.64l2 3.46c.12.22.39.3.61.22l2.49-1c.52.4 1.08.73 1.69.98l.38 2.65c.03.24.24.42.49.42h4c.25 0 .46-.18.49-.42l.38-2.65c.61-.25 1.17-.59 1.69-.98l2.49 1c.23.09.49 0 .61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.65zM12 15.5c-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"/>
                            </svg>
                            Settings
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<<script>
export default {
    
    data: () => {
        return {
            hide: true,
        }
    },
    computed: {
        computeClasses() {
            return (this.hide) ? "hidden" : "";
        }
    }
}
</script>
