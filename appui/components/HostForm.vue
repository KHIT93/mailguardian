<template>
    <form method="POST" class="space-y-8 sm:space-y-5 divide-y divide-gray-200" @submit.prevent="submit">
        <div class="">
            <p v-if="form.errors.has('non_field_errors')" class="text-red-500">
                {{ form.errors.get('non_field_errors') }}
            </p>
            <FormInput inputId="hostname" label="Hostname" type="text" v-model="form.hostname"/>
            <p v-if="form.errors.has('hostname')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('hostname') }}
            </p>
            <hr class="my-4"/>
            <FormInput inputId="ip_address" label="IP Address" type="text" v-model="form.ip_address" class="my-4"/>
            <p v-if="form.errors.has('ip_address')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('ip_address') }}
            </p>
            <FormInput inputId="priority" label="Priority" type="number" v-model="form.priority"/>
            <p v-if="form.errors.has('priority')" class="text-red-500 text-xs py-1">
                {{ form.errors.get('priority') }}
            </p>
            <hr class="my-4"/>
            <div class="flex my-4 items-center">
                <input id="use_tls" v-model="form.use_tls" name="use_tls" type="checkbox" class="transition duration-300 h-4 w-4 text-blue-600 focus:ring-blue-500 border-2 border-gray-300 rounded" />
                <label for="use_tls" class="ml-2 block text-sm text-gray-900">
                    Communicate with this host using SSL/TLS encryption
                </label>
            </div>
            <div class="flex my-4 items-center">
                <input id="passive" v-model="form.passive" name="passive" type="checkbox" class="transition duration-300 h-4 w-4 text-blue-600 focus:ring-blue-500 border-2 border-gray-300 rounded" />
                <label for="passive" class="ml-2 block text-sm text-gray-900">
                    This host is passive
                </label>
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
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import FormInput from './FormInput.vue'
import Form from '~/classes/Form'
const props = defineProps({
    id: String
})
let form = reactive(new Form({
    hostname: '',
    ip_address: '',
    use_tls: false,
    priority: 10,
    passive: false
}))

const toast = useToast()

onMounted(async () => {
    if(props.id) {
        let res = (await useBackendFetch(`/api/hosts/${props.id}/`))
        form.hostname = res.hostname,
        form.ip_address = res.ip_address,
        form.use_tls = res.use_tls,
        form.priority = res.priority,
        form.passive = res.passive
    }
})

async function submit() {
    if (props.id) {
        await form.put(`/api/hosts/${props.id}/`)
        toast.add({
            title: `Host ${form.hostname} has been updated`
        })
    }
    else {
        await form.post('/api/hosts/')
        toast.add({
            title: `Host ${form.hostname} has been created`
        })
    }
}
</script>