<template>
    <mg-message-list :messages="messages" :count="message_count" class="lg:px-4 pt-6 pb-8"></mg-message-list>
</template>
<script>
import { mapMutations } from 'vuex';
import MessageList from '../../components/MessageList.vue';
export default {
    components: {
        'mg-message-list': MessageList
    },
    data: () => {
        return {
            messages: [],
            message_count: 0,
            interval: null,
        }
    },
    created() {
        this.getMessages();
        this.interval = setInterval(function () {
            this.getMessages();
        }.bind(this), 5000);
    },
    methods: {
        getMessages() {
            this.toggleLoading();
            axios.get('/api/messages/?page_size=50').then(response => {
                this.messages = response.data.results;
                this.message_count = response.data.count;
                this.toggleLoading();
            })
        },
        ...mapMutations(['toggleLoading'])
    },
    beforeDestroy() {
        clearInterval(this.interval);
    }
}
</script>