<template>
    <mg-page>
        <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
            <div class="card p-2">
                <h2 class="border-b pb-2">Contents of message <em>{{ uuid }}</em></h2>
                <div>
                    <div class="flex border-b pb-1">
                        <div class="w-1/2 md:w-1/3">From:</div>
                        <div class="w-1/2 md:w-2/3">{{message.from_address}}</div>
                    </div>
                    <div class="flex border-b pb-1">
                        <div class="w-1/2 md:w-1/3">Date:</div>
                        <div class="w-1/2 md:w-2/3">{{message.date}}</div>
                    </div>
                    <div class="flex pb-1">
                        <div class="w-1/2 md:w-1/3">Subject:</div>
                        <div class="w-1/2 md:w-2/3">{{message.subject}}</div>
                    </div>
                </div>
                <button role="button" @click="goback" class="btn btn-sm btn-green shadow ml-2">Go back</button>
            </div>
            <div class="card p-2" v-if="content.simple_version != ''">
                <p class="border-b">Simplied message ({{ content.simple_type }})</p>
                <div v-text="content.simple_version"/>
            </div>
            <div class="card p-2" v-if="content.rich_version != ''">
                <p class="border-b">Full message ({{ content.rich_type }})</p>
                <div v-html="content.rich_version"/>
            </div>

            <div class="card p-2" v-if="content.attachments">
                <p class="border-b">Email attachments</p>
                <p v-for="(value, index) in content.attachments" :key="index">{{value}}</p>
            </div>
        </div>
    </mg-page>
</template>

<script>
import { mapMutations, mapGetters } from 'vuex';
import router from '../../routing/router';
export default {
    props: ['uuid'],
    data: () => {
        return {
            content: {},
            message: {},
            file_exists: false
        }
    },
    created() {
        this.getQueueFileStatus().then(() => {
            if (!this.file_exists) {
                router.push({ name: 'not_found' });
            }
            else {
                this.getMessage();
                this.get();
            }
        });
    },
    methods: {
        get() {
            if (this.message.queue_file_exists) {
                axios.get('/api/messages/' + this.uuid + '/contents/').then(response => {
                    this.content = response.data.message;
                }).catch(error => {
                    if (error.response.status !== 404) {
                        this.notify(this.createNotification('An error occurred while getting the message contents', `${error}`, 'error'));
                    }
                });
            }
            else {
                this.content = 'Message contents are no longer available on this server';
            }
        },
        getMessage() {
            axios.get('/api/messages/' + this.uuid + '/').then(response => {
                this.message = response.data;
            }).catch(error => {
                if (error.response.status == 404) {
                    router.push({ name: 'not_found' });
                }
                else if (error.response.status == 403) {
                    router.push({ name: 'access_denied' });
                }
            })
        },
        getQueueFileStatus() {
            axios.get('/api/messages/'+this.uuid+'/file-exists/').then(response => {
                this.file_exists = response.data.file_exists;
            }).catch(error => {
                console.log(error.response);
            });
        },
        goback() {
            router.push('/messages/'+this.uuid);
        }
        ...mapMutations(['notify', 'toggleLoading', 'setLoading'])
    }
}
</script>