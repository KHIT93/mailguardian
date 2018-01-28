<template>
    <mw-admin-layout>
        <h2 class="font-normal text-center mb-2">Administration dashboard</h2>
        <p>This is the administrative dashboard. From here you can manage the underlying components and configuration files for your system</p>
    </mw-admin-layout>
</template>
<script>
import { mapGetters } from 'vuex';
import AdminLayout from '../../components/AdminLayout.vue';
export default {
    data: () => {
        return {
            
        }
    },
    components: {
        'mw-admin-layout': AdminLayout
    },
    computed: {
        ...mapGetters(['user'])
    }
}
</script>