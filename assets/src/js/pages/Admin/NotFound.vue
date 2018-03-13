<template>
    <mw-admin-layout>
        <div class="text-center text-grey-darker py-6">
            <div>
                <div class="mb-2">
                    <span class="text-5xl">Page not found</span>
                </div>
                <div class="uppercase">
                    Whoops! The page you were looking for does not seem to exist.
                </div>
            </div>
        </div>
    </mw-admin-layout>
</template>

<script>
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
    },
    mounted() {
        console.log('Page not found.')
    }
}
</script>