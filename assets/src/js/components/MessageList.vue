<template>
    <div class="sm:container mx-auto">
        <div class="bg-white border sm:rounded shadow table-wrapper">
            <table class="table text-sm cursor-pointer break-words">
                <thead>
                    <tr>
                        <th>From</th>
                        <th>To</th>
                        <th class="hidden md:table-cell">Subject</th>
                        <th>Recieved</th>
                        <th class="hidden md:table-cell">Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="count == 0">
                        <td colspan="5">
                            There are currently no messages to display
                        </td>
                    </tr>
                    <tr v-for="item in messages" :key="item.id" class="text-grey-darker" @click="details(item.id)" v-else>
                        <td>{{ item.from_address }}</td>
                        <td>{{ item.to_address }}</td>
                        <td class="hidden md:table-cell">{{ item.subject }}</td>
                        <td>{{ item.timestamp }}</td>
                        <td class="hidden md:table-cell">Status</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
<script>
import router from '../routing/router';
import { mapGetters } from 'vuex';
export default {
    props: ['messages', 'count'],
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