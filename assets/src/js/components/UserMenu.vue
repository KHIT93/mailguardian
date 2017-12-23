<template>
    <div>
        <div class="w-1/4 sm:w-auto sm:flex text-right mb-px" @click="hide = !hide">
            <div>
                <!-- <img class="h-8 w-8 inline-block rounded-full" src="https://avatars0.githubusercontent.com/u/8628945?s=460&v=4"/>-->
                <svg class="fill-current h-8 w-8 text-white text-5xl" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                    <path d="M0 0h24v24H0z" fill="none"/>
                </svg>
            </div>
            <div class="hidden sm:block sm:flex sm:items-center ml-2">
                <span class="text-white text-sm mr-1">{{user.full_name != " " ? user.full_name : user.username}}</span>
                <div>
                    <svg class="fill-current text-white h-4 w-4 block opacity-50" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" v-show="hide">
                        <path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/>
                        <path d="M0 0h24v24H0z" fill="none"/>
                    </svg>
                    <svg class="fill-current text-white h-4 w-4 block opacity-50" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" v-show="!hide">
                        <path d="M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z"/>
                        <path d="M0 0h24v24H0z" fill="none"/>
                    </svg>
                </div>
            </div>
        </div>
        <div class="bg-grey-lightest sm:rounded-lg sm:shadow-md w-full sm:w-64 sm:z-50 absolute pin-r" :class="{'hidden' : hide}">
            <div class="px-4 py-3 sm:rounded-t-lg hover:bg-grey-light">
                <h4>My profile</h4>
            </div>
            <div class="px-4 py-3 border-t hover:bg-grey-light">
                <h4>Settings</h4>
            </div>
            <div class="px-4 py-3 border-t hover:bg-grey-light">
                <h4>Go to admin</h4>
            </div>
            <div class="px-4 py-3 border-t sm:rounded-b-lg hover:bg-grey-light">
                <h4>Log out</h4>
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
import { directive as onClickaway } from 'vue-clickaway';
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
        ...mapGetters(['user']),
    },
    directives: {
        onClickaway: onClickaway
    }
}
</script>
