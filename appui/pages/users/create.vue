<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <NuxtLink to="/users" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></NuxtLink>
        </div>
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white space-y-8 sm:p-6">
                <UserForm :id="false"/>
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import MainLayout from '~/components/MainLayout.vue'
import UserForm from '~/components/UserForm.vue'
</script>