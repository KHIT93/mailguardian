<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <router-link to="/lists" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></router-link>
        </div>
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white space-y-8 sm:p-6">
                <form method="POST">
                    <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                        {{ form.errors.get('non_field_errors') }}
                    </p>
                    <div class="relative" v-if="entry.from_entry_type == 'email'">
                        <input id="from_address" v-model="form.from_address.value" name="from_address" type="email" autocomplete="email" required="" :class="{ 'border-red-600': form.errors.has('from_address') }" class="peer placeholder-transparent transition duration-300 appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Senders email" />
                        <label for="from_address" class="absolute flex bg-white px-1 left-0 -top-6 text-gray-600 text-sm transition-all duration-200 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-2 peer-placeholder-shown:left-3 peer-focus:-top-6 peer-focus:left-0 peer-focus:text-blue-500 peer-focus:text-sm peer-focus:bg-white peer-focus:px-1 peer-focus:flex peer-focus:z-50">Senders email</label>
                        <p v-if="form.errors.has('from_address')" class="text-red-500 text-xs py-1">
                            {{ form.errors.get('from_address') }}
                        </p>
                    </div>
                    <div class="relative" v-if="entry.from_entry_type == 'domain' || entry.from_entry_type == 'ip_address'">
                        <input id="from_domain" v-model="form.from_domain.value" name="from_domain" type="text" required="" :class="{ 'border-red-600': form.errors.has('from_domain') }" class="peer placeholder-transparent transition duration-300 appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Senders domain" />
                        <label for="from_domain" class="absolute flex bg-white px-1 left-0 -top-6 text-gray-600 text-sm transition-all duration-200 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-2 peer-placeholder-shown:left-3 peer-focus:-top-6 peer-focus:left-0 peer-focus:text-blue-500 peer-focus:text-sm peer-focus:bg-white peer-focus:px-1 peer-focus:flex peer-focus:z-50">Senders domain</label>
                        <p v-if="form.errors.has('from_domain')" class="text-red-500 text-xs py-1">
                            {{ form.errors.get('from_domain') }}
                        </p>
                    </div>
                    <hr class="my-4"/>
                    <div class="relative" v-if="entry.to_entry_type == 'email'">
                        <input id="to_address" v-model="form.to_address.value" name="to_address" type="email" autocomplete="email" required="" :class="{ 'border-red-600': form.errors.has('to_address') }" class="peer placeholder-transparent transition duration-300 appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Recipient email" />
                        <label for="to_address" class="absolute flex bg-white px-1 left-0 -top-6 text-gray-600 text-sm transition-all duration-200 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-2 peer-placeholder-shown:left-3 peer-focus:-top-6 peer-focus:left-0 peer-focus:text-blue-500 peer-focus:text-sm peer-focus:bg-white peer-focus:px-1 peer-focus:flex peer-focus:z-50">Recipient email</label>
                        <p v-if="form.errors.has('to_address')" class="text-red-500 text-xs py-1">
                            {{ form.errors.get('to_address') }}
                        </p>
                    </div>
                    <div class="relative" v-if="entry.to_entry_type == 'domain' || entry.to_entry_type == 'ip_address'">
                        <input id="to_domain" v-model="form.to_domain.value" name="to_domain" type="text" required="" :class="{ 'border-red-600': form.errors.has('to_domain') }" class="peer placeholder-transparent transition duration-300 appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Recipient domain" />
                        <label for="to_domain" class="absolute flex bg-white px-1 left-0 -top-6 text-gray-600 text-sm transition-all duration-200 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-2 peer-placeholder-shown:left-3 peer-focus:-top-6 peer-focus:left-0 peer-focus:text-blue-500 peer-focus:text-sm peer-focus:bg-white peer-focus:px-1 peer-focus:flex peer-focus:z-50">Recipient domain</label>
                        <p v-if="form.errors.has('to_domain')" class="text-red-500 text-xs py-1">
                            {{ form.errors.get('to_domain') }}
                        </p>
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
            entry.value = res
            form = new Form({
                from_address: entry.from_address,
                from_domain: entry.from_domain,
                to_address: entry.to_address,
                to_domain: entry.to_domain,
                listing_type: entry.listing_type,
            })
            loading.value = false
            return res
        })

        onMounted(() => {
            getEntry()
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