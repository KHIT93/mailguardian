<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2">
            <h2 class="border-b">Details for log entry</h2>
            <div class="md:flex md:items-center mb-6 mt-4">
                <div class="md:w-1/6">
                    <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4">
                        Timestamp
                    </label>
                </div>
                <div class="md:w-5/6">
                    {{ entry.timestamp | ago }}
                </div>
            </div>
            <div class="md:flex md:items-center mb-6 mt-4">
                <div class="md:w-1/6">
                    <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4">
                        Module
                    </label>
                </div>
                <div class="md:w-5/6">
                    {{ entry.module }}
                </div>
            </div>
            <div class="md:flex md:items-center mb-6 mt-4">
                <div class="md:w-1/6">
                    <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4">
                        Record ID
                    </label>
                </div>
                <div class="md:w-5/6">
                    {{ entry.object_pk }}
                </div>
            </div>
            <div class="md:flex md:items-center mb-6 mt-4">
                <div class="md:w-1/6">
                    <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4">
                        Action
                    </label>
                </div>
                <div class="md:w-5/6">
                    {{ entry.action_name }}
                </div>
            </div>
            <div class="md:flex md:items-center mb-6 mt-4">
                <div class="md:w-1/6">
                    <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4">
                        Perfomed by
                    </label>
                </div>
                <div class="md:w-5/6">
                    {{ entry.actor_email }}
                </div>
            </div>
            <div class="md:flex md:items-center mb-6 mt-4">
                <div class="md:w-1/6">
                    <label class="block text-grey-darker font-bold mb-1 md:mb-0 pr-4">
                        From IP Address
                    </label>
                </div>
                <div class="md:w-5/6">
                    {{ entry.remote_addr }}
                </div>
            </div>
            <template v-if="['Create', 'Update', 'Delete'].includes(entry.action_name)">
                <h3 class="border-b text-center pb-1">List of changes</h3>
                <div class="table-wrapper">
                    <table class="table text-sm break-words">
                        <thead>
                            <tr>
                                <th>Field</th>
                                <th>Value Before</th>
                                <th>Value After</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(change, key) in entry.changes" :key="key">
                                <td>{{key}}</td>
                                <td>{{change[0]}}</td>
                                <td>{{change[1]}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </template>
        </div>
    </div>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex';
export default {
    props: ['id'],
    data: () => {
        return {
            entry: []
        }
    },
    created() {
        this.get()
    },
    methods: {
        get() {
            axios.get('/api/audit-log/'+this.id+'/').then(response => {
                this.entry = response.data;
            }).catch(error => {
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        ...mapMutations(['toggleLoading', 'notify'])
    }
}
</script>
