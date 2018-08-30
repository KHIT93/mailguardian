<template>
    <div v-if="!initializing">
        <div v-show="loading" class="absolute loader" style="top:50%; right:50%;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" class="stroke-current h-10 w-10">
                <circle cx="50" cy="50" fill="none" stroke-linecap="round" r="40" stroke-width="4" stroke="#000" stroke-dasharray="62.83185307179586 62.83185307179586" transform="rotate(360 -8.10878e-8 -8.10878e-8)">
                    <animateTransform attributeName="transform" type="rotate" calcMode="linear" values="0 50 50;360 50 50" keyTimes="0;1" dur="1s" begin="0s" repeatCount="indefinite"></animateTransform>
                </circle>
                <circle cx="50" cy="50" fill="none" stroke-linecap="round" r="35" stroke-width="4" stroke="#ccc" stroke-dasharray="54.97787143782138 54.97787143782138" stroke-dashoffset="54.97787143782138" transform="rotate(-360 -8.10878e-8 -8.10878e-8)">
                    <animateTransform attributeName="transform" type="rotate" calcMode="linear" values="0 50 50;-360 50 50" keyTimes="0;1" dur="1s" begin="0s" repeatCount="indefinite"></animateTransform>
                </circle>
            </svg>
        </div>
        <div v-show="!loading"><slot></slot></div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
export default {
    computed: {
        ...mapGetters(['loading', 'initializing'])
    }
}
</script>