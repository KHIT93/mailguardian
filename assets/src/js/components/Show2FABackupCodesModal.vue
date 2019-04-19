<template>
    <div class="h-full">
        <h2 class="p-2 text-center">Your Two-Factor Backup codes</h2>
        <div class="px-4">
            <div v-if="!codes_loading" class="flex flex-col items-center">
                <p class="text-center">
                    Below you will find a set of Two-Factor backup codes for your account.
                    Please store these safely as this will be the only way to access your account if you should loose your Two-Factor device.
                </p>
                <p class="text-center">
                    <span v-for="code in codes" :key="code.id">{{ code.code }}<br/></span>
                </p>
            </div>
            <p v-else class="text-center">
                Fetching backup codes from the server. Please give us a moment
            </p>
        </div>
        <div class="px-6 py-4 border-t bg-gray-100 rounded-b">
            <div class="flex flex-row-reverse">
                <button type="button" @click.prevent="$emit('close')" :disabled="codes_loading" class="btn btn-green shadow">Close</button>
                <button type="button" @click.prevent="generate" v-if="codes.length < 5" :disabled="codes_loading" class="btn btn-orange shadow">Generate new codes</button>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data: () => {
        return {
            codes: [],
            codes_loading: true
        }
    },
    mounted() {
        this.get();
    },
    methods: {
        get() {
            this.codes_loading = true;
            axios.get('/api/two-factor-codes/my/').then(response => {
                this.codes = response.data;
                this.codes_loading = false;
            }).catch(error => {
                this.codes.push(error.response.data);
                this.codes_loading = false;
            })
        },
        generate() {
            this.$modal.show('dialog', {
                title: 'Generate new 2FA Backup codes?',
                text: `Are you sure that you want to generate new backup codes? This operation will generate ${5-this.codes.length} new codes`,
                buttons: [
                    {
                        title: 'Yes',
                        handler: () => {
                            this.codes_loading = true;
                            axios.post('/api/two-factor-codes/generate/', {}).then(response => {
                                this.get();
                                this.$modal.hide('dialog');
                            }).catch(error => {
                                this.$modal.hide('dialog');
                            })
                        },
                        default: true
                    },
                    {
                        title: 'No'
                    }
                ]
            });
            
        }
    }
}
</script>