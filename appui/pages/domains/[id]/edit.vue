<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <NuxtLink to="/domains" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></NuxtLink>
        </div>
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white space-y-8 sm:p-6">
                <DomainForm v-if="id" :id="id"/>
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import MainLayout from '~/components/MainLayout.vue'
import DomainForm from '~/components/DomainForm.vue'
import { useRoute } from 'vue-router'

useHead({
    title: 'MailGuardian - Edit Domain'
})

let { id } = useRoute().params
</script>