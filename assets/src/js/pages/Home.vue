<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="bg-white border sm:rounded shadow">
            <div class="sm:flex sm:justify-between">
                <div class="sm:w-1/3 text-center text-grey-darker py-6">
                    <div class="sm:border-r">
                        <div class="mb-2">
                            <span class="text-5xl">{{ daily_total }}</span>
                        </div>
                        <div class="uppercase">
                            Total emails recieved
                        </div>
                    </div>
                </div>
                <div class="sm:w-1/3 text-center text-grey-darker py-6">
                    <div class="sm:border-r">
                        <div class="mb-2">
                            <span class="text-5xl">{{ daily_spam }}</span>
                        </div>
                        <div class="uppercase">
                            Spam emails recieved
                        </div>
                    </div>
                </div>
                <div class="sm:w-1/3 text-center text-grey-darker py-6">
                    <div>
                        <div class="mb-2">
                            <span class="text-5xl">{{ daily_virus }}</span>
                        </div>
                        <div class="uppercase">
                            Viruses recieved
                        </div>
                    </div>
                </div>
            </div>
            <!-- Chart.js graph here for showing message stats -->
        </div>
    </div>
</template>

<script>
    import Modal from '../components/Modal.vue';
    export default {
        data: () => {
            return {
                chartdata: [],
                modal: false,
                daily_total: 0,
                daily_spam: 0,
                daily_virus: 0
            }
        },
        mounted() {
            this.get();
        },
        methods: {
            get() {
                axios.post('/api/dashboard/', {}).then(response => {
                    this.daily_total = response.data.daily_total;
                    this.daily_spam = response.data.daily_spam;
                    this.daily_virus = response.data.daily_virus;
                });
            }
        },
        components: {
            'mw-modal': Modal
        },
    }
</script>
