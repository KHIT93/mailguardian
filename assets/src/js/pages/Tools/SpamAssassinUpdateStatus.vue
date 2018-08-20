<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <div v-if="!user.is_staff">
                <p>You are not authorized to view the mail queue</p>
            </div>
            <div v-else>
                <p>The rules were last synchroized with the application {{ last_updated | ago }}.</p>
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
    created() {
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
            axios.post('/api/sa-rule-descriptions/sync/').then(response => {
                this.notify(this.createNotification('Rule descriptions synchronized', 'The spamassassin rule descriptions have been synchronized with the application', 'success'))
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
