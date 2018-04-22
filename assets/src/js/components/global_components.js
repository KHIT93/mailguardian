import Vue from 'vue';
import Modal from './Modal.vue';
import MainWrapper from './MainWrapper.vue';
import NotificationWrapper from './NotificationWrapper.vue';

Vue.component('mw-modal', Modal);

export default {
    'mw-wrapper': MainWrapper,
    'mw-notifications': NotificationWrapper
}