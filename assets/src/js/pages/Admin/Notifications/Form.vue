<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="card p-2">
            <form @submit.prevent="submit">
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="title">
                            Title*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.title" class="form-input" name="title" id="title" type="text" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="body">
                            Message body*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <textarea v-model="form.body" class="form-input" name="body" id="body" required></textarea>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="relay_type">
                            Notification type
                        </label>
                    </div>
                    <div class="md:w-1/2 md:inline-flex">
                        <div class="relative">
                            <select v-model="form.notification_type" name="relay_type" class="form-select">
                                <option value="">-- Select Notification type --</option>
                                <option value="login">Login</option>
                                <option value="dashboard">Dashboard</option>
                            </select>
                            <div class="form-select-icon">
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="date_start">
                            Start date*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.date_start" class="form-input" name="date_start" id="date_start" type="date" required>
                    </div>
                </div>
                <div class="md:flex md:items-center mb-6 mt-4">
                    <div class="md:w-1/4">
                        <label class="block text-gray-700 font-bold md:text-right mb-1 md:mb-0 pr-4" for="date_end">
                            End date*
                        </label>
                    </div>
                    <div class="md:w-1/2">
                        <input v-model="form.date_end" class="form-input" name="date_end" id="date_end" type="date" required>
                    </div>
                </div>
                <div class="flex flex-row-reverse border-t pt-2">
                    <button type="submit" class="btn btn-blue shadow">
                        Submit
                    </button>
                    <button v-if="id" @click="destroy" type="button" class="mr-1 flex-shrink-0 bg-red-500 hover:bg-red-600 border-red-500 hover:border-red-600 text-sm border-4 text-white py-1 px-2 rounded shadow">
                        Delete
                    </button>
                </div>
            </form>
        </div>
    </div>
</mg-page>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import router from '../../../routing/router';
import Form from '../../../classes/Form';
export default {
    props: ['id'],
    data: () => {
        return {
            entity: {},
            form: {}
        }
    },
    created() {
        if (this.id) {
            this.get();
        }
        else {
            this.setLoading(false);
            this.form = new Form({
                title: '',
                body: '',
                notification_type: '',
                date_start: '',
                date_end: ''
            });
        }
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        get() {
            this.setLoading(true);
            axios.get('/api/notifications/'+this.id+'/').then(response => {
                this.entity = response.data;
                this.form = new Form({
                    id: response.data.id,
                    title: response.data.title,
                    body: response.data.body,
                    notification_type: response.data.notification_type,
                    date_start: response.data.date_start,
                    date_end: response.data.date_end
                });
                this.setLoading(false);
            }).catch(error => {
                this.setLoading(false);
                if (error.response.status == 404) {
                    router.push({ name: 'not_found' });
                }
                else if (error.response.status == 403) {
                    router.push({ name: 'access_denied' });
                }
            });
        },
        submit() {
            if (this.id) {
                this.update();
            }
            else {
                this.add();
            }
        },
        add() {
            this.setLoading(true);
            this.form.post('/api/notifications/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Notification created', `The notification ${data.title} has been created`, 'success'));
                this.setLoading(false);
                router.push('/admin/notifications');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        update() {
            this.setLoading(true);
            this.form.put('/api/notifications/'+this.entity.id+'/').then(data => {
                console.log(data);
                this.notify(this.createNotification('Notification updated', `The notification ${data.title} has been updated`, 'success'));
                this.setLoading(false);
                router.push('/admin/notifications');
            }).catch(error => {
                this.setLoading(false);
                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
            });
        },
        destroy() {
            this.$modal.show('dialog', {
                title: 'Delete notification?',
                text: `Are you sure that you want to remove this notification?`,
                buttons: [
                    {
                        title: 'Yes',
                        handler: () => {
                            this.setLoading(true);
                            this.form.delete('/api/notifications/'+this.entity.id+'/').then(data => {
                                this.setLoading(false);
                                this.notify(this.createNotification('Notification deleted', `The notification ${this.entity.title} has been deleted`, 'success'));
                            }).catch(error => {
                                this.setLoading(false);
                                this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
                            });
                            this.$modal.hide('dialog');
                            router.push('/admin/notifications');
                        },
                        default: true
                    },
                    {
                        title: 'No'
                    }
                ]
            });
        },
        ...mapMutations(['notify', 'setLoading'])
    }
}
</script>