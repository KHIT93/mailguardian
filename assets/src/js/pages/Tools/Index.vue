<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <div v-if="user.is_staff">
                <h2 class="p-1 font-hairline text-grey-darkest">Admin tools</h2>
                <router-link class="block border-t px-4 py-2 hover:bg-grey-lighter no-underline text-grey-darkest" to="/tools/mailqueue">
                    View mail queue<br/>
                    <span class=" text-xs text-grey-dark">View the current messages in the mailqueue</span>
                </router-link>
                <!-- <router-link class="block border-t px-4 py-2 hover:bg-grey-lighter no-underline text-grey-darkest" to="/tools/mailqueue">
                    Clear mail queue<br/>
                    <span class=" text-xs text-grey-dark">Remove all messages from the mailqueue</span>
                </router-link> -->
                <router-link class="block border-t px-4 py-2 hover:bg-grey-lighter no-underline text-grey-darkest" to="/tools/tasks">
                    View task queue<br/>
                    <span class=" text-xs text-grey-dark">View the current queue of application tasks</span>
                </router-link>
                <!-- <router-link class="block border-t px-4 py-2 hover:bg-grey-lighter no-underline text-grey-darkest" to="/tools/tasks">
                    ClamAV status<br/>
                    <span class=" text-xs text-grey-dark">View the status of the ClamAV virus scanner engine/span>
                </router-link> -->
                <!-- <router-link class="block border-t px-4 py-2 hover:bg-grey-lighter no-underline text-grey-darkest" to="/tools/tasks">
                    GeoIP update status<br/>
                    <span class=" text-xs text-grey-dark">View the current state of the GeoIP database used to find out from which countries, that the given IP-addresses are located in</span>
                </router-link> -->
                <router-link class="block border-t px-4 py-2 hover:bg-grey-lighter no-underline text-grey-darkest" to="/tools/sa-status">
                    SpamAssassin rules status<br/>
                    <span class=" text-xs text-grey-dark">See when the SpamAssassin rules were last updated or perform a manual update</span>
                </router-link>
                <router-link class="block border-t border-b px-4 py-2 hover:bg-grey-lighter no-underline text-grey-darkest" to="/tools/app-updates">
                    Application update status<br/>
                    <span class=" text-xs text-grey-dark">Check for updates for the application itself</span>
                </router-link>
            </div>
            <div>
                <h2 class="border-b p-1 pt-4 font-hairline text-grey-darkest">Helpful links</h2>
                <a class="block px-4 py-2 hover:bg-grey-lighter no-underline text-grey-darkest" href="http://mxtoolbox.com/NetworkTools.aspx">
                    MXToolBox<br/>
                    <span class=" text-xs text-grey-dark">A popular and powerful set of tools, which you can use to find and resolve issues around sending and receiving email</span>
                </a>
                <a class="block border-t border-b px-4 py-2 hover:bg-grey-lighter no-underline text-grey-darkest" href="https://www.tcpiputils.com/">
                    TCP IP Utilities<br/>
                    <span class=" text-xs text-grey-dark">A service that allows you find a lot of information about IP-addresses</span>
                </a>
            </div>
        </div>
    </div>
</mg-page>
</template>
<script>
import { mapGetters } from 'vuex';
export default {
    data: () => {
        return {

        }
    },
    mounted() {
        this.$store.commit('setLoading', false);
    },
    computed: {
        ...mapGetters(['isLoggedIn', 'user', 'loading', 'settings'])
    }
}
</script>