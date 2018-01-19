<template>
    <mw-message-list :messages="messages"></mw-message-list>
</template>
<script>
import { mapMutations } from 'vuex';
import MessageList from '../../components/MessageList.vue';
export default {
    components: {
        'mw-message-list': MessageList
    },
    data: () => {
        return {
            messages: [],
            interval: null,
        }
    },
    mounted() {
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