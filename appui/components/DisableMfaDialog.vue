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
                <FormInput v-model="code" label="Verification code" type="number" input-id="code"/>
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
<script>
import { DialogTitle } from '@headlessui/vue'
import { CheckIcon } from '@heroicons/vue/24/solid'
import FormInput from './FormInput.vue'
import { onMounted, reactive, ref } from 'vue'
export default {
    props: ['show', 'method'],
    components: {
        DialogTitle,
        CheckIcon,
        FormInput
    },
    setup(props) {
        let { show, method } = props
        const started = ref(false)
        const code = ref(null)
        return {
            show,
            method,
            started,
            code
        }
    },
    methods: {
        deactivateTwoFactorAuth() {
            useBackendFetch(`/rest-auth/${this.method}/deactivate/`, { method:'POST', body: { code: this.code } }).then(response => {
                this.$emit('close')
            }).catch(error => {
                console.error(error)
            })
        },
        startMfaDeactivation() {
            this.started = true
            useBackendFetch('/rest-auth/code/request/', { method:'POST', body: { method: this.method } }).then(response => {
                console.log(response.data)
            }).catch(error => {
                console.error(error)
            })
        }
    }
}
</script>