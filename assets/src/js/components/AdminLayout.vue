<template>
    <div class="lg:flex">
        <div class="lg:w-1/4">
            <mw-admin-menu></mw-admin-menu>
        </div>
        <div class="lg:w-3/4">
            <div class="container mx-auto sm:px-2 pt-2 pb-8">
                <div class="bg-white border sm:rounded shadow p-2">
                    <slot></slot>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import AdminNavigation from './AdminNavigation.vue';
export default {
    components: {
        'mw-admin-menu': AdminNavigation
    },
}
</script>