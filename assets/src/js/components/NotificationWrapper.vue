<template>
    <div class="absolute right-0 bottom-0 z-10" v-cloak>
        <mg-notification v-for="item in notifications" :notification="item" :key="item.id"></mg-notification>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import Notification from './Notification.vue';
export default {
    data: () => {
        return {
            
        }
    },
    components: {
        'mg-notification': Notification
    },
    computed: {
        ...mapGetters(['notifications'])
    }
}
</script>