<template>
    <form @submit.prevent="nextStep">
        <div class="p-4" v-if="qrcode">
            <QRCode :value="qrcode" render-as="svg" size="300"/>
        </div>
        <UFormGroup label="Verification code" size="md">
            <UInput id="code" type="number" v-model="code" autocomplete="one-time-code"/>
        </UFormGroup>
        <div class="pt-5">
            <div class="flex">
                <button type="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Next
                </button>
            </div>
        </div>
    </form>
</template>
<script setup>
import { onMounted, ref, reactive } from 'vue'
import FormInput from '~/components/FormInput.vue'
import QRCode from 'qrcode.vue'

const props = defineProps(['method'])
const emits = defineEmits(['complete'])

let code = ref('')
const qrcode = ref('')
const { method } = props

onMounted(async () => {
    console.log(qrcode.value)
    let { data: res } = await useBackendFetch(`/rest-auth/${method}/activate/`, { method: 'POST'})
    if (res.details.startsWith('otpauth://', 0)) {
        qrcode.value = res.details
    }
})

function nextStep() {
    $fetch(`/rest-auth/${method}/activate/confirm/`, { method: 'POST', body: { code: code }}).then(response => {
        emits('complete', response.data)
    }).catch(error => {
        console.log(error)
    })
}
</script>