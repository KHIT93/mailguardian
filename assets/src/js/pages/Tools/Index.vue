<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <div v-if="user.is_staff">
                <h2 class="p-1 font-thin text-lg text-gray-800">Admin tools</h2>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/mailqueue">
                    View mail queue<br/>
                    <span class=" text-xs text-gray-600">View the current messages in the mailqueue</span>
                </router-link>
                <!-- <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/mailqueue">
                    Clear mail queue<br/>
                    <span class=" text-xs text-gray-600">Remove all messages from the mailqueue</span>
                </router-link> -->
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/tasks">
                    View task queue<br/>
                    <span class=" text-xs text-gray-600">View the current queue of application tasks</span>
                </router-link>
                <!-- <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/tasks">
                    ClamAV status<br/>
                    <span class=" text-xs text-gray-600">View the status of the ClamAV virus scanner engine/span>
                </router-link> -->
                <a href="#" class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" @click.prevent="geoip_update">
                    GeoIP update status<br/>
                    <span class=" text-xs text-gray-600">View the current state of the GeoIP database used to find out from which countries, that the given IP-addresses are located in</span>
                </a> 
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/sa-status">
                    SpamAssassin rules status<br/>
                    <span class=" text-xs text-gray-600">See when the SpamAssassin rules were last updated or perform a manual update</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/app-updates">
                    Application update status<br/>
                    <span class=" text-xs text-gray-600">Check for updates for the application itself</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/admin/audit-log">
                    Audit Log<br/>
                    <span class=" text-xs text-gray-600">Show the audit log</span>
                </router-link>
                <router-link class="block border-t border-b px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/data-import">
                    Data import<br/>
                    <span class=" text-xs text-gray-600">Perform import of data into various parts of the application</span>
                </router-link>
            </div>
            <div>
                <h2 class="border-b p-1 pt-4 font-thin text-lg text-gray-800">Helpful links</h2>
                <a class="block px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" href="http://mxtoolbox.com/NetworkTools.aspx">
                    MXToolBox<br/>
                    <span class=" text-xs text-gray-600">A popular and powerful set of tools, which you can use to find and resolve issues around sending and receiving email</span>
                </a>
                <a class="block border-t border-b px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" href="https://www.tcpiputils.com/">
                    TCP IP Utilities<br/>
                    <span class=" text-xs text-gray-600">A service that allows you find a lot of information about IP-addresses</span>
                </a>
            </div>
        </div>
    </div>
</mg-page>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex';
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
    },
    methods: {
        geoip_update() {
            axios.get('api/geoip/update/').then(response => {
                this.notify(this.createNotification('GeoIP Update completed', 'Update of MaxMind GeoLite2 database has been completed', 'success'));
            }).catch(error => {
                console.log(error);
                this.notify(this.createNotification('An error occurred while getting the message contents', `${error}`, 'error'));
            });
        },
        ...mapMutations(['notify'])
    }
}
</script>