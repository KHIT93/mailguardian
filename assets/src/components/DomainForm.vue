<template>
    <form method="POST" class="space-y-8 sm:space-y-5 divide-y divide-gray-200" @submit.prevent="submit">
        <div class="">
            <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                {{ form.errors.get('non_field_errors') }}
            </p>
            <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 my-4 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                <label for="name" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Domain</label>
                <input type="text" name="name" id="name" v-model="form.name" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Domain" />
                <p v-if="form.errors.has('name')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('name') }}
                </p>
            </div>
            <div class="relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 my-4 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                <label for="destination" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Destination</label>
                <input type="text" name="destination" id="destination" v-model="form.destination" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Destination" />
                <p v-if="form.errors.has('destination')" class="text-red-500 text-xs py-1">
                    {{ form.errors.get('destination') }}
                </p>
            </div>
            <hr />
            <div class="md:flex space-x-2">
                <div class="w-1/2 relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 my-4 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                    <label for="relay_type" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Relay type</label>
                    <select v-model="form.relay_type" id="relay_type" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Select relay type">
                        <option value="smtp">Deliver to my email server (SMTP)</option>
                        <option value="smtps">Deliver to my email server (SMTP with SSL/TLS)</option>
                    </select>
                    <p v-if="form.errors.has('destination')" class="text-red-500 text-xs py-1">
                        {{ form.errors.get('destination') }}
                    </p>
                </div>
                <div class="w-1/2 relative transition duration-300 border border-gray-300 rounded-md px-3 py-2 my-4 shadow-sm focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
                    <label for="receive_type" class="absolute -top-2 left-2 -mt-px inline-block px-1 bg-white text-xs font-base text-gray-900">Delivery type</label>
                    <select v-model="form.receive_type" id="receive_type" class="block w-full border-0 p-0 text-gray-900 placeholder-gray-500 focus:ring-0 sm:text-sm" placeholder="Select Delivery type">
                        <option value="load_balanced">Load balancing</option>
                        <option value="failover">Failover</option>
                    </select>
                    <p v-if="form.errors.has('receive_type')" class="text-red-500 text-xs py-1">
                        {{ form.errors.get('receive_type') }}
                    </p>
                </div>
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
                <button type="submit" @click="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Save
                </button>
            </div>
        </div>
    </form>
</template>

<script>
import { reactive, ref, onMounted } from 'vue'
import Form from '../classes/Form'
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/solid'
import { ArrowLeftIcon } from '@heroicons/vue/outline'

export default {
    props: [
        'id'
    ],
    components: {
        ArrowLeftIcon,
        ChevronDownIcon,
        Disclosure,
        DisclosureButton,
        DisclosurePanel
    },
    setup(props) {
        let { id } = props
        let form = reactive(new Form({
            name: '',
            active: '',
            allowed_accounts: '',
            destination: '',
            receive_type: 'smtp',
            relay_type: 'failover'
        }))
        let nodes = ref([])

        onMounted(async () => {
            if(id) {
                let res = (await axios.get(`/api/domains/${id}/`)).data
                form.name = res.name,
                form.active = res.active,
                form.allowed_accounts = res.allowed_accounts,
                form.destination = res.destination,
                form.receive_type = res.receive_type,
                form.relay_type = res.relay_type
            }
            nodes = (await axios.get('/api/hosts/'))
        })

        return {
            form,
            nodes,
            id
        }
    },
    methods: {
        async submit() {
            if (this.id) {
                await this.form.patch(`/api/domains/${this.id}/`)
            }
            else {
                await this.form.post('/api/domains/')
            }
        }
    }
}
</script>