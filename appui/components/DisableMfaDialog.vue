<template>
    <div
        class="inline-block w-full sm:max-w-xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        >
        <DialogTitle
            as="h3"
            class="text-lg font-medium leading-6 text-gray-900"
            >
            Disable Two-Factor Authentication
        </DialogTitle>
        <div>
            <p>Are you sure that you want to disable Two-Factor Authentication?</p>
            <p>If yes, please press <code class="text-blue-700 bg-gray-100 p-1">Start</code> to intiate the deactivation</p>
            <button type="button" @click="startMfaDeactivation" v-if="!started" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Start
            </button>
            <template v-if="started">
                <p>Please input your verification code and press <code class="text-blue-700 bg-gray-100 p-1">Confirm</code> to complete the deactivation</p>
                <UFormGroup label="Verification code" size="md">
                    <UInput id="code" type="number" v-model="code" autocomplete="one-time-code"/>
                </UFormGroup>
                <div class="pt-5">
                    <div class="flex">
                        <button type="button" @click="deactivateTwoFactorAuth" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-500 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                            Confirm
                        </button>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>
<script setup>
import { DialogTitle } from '@headlessui/vue'
import { onMounted, reactive, ref } from 'vue'

const props = defineProps(['show', 'method'])
const emits = defineEmits(['close'])
let { show, method } = props
const started = ref(false)
const code = ref(null)

function deactivateTwoFactorAuth() {
    useBackendFetch(`/rest-auth/${method}/deactivate/`, { method:'POST', body: { code: code } }).then(response => {
        emits('close')
    }).catch(error => {
        console.error(error)
    })
}
function startMfaDeactivation() {
    started = true
    useBackendFetch('/rest-auth/code/request/', { method:'POST', body: { method: method } }).then(response => {
        console.log(response.data)
    }).catch(error => {
        console.error(error)
    })
}
</script>