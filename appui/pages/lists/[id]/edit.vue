<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <NuxtLink to="/lists" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></NuxtLink>
        </div>
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white space-y-8 sm:p-6">
                <form method="POST" class="space-y-8 sm:space-y-5 divide-y divide-gray-200">
                    <div class="">
                        <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                            {{ form.errors.get('non_field_errors') }}
                        </p>
                        <UFormGroup label="Senders email" size="md" class="my-4" v-if="entry.from_entry_type == 'email'">
                            <UInput id="from_address" type="text" v-model="form.from_address"/>
                            <p v-if="form.errors.has('from_address')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('from_address') }}
                            </p>
                        </UFormGroup>
                        <UFormGroup label="Senders domain" size="md" class="my-4" v-if="entry.from_entry_type == 'domain' || entry.from_entry_type == 'ip_address'">
                            <UInput id="from_domain" type="text" v-model="form.from_domain"/>
                            <p v-if="form.errors.has('from_domain')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('from_domain') }}
                            </p>
                        </UFormGroup>
                        <hr class="my-4"/>
                        <UFormGroup label="Recipient email" size="md" class="my-4" v-if="entry.to_entry_type == 'email'">
                            <UInput id="to_address" type="text" v-model="form.to_address"/>
                            <p v-if="form.errors.has('to_address')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('to_address') }}
                            </p>
                        </UFormGroup>
                        <UFormGroup label="Recipient domain" size="md" class="my-4" v-if="entry.to_entry_type == 'domain' || entry.to_entry_type == 'ip_address'">
                            <UInput id="to_domain" type="text" v-model="form.to_domain"/>
                            <p v-if="form.errors.has('to_domain')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('to_domain') }}
                            </p>
                        </UFormGroup>
                    </div>
                    <div class="pt-5">
                        <div class="flex justify-end">
                            <button type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                Cancel
                            </button>
                            <button type="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                Save
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import { onMounted, ref, reactive, computed, toRefs } from 'vue'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import { useRoute } from 'vue-router'
import MainLayout from '~/components/MainLayout.vue'
import Form from '~/classes/Form'

let { id } = useRoute().params
let entry = ref({})
let form = reactive(new Form({
    from_address: '',
    from_domain: '',
    to_address: '',
    to_domain: '',
    listing_type: '',
}))
let loading = ref(false)
async function getEntry() {
    loading.value = true
    let res = (await useBackendFetch(`/api/lists/${id}/`))
    form.from_address = res.from_address
    form.from_domain = res.from_domain
    form.to_address = res.to_address
    form.to_domain = res.to_domain
    form.listing_type = res.listing_type
    loading = false
    return res
}

onMounted(async () => {
    entry.value = (await getEntry())
})
</script>