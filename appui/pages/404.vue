<template>
    <MainLayout v-if="$auth().isAuthenticated()">
        <div class="flex">
            <p class="border-r text-5xl text-blue-500 font-bold px-2 animate-wiggle">&lt;404&gt;</p>
            <div class="px-2">
                <h1 class="text-5xl font-bold">Page not found</h1>
                <p class="text-sm text-gray-400">It would appear is if you tried to go somewhere where there is nothing</p>
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
    import MainLayout from '../components/MainLayout.vue'
    const { $auth } = useNuxtApp()
</script>