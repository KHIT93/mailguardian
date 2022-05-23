<template>
    <MainLayout>
        <div class="flex w-full pb-4">
            <router-link to="/audit/log" class="rounded-full hover:bg-gray-200 p-4 cursor-pointer transition duration-200"><ArrowLeftIcon class="w-4 h-4"/></router-link>
        </div>
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:px-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                    {{ entry.timestamp }}
                </h3>
            </div>
            <div class="border-t border-gray-200 bg-gray-50">
                <dl>
                    <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">
                            IP Address
                        </dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            {{ entry.remote_addr }}
                        </dd>
                    </div>
                    <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">
                            Record Type
                        </dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            {{ entry.content_type_name }}
                        </dd>
                    </div>
                    <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">
                            Record
                        </dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            {{ entry.object_pk }}
                        </dd>
                    </div>
                    <div class="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">
                            By
                        </dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            {{ entry.actor_email }}
                        </dd>
                    </div>
                </dl>
                <div class="px-4 py-5 sm:gap-4 sm:px-6">
                    <p class="text-sm font-medium text-gray-500">Contents</p>
                    <code>
                        {{ changes }}
                    </code>
                </div>
            </div>
        </div>
    </MainLayout>
</template>

<script>
import MainLayout from '~/components/MainLayout.vue'
import { useRoute } from 'vue-router'
import { ref } from '@vue/reactivity'
import { onMounted } from '@vue/runtime-core'
import { ArrowLeftIcon } from '@heroicons/vue/outline/esm/index.js'

export default {
    components: {
        MainLayout,
        ArrowLeftIcon
    },
    setup(props) {
        let { id } = useRoute().params

        let entry = ref({})
        let changes = ref([])
 
        const parse_changes = (changes) => {
            let data = {}
            try {
                data = JSON.parse(changes)
            }
            catch {
                return changes
            }
            
            if (typeof data == 'string' || data instanceof String) {
                return data
            }
            let response = []
            for (let [key, value] of Object.entries(data)) {
                response.push({
                    key: key,
                    from: value[0],
                    to: value[1],
                    change: `${value[0]} -> ${value[1]}`
                })
            }

            console.log(response)

            return response
            
        }

        onMounted(async () => {
            entry.value = (await axios.get(`/api/datalog/${id}/`)).data
            changes.value = (await parse_changes(entry.value.changes))
            // entry.value.changes = JSON.parse(entry.value.changes)
        })

        return {
            id,
            entry,
            parse_changes,
            changes
        }
    }
}
</script>