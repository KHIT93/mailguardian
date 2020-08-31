<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <div v-if="user.is_staff">
                <h2 class="p-1 pb-0 font-thin text-lg text-gray-800">Data import</h2>
                <p class="p-1 text-xs text-gray-800">Import data into various parts of the system. Each option shows you how the import file should be structured</p>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/data-import/lists">
                    List Entries<br/>
                    <span class=" text-xs text-gray-600">Import data entries into the block list and allow list</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/data-import/domains">
                    Domains<br/>
                    <span class=" text-xs text-gray-600">Import domains, for which email should be handled</span>
                </router-link>
                <router-link class="block border-t px-4 py-2 hover:bg-gray-200 no-underline text-gray-800" to="/tools/data-import/relays">
                    SMTP relays<br/>
                    <span class=" text-xs text-gray-600">Import information about which servers should be allowed to relay email through the application</span>
                </router-link>
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