<template>
<mg-page>
  <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <div v-if="!user.is_staff">
                <p>You are not authorized to view the mail queue</p>
            </div>
            <div v-else class="table-wrapper">
                <div class="mb-2">
                    Mail queue at {{ moment(loaded_at).format('YYYY-MM-DD HH:mm:ss') }}
                    <button type="button" class="btn btn-blue shadow" v-if="mails.length">
                        Resend all
                    </button>
                </div>
                <table class="w-full table text-sm">
                    <thead>
                        <tr>
                            <th>Queue ID</th>
                            <th>Sender</th>
                            <th>Recipients</th>
                            <th>Date</th>
                            <th>Status</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="mail in mails" :key="mail.qid" class="text-sm">
                            <td>{{ mail.qid }}</td>
                            <td>{{ mail.sender }}</td>
                            <td>{{ mail.recipients.join(', ') }}</td>
                            <td>{{ mail.date }}</td>
                            <td>{{ mail.status }}</td>
                            <td><button type="button" class="btn-sm btn-blue shadow" @click="resend(mail)">Resend</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
  </div>
</mg-page>
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
    created() {
        if (this.user.is_staff) {
            this.get();
        }
        
    },
    computed: {
        ...mapGetters(['isLoggedIn', 'user', 'loading'])
    },
    methods: {
        get() {
            this.setLoading(true);
            axios.get('/api/messages/queue/').then(response => {
                this.mails = response.data.mails;
                this.loaded_at = response.data.loaded_at;
                this.setLoading(false);
            });
        },
        resend(message) {
            axios.post('/api/messages/resend/', { 'messages': [{ 'qid': message.qid, 'hostname': message.hostname }] }).then(response => {
                this.notify(this.createNotification('Message resent', `The message has been resent and should be delivered soon`, 'success'));
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        async resend_all() {
            let messages;
            await this.mails.forEach((item,index) => {
                messages.push({
                    'qid': item.qid,
                    'hostname': item.hostname
                })
            });
            axios.post('/api/messages/resend/', { 'messages': messages }).then(response => {
                this.notify(this.createNotification('Message resent', `The message has been resent and should be delivered soon`, 'success'));
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        moment(str) {
            return window.moment(str);
        },
        ...mapMutations(['toggleLoading', 'setLoading', 'notify'])
    }
}
</script>