<template>
    <div class="absolute pin-r pin-b z-10" v-cloak>
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