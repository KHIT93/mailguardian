import Vue from 'vue';
import Vuex from 'vuex';
import VuexFlash from 'vuex-flash';
import { createFlashStore } from 'vuex-flash';
import state from './state';
import getters from './getters';
import mutations from './mutations';
import actions from './actions';

Vue.use(Vuex);
Vue.use(VuexFlash, { mixin: true });


export const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions,
    plugins: [
        createFlashStore()
    ]
});