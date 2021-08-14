<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <router-link to="/lists" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></router-link>
        </div>
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white space-y-8 sm:p-6">
                <form method="POST" class="space-y-8 sm:space-y-5 divide-y divide-gray-200">
                    <div class="">
                        <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                            {{ form.errors.get('non_field_errors') }}
                        </p>
                        <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600" v-if="entry.from_entry_type == 'email'">
                            <label for="from_address" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Senders email</label>
                            <input type="text" name="from_address" id="from_address" v-model="form.from_address.value" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Senders email" />
                            <p v-if="form.errors.has('from_address')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('from_address') }}
                            </p>
                        </div>
                        <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600" v-if="entry.from_entry_type == 'domain' || entry.from_entry_type == 'ip_address'">
                            <label for="from_domain" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Senders email</label>
                            <input type="text" name="from_domain" id="from_domain" v-model="form.from_domain.value" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Senders email" />
                            <p v-if="form.errors.has('from_domain')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('from_domain') }}
                            </p>
                        </div>
                        <hr class="my-4"/>
                        <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600" v-if="entry.to_entry_type == 'email'">
                            <label for="to_address" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Senders email</label>
                            <input type="text" name="to_address" id="to_address" v-model="form.to_address.value" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Senders email" />
                            <p v-if="form.errors.has('to_address')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('to_address') }}
                            </p>
                        </div>
                        <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600" v-if="entry.to_entry_type == 'domain' || entry.to_entry_type == 'ip_address'">
                            <label for="to_domain" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Senders email</label>
                            <input type="text" name="to_domain" id="to_domain" v-model="form.to_domain.value" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Senders email" />
                            <p v-if="form.errors.has('to_domain')" class="text-red-500 text-xs py-1">
                                {{ form.errors.get('to_domain') }}
                            </p>
                        </div>
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

<script>
import { onMounted, ref, computed, toRefs } from 'vue'
import { ArrowLeftIcon } from '@heroicons/vue/outline'
import { RouterLink, useLink, useRouter, useRoute } from 'vue-router'
import MainLayout from '../../../components/MainLayout.vue'
import Form from '../../../classes/Form'
export default {
    components: {
        ArrowLeftIcon,
        MainLayout
    },
    setup(props) {
        let { id } = useRoute().params
        let entry = ref({})
        let form = new Form({
            from_address: ref(''),
            from_domain: ref(''),
            to_address: ref(''),
            to_domain: ref(''),
            listing_type: ref(''),
        })
        let loading = ref(false)
        let getEntry = (async () => {
            loading.value = true
            let res = (await axios.get(`/api/lists/${id}/`)).data
            form.from_address.value = res.from_address
            form.from_domain.value = res.from_domain
            form.to_address.value = res.to_address
            form.to_domain.value = res.to_domain
            form.listing_type.value = res.listing_type
            loading.value = false
            return res
        })

        onMounted(async () => {
            entry.value = (await getEntry())
        })

        return {
            id,
            entry,
            form,
            loading,
            getEntry
        }
    }
}
</script>