<template>
    <form @submit.prevent="nextStep">
        <div class="p-4" v-if="qrcode">
            <QRCode :value="qrcode" render-as="svg" size="300"/>
        </div>
        <FormInput v-model="code" label="Verification code" type="number" input-id="code"/>
        <div class="pt-5">
            <div class="flex">
                <button type="submit" class="transition duration-300 ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Next
                </button>
            </div>
        </div>
    </form>
</template>
<script>
import { onMounted, ref, reactive } from 'vue'
import FormInput from '../FormInput.vue'
import QRCode from 'qrcode.vue'
export default {
    props: ['method'],
    components: {
        FormInput,
        QRCode
    },
    setup(props) {
        let code = ref('')
        const qrcode = ref('')
        const { method } = props
        onMounted(async () => {
            console.log(qrcode.value)
            let res = (await axios.post(`/rest-auth/${method}/activate/`)).data
            if (res.details.startsWith('otpauth://', 0)) {
                qrcode.value = res.details
            }
        })
        return {
            code,
            qrcode,
            method
        }
    },
    methods: {
        nextStep() {
            axios.post(`/rest-auth/${this.method}/activate/confirm/`, { code: this.code }).then(response => {
                this.$emit('complete', response.data)
            }).catch(error => {
                console.log(error)
            })
        }
    }
}
</script>