<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <div class="mb-2">
                Tasks
            </div>
            <table class="w-full table text-sm">
                <thead>
                    <tr>
                        <th>Task ID</th>
                        <th v-if="app_info.mailguardian_multi_node">Host</th>
                        <th>Recipients</th>
                        <th>Created</th>
                        <th>Updated</th>
                        <th>Completed</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="!count">
                        <td colspan="7">
                            There are currently no tasks to process
                        </td>
                    </tr>
                    <tr v-for="task in tasks" :key="task.id" class="text-sm" v-else>
                        <td>{{ mail.id }}</td>
                        <td v-if="app_info.mailguardian_multi_node">{{ mail.hostname }}</td>
                        <td>{{ mail.user_email }}</td>
                        <td>{{ mail.created }}</td>
                        <td>{{ mail.updated }}</td>
                        <td>{{ mail.completed }}</td>
                        <td>{{ mail.status_code }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex';
export default {
    data: () => {
        return {
            tasks: [],
            nextLink: null,
            previousLink: null,
            pages: 1,
            currentPage: 1,
            count: 0
        }
    },
    created() {
        this.get();
    },
    computed: {
        ...mapGetters(['loading', 'app_info'])
    },
    methods: {
        get() {
            axios.get('/api/tasks/').then(response => {
                this.tasks = response.data.results;
                this.nextLink = response.data.next;
                this.previousLink = response.data.previous;
                this.pages = response.data.page_count;
                this.currentPage = response.data.current;
                this.count = response.data.count;
            })
        },
        next() {

        },
        previous() {

        }
    }
}
</script>
