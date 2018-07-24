<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <div v-if="user.is_staff">
                <h2 class="border-b p-1">Admin tools</h2>
                <ul class="border-b pt-2 pb-3">
                    <li><router-link to="/tools/mailqueue">View mail queue</router-link></li>
                    <li>Clear mail queue</li>
                    <li>View job queue</li>
                    <li>Clam AV Status</li>
                    <li>GeoIP update status</li>
                    <li><router-link to="/tools/sa-status">SpamAssassin rules status</router-link></li>
                    <li><router-link to="/tools/app-updates">Application update status</router-link></li>
                </ul>
            </div>
            <div>
                <h2 class="border-b p-1">Helpful links</h2>
                <ul>
                    <li><a href="http://mxtoolbox.com/NetworkTools.aspx" target="new">MXToolBox</a></li>
                    <li><a href="https://www.tcpiputils.com/" target="new">TCP IP Utilities</a></li>
                </ul>
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
export default {
    data: () => {
        return {

        }
    },
    computed: {
        ...mapGetters(['isLoggedIn', 'user', 'loading'])
    }
}
</script>