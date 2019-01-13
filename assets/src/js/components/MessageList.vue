<template>
    <div class="sm:container mx-auto">
        <div class="card table-wrapper">
            <table class="table text-sm cursor-pointer break-words">
                <thead>
                    <tr>
                        <th>From</th>
                        <th>To</th>
                        <th class="hidden md:table-cell">Subject</th>
                        <th>Recieved</th>
                        <th v-if="app_info.mailguardian_multi_node">Recieved on</th>
                        <th class="hidden md:table-cell">Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="count == 0">
                        <td colspan="5">
                            There are currently no messages to display
                        </td>
                    </tr>
                    <tr v-for="item in messages" :key="item.id" class="text-grey-darkest" :class="computeColorClasses(item)" @click="details(item.id)" v-else>
                        <td>{{ item.from_address }}</td>
                        <td>{{ item.to_address }}</td>
                        <td class="hidden md:table-cell">{{ item.subject }}</td>
                        <td>{{ new Date(item.timestamp).toLocaleString() }}</td>
                        <td v-if="app_info.mailguardian_multi_node">{{ item.mailscanner_hostname }}</td>
                        <td class="hidden md:table-cell">
                            <span v-if="item.is_clean">Clean</span>
                            <template v-else>
                                <span v-if="item.is_spam">Spam</span>
                                <span v-if="item.is_rbl_listed">RBL</span>
                                <span v-if="item.infected">Infected</span>
                            </template>
                            <span v-if="item.blacklisted">Blacklisted</span>
                            <span v-if="item.whitelisted">Whitelisted</span>
                        </td>
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
        ...mapGetters(['loading', 'app_info'])
    },
    methods: {
        details(id) {
            router.push('/messages/'+id);
        },
        computeColorClasses(item) {
            if (item.is_spam) {
                return 'bg-red';
            }
            if (item.is_rbl_listed) {
                return 'bg-orange';
            }
            if (item.blacklisted) {
                return 'bg-black text-white';
            }
            if (item.whitelisted) {
                return 'bg-green-lighter';
            }
        }
    }
}
</script>