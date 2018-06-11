<template>
    <div>
        <div class="lg:flex" v-if="user.is_staff">
            <div class="lg:w-1/4">
                <mg-admin-menu></mg-admin-menu>
            </div>
            <div class="lg:w-3/4">
                <div class="container mx-auto sm:px-2 pt-2 pb-8">
                    <div class="bg-white border sm:rounded shadow p-2">
                        <slot></slot>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>You are not authorized to view this page</div>
    </div>
</template>
<script>
import AdminNavigation from './AdminNavigation.vue';
import { mapGetters } from 'vuex';
export default {
    components: {
        'mg-admin-menu': AdminNavigation
    },
    computed: {
        ...mapGetters(['user'])
    }
}
</script>