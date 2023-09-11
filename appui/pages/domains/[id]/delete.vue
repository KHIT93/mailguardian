<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <NuxtLink to="/domains" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></NuxtLink>
        </div>
        <div class="shadow overflow-hidden sm:rounded-md">
            <UCard>
                <template #header>
                    <h1 class="text-xl">Delete domain ({{ id }})?</h1>
                </template>
                <p>
                    Are you absoutely certain that you wish to delete this domain?<br/>
                    This action cannot be undone!
                </p>
                <template #footer>
                    <form @submit.prevent="submit">
                        <div class="flex justify-end">
                            <button type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                No
                            </button>
                            <button type="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-500 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                                Yes
                            </button>
                        </div>
                    </form>
                </template>
            </UCard>
        </div>
    </MainLayout>
</template>

<script setup>
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import MainLayout from '~/components/MainLayout.vue'
import { useRoute } from 'vue-router'
import Form from '~/classes/Form'

useHead({
    title: 'MailGuardian - Delete Domain'
})

let { id } = useRoute().params
let form = reactive(new Form({
    id: id
}))

async function submit() {
    await form.delete(`/api/domains/${id}/`)
    navigateTo('/domains')
}
</script>