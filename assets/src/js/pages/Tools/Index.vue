<template>
    <div>
        <div v-if="user.is_staff">
            <h2>Admin tools</h2>
            <ul>
                <li>View mail queue</li>
                <li>Clear mail queue</li>
                <li>View job queue</li>
                <li>Clam AV Status</li>
                <li>GeoIP update status</li>
                <li>SpamAssassin rules status</li>
            </ul>
        </div>
        <div>
            <h2>Helpful links</h2>
            <ul>
                <li><a href="http://mxtoolbox.com/NetworkTools.aspx" target="new">MXToolBox</a></li>
                <li><a href="https://www.tcpiputils.com/" target="new">TCP IP Utilities</a></li>
            </ul>
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