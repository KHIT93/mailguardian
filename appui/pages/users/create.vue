<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <router-link to="/users" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></router-link>
        </div>
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white space-y-8 sm:p-6">
                <UserForm :id="false"/>
            </div>
        </div>
    </MainLayout>
</template>

<script>
import { ArrowLeftIcon } from '@heroicons/vue/outline/esm/index.js'
import MainLayout from '~/components/MainLayout.vue'
import UserForm from '~/components/UserForm.vue'
export default {
    components: {
        ArrowLeftIcon,
        MainLayout,
        UserForm
    },
}
</script>