import Vue from 'vue';
import Vuex from 'vuex';const LOGIN = "LOGIN";
import state from './state';
import getters from './getters';
import mutations from './mutations';
import actions from './actions';

const LOGIN_SUCCESS = "LOGIN_SUCCESS";
const LOGIN_FAILED = "LOGIN_FAILED";
const LOGOUT = "LOGOUT";

export const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions
});