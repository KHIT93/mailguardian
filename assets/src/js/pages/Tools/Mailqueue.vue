<template>
  <div class="container mx-auto sm:px-4 pt-6 pb-8">
        <div class="bg-white border sm:rounded shadow p-2">
            <div v-if="!user.is_staff">
                <p>You are not authorized to view the mail queue</p>
            </div>
            <div v-else>
                <div class="mb-2">
                    Mail queue at {{ moment(loaded_at).format('YYYY-MM-DD hh:mm:ss') }}
                </div>
                <table class="w-full">
                    <thead>
                        <tr>
                            <th>Queue ID</th>
                            <th>Sender</th>
                            <th>Recipients</th>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="mail in mails" :key="mail.qid">
                            <td>{{ mail.qid }}</td>
                            <td>{{ mail.sender }}</td>
                            <td>{{ mail.recipients }}</td>
                            <td>{{ mail.date }}</td>
                            <td>{{ mail.status }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
export default {
    data: () => {
        return {
            mails: [],
            loaded_at: null
        }
    },
    mounted() {
        if (this.user.is_staff) {
            this.get();
        }
    },
    computed: {
        ...mapGetters(['isLoggedIn', 'user', 'loading'])
    },
    methods: {
        get() {
            this.toggleLoading();
            axios.get('/api/messages/queue').then(response => {
                this.mails = response.data.mails;
                this.loaded_at = response.data.loaded_at;
                this.toggleLoading();
            });
        },
        moment(str) {
            return window.moment(str);
        },
        ...mapMutations(['toggleLoading'])
    }
}
</script>