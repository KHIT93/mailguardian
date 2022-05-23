<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <router-link to="/domains" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></router-link>
        </div>
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white space-y-8 sm:p-6">
                <DomainForm v-if="id" :id="id"/>
            </div>
        </div>
    </MainLayout>
</template>

<script>
import { ArrowLeftIcon } from '@heroicons/vue/outline/esm/index.js'
import MainLayout from '~/components/MainLayout.vue'
import DomainForm from '~/components/DomainForm.vue'
import { useRoute } from 'vue-router'

export default {
    components: {
        MainLayout,
        DomainForm,
        ArrowLeftIcon
    },
    setup(props) {
        let { id } = useRoute().params

        return {
            id
        }
    }
}
</script>