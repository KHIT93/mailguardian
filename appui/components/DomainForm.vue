<template>
    <form method="POST" class="space-y-8 sm:space-y-5 divide-y divide-gray-200" @submit.prevent="submit">
        <div class="">
            <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                {{ form.errors.get('non_field_errors') }}
            </p>
            <FormInput inputId="name" label="Domain" type="text" v-model="form.name" class="my-4"/>
            <p v-if="form.errors.has('name')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('name') }}
            </p>
            <FormInput inputId="destination" label="Destination" type="text" v-model="form.destination" class="my-4"/>
            <p v-if="form.errors.has('destination')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('destination') }}
            </p>
            <hr />
            <div class="md:flex space-x-2">
                <UFormGroup label="Relay type" size="md" class="w-full sm:w-1/2 my-4">
                    <USelectMenu class="w-full" size="md" placeholder="Select Relay type..." label="Relay type" name="relay_type" id="relay_type" value-attribute="value" v-model="form.relay_type" :options="relayTypes">
                        <template #label>{{ selectedRelayType.label }}</template>
                    </USelectMenu>
                    <p v-if="form.errors.has('relay_type')" class="text-red-500 text-xs py-1">
                        {{ form.errors.get('relay_type') }}
                    </p>
                </UFormGroup>
                <UFormGroup label="Delivery type" size="md" class="w-full sm:w-1/2 my-4">
                <USelectMenu class="w-full" size="md" placeholder="Select Delivery type..." label="Delivery type" name="receive_type" id="receive_type" value-attribute="value" v-model="form.receive_type" :options="receiveTypes">
                    <template #label>{{ selectedReceiveType.label }}</template>
                </USelectMenu>
                <p v-if="form.errors.has('receive_type')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('receive_type') }}
                </p>
                </UFormGroup>
            </div>
            <Disclosure v-slot="{ open }" v-if="nodes.length > 0">
                <DisclosureButton class="flex justify-between w-full px-4 py-2 text-sm font-medium text-left text-blue-900 bg-blue-100 hover:bg-blue-200 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
                    <span>DNS Configuration</span>
                    <ChevronDownIcon :class="open ? 'transform rotate-180' : ''" class="w-5 h-5 text-blue-500"/>
                </DisclosureButton>
                <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead>
                            <tr>
                                <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                    Name
                                </th>
                                <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                    Type
                                </th>
                                <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                    Priority
                                </th>
                                <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                    TTL
                                </th>
                                <th scope="col" class="px-6 pt-3 pb-1 text-left text-xs font-medium text-gray-400 tracking-wider">
                                    Value
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="host in nodes" :key="host.id">
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                    {{ form.name }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                    MX
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                    {{ (form.recieve_type == 'failover') ? host.priority: 10  }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                    300
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                    {{ host.hostname }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </DisclosurePanel>
            </Disclosure>
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
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import Form from '~/classes/Form'
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/24/solid'
import FormInput from './FormInput.vue'
import FormSelection from './FormSelection.vue'

const props = defineProps(['id'])

const toast = useToast()

const form = reactive(new Form({
    name: '',
    active: '',
    allowed_accounts: '',
    destination: '',
    receive_type: 'smtp',
    relay_type: 'failover'
}))
let nodes = ref([])

const relayTypes = [
    { value: "smtp", label: "Deliver to my email server (SMTP)" },
    { value: "smtps", label: "Deliver to my email server (SMTP with SSL/TLS)" }
]
const selectedRelayType = computed(() => relayTypes.find(relayType => relayType.value == form.relay_type) || {value: '', label: '-- Select --'})

const receiveTypes = [
    { value: "load_balanced", label: "Load balancing" },
    { value: "failover", label: "Failover" }
]

const selectedReceiveType = computed(() => receiveTypes.find(receiveType => receiveType.value == form.receive_type) || {value: '', label: '-- Select --'})

onMounted(async () => {
    if(props.id) {
        let res = (await useBackendFetch(`/api/domains/${props.id}/`))
        form.name = res.name,
        form.active = res.active,
        form.allowed_accounts = res.allowed_accounts,
        form.destination = res.destination,
        form.receive_type = res.receive_type,
        form.relay_type = res.relay_type
    }
    nodes.value = (await useBackendFetch('/api/hosts/')).results
})

async function submit() {
    try {
        if (props.id) {
            await form.put(`/api/domains/${props.id}/`)
        }
        else {
            await form.post('/api/domains/')
        }
        toast.add({
            'id': 'domains_form_submitted',
            'title': (props.id) ? `Domain ${res.name} updated` : `Domain ${res.name} created`,
            'description': 'The changes will be active within a few minutes',
            'icon': 'i-heroicons-check-circle',
            'timeout': 5000
        })
        navigateTo('/domains')
    }
    catch(error) {
        console.log(error)
    }
}
</script>