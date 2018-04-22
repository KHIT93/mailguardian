<template>
    <div class="sm:container mx-auto">
        <div class="bg-white border sm:rounded shadow">
            <mw-message-list-header></mw-message-list-header>
            <div class="flex text-sm break-words items-center p-2" v-if="count == 0">
                <p>There are currently no messages to display</p>
            </div>
            <mw-message-list-entry v-for="item in messages" :key="item.id" :item="item" @click="details(item.id)" v-else></mw-message-list-entry>
        </div>
    </div>
</template>
<script>
import router from '../routing/router';
import MessageListHeader from './MessageListHeader.vue';
import MessageListEntry from './MessageListEntry.vue';
import { mapGetters } from 'vuex';
export default {
    props: ['messages', 'count'],
    components: {
        'mw-message-list-header': MessageListHeader,
        'mw-message-list-entry': MessageListEntry
    },
    data: () => {
        return {

        }
    },
    computed: {
        ...mapGetters(['loading'])
    },
    methods: {
        details(id) {
            router.push('/messages/'+id);
        }
    }
}
</script>