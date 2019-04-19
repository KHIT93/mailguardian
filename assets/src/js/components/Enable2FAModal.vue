<template>
    <form @submit.prevent="submit" class="h-full">
        <h2 class="p-2 text-center">Enable Two-Factor Authentication</h2>
        <div class="px-4">
            <div v-if="!qr_loading" class="flex flex-col items-center">
                <img :src="qr" class="w-64 h-64"/>
                <p class="text-center">
                    Scan the above QR-code with your favorite two factor authentictation mobile app
                </p>
            </div>
            <p v-else class="text-center">
                Fetching QR-code from the server. Please give us a moment
            </p>
        </div>
        <div class="px-6 py-4 border-t bg-gray-100 rounded-b">
            <div class="flex flex-row-reverse">
                <button type="button" @click.prevent="$emit('close')" class="btn btn-gray-lightest shadow">Cancel</button>
                <button type="submit" class="btn btn-blue shadow mr-2">Enable 2FA</button>
            </div>
        </div>
    </form>
</template>
<script>
import { mapGetters, mapActions } from 'vuex';
import QRious from 'qrious';
export default {
    data: () => {
        return {
            qr: '',
            qr_loading: true,
            totp_key: ''
        }
    },
    mounted() {
        axios.get('/api/two-factor/qr/').then(response => {
            let qr = new QRious({
                value: response.data.url
            });
            this.qr = qr.toDataURL('image/jpeg');
            this.totp_key = response.data.totp_key;
            this.qr_loading = false;
        })
    },
    methods: {
        submit() {
            axios.put('/api/two-factor/enable/', {'totp_key': this.totp_key}).then(response => {
                if (response.status == 201) {
                    this.$emit('close');
                    this.getCurrentUser();
                }
            })
        },
        ...mapActions(['getCurrentUser'])
    }
}
</script>