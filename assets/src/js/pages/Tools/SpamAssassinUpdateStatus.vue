<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="bg-white border sm:rounded shadow p-2">
            <div v-if="!user.is_staff">
                <p>You are not authorized to view the mail queue</p>
            </div>
            <div v-else>
                <p>The rules were last synchroized with the application on {{ last_updated }}.</p>
                <button @click="sync" type="button" class="bg-blue hover:bg-blue-dark no-underline text-white font-semibold py-2 px-4 border border-blue hover:border-bleu-dark text-sm rounded">Synchronize rule descriptions</button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
export default {
    data: () => {
        return {
            last_updated: 'N/A'
        }
    },
    mounted() {
        if (this.user.is_staff) {
            this.get();
        }
    },
    computed: {
        ...mapGetters(['user'])
    },methods: {
        get() {
            axios.post('/api/settings/by-key/', {'key': 'sa.last_updated'}).then(response => {
                this.last_updated = response.data.value;
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        sync() {
            this.toggleLoading();
            axios.post('/api/sa-rules/sync/').then(response => {
                this.last_updated = response.data.value;
                this.toggleLoading();
            }).catch(error => {
                this.toggleLoading();
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        ...mapMutations(['notify', 'toggleLoading'])
    }
}
</script>

<style>

</style>
