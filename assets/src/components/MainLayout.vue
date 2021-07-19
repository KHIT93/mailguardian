<template>
    <div class="text-sm">
        <TopNavbar />
        <main class="flex pt-px">
            <SideNavbar />
            <section class="w-full md:w-3/4 xl:w-4/5">
                <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                    <!-- Replace with your content -->
                    <div class="px-4 py-6 sm:px-0">
                        <slot></slot>
                    </div>
                    <!-- /End replace -->
                </div>
            </section>
        </main>
    </div>
</template>

<script>
import TopNavbar from '../components/TopNavbar.vue'
import SideNavbar from '../components/SideNavbar.vue'
export default {
    components: {
        TopNavbar,
        SideNavbar,
    }
}
</script>