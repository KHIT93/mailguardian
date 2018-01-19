<template>
    <div class="container mx-auto">
        <div class="bg-white border sm:rounded shadow">
            <div class="flex shadow">
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r px-2 py-2 font-semibold">
                    <div class="">
                        From
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r px-2 py-2 font-semibold">
                    <div class="">
                        To
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r px-2 py-2 font-semibold">
                    <div class="">
                        Subject
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r px-2 py-2 font-semibold">
                    <div class="">
                        Recieved
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 px-2 py-2 font-semibold">
                    <div class="">
                        Status
                    </div>
                </div>
            </div>
            <div class="flex text-sm break-words items-center p-2" v-if="count == 0">
                <p>There are currently no messages to display</p>
            </div>
            <div class="flex hover:bg-grey-lighter text-sm cursor-pointer break-words" v-for="item in messages" :key="item.id" @click="details(item.id)" v-else>
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r p-2">
                    <div class="">
                        <p>{{ item.from_address }}</p>
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r p-2">
                    <div class="">
                        <p>{{ item.to_address }}</p>
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r p-2">
                    <div class="">
                        <p>{{ item.subject }}</p>
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r p-2">
                    <div class="">
                        <p>{{ item.timestamp }}</p>
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 p-2">
                    <div class="">
                        <p>Status</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import router from '../routing/router';
export default {
    props: ['messages', 'count'],
    data: () => {
        return {

        }
    },
    methods: {
        details(id) {
            router.push('/messages/'+id);
        }
    }
}
</script>