import Vue from 'vue';
import Modal from './Modal.vue';
import MainWrapper from './MainWrapper.vue';
import NotificationWrapper from './NotificationWrapper.vue';

import AccountCircleIcon from '../icons/AccountCircleIcon.vue';
import BlockIcon from '../icons/BlockIcon.vue';
import BuildIcon from '../icons/BuildIcon.vue';
import CheckmarkIcon from '../icons/CheckmarkIcon.vue';
import ClearIcon from '../icons/ClearIcon.vue';
import DashboardIcon from '../icons/DashboardIcon.vue';
import DeleteIcon from '../icons/DeleteIcon.vue';
import DnsIcon from '../icons/DnsIcon.vue';
import EmailIcon from '../icons/EmailIcon.vue';
import ExitToAppIcon from '../icons/ExitToAppIcon.vue';
import ExpandLessIcon from '../icons/ExpandLessIcon.vue';
import ExpandMoreIcon from '../icons/ExpandMoreIcon.vue';
import ExposureIcon from '../icons/ExposureIcon.vue';
import ImportContactsIcon from '../icons/ImportContactsIcon.vue';
import InsertChartIcon from '../icons/InsertChartIcon.vue';
import LockIcon from '../icons/LockIcon.vue';
import MenuIcon from '../icons/MenuIcon.vue';
import PeopleIcon from '../icons/PeopleIcon.vue';
import PlaylistAddCheckmarkIcon from '../icons/PlaylistAddCheckmarkIcon.vue';
import SecurityIcon from '../icons/SecurityIcon.vue';
import SettingsIcon from '../icons/SettingsIcon.vue';
import WidgetsIcon from '../icons/WidgetsIcon.vue';
import NavigateBefore from '../icons/NavigateBefore.vue';
import NavigateNext from '../icons/NavigateNext.vue';

Vue.component('mw-modal', Modal);

Vue.component('mw-account-circle-icon', AccountCircleIcon);
Vue.component('mw-block-icon', BlockIcon);
Vue.component('mw-build-icon', BuildIcon);
Vue.component('mw-checkmark-icon', CheckmarkIcon);
Vue.component('mw-clear-icon', ClearIcon);
Vue.component('mw-dashboard-icon', DashboardIcon);
Vue.component('mw-delete-icon', DeleteIcon);
Vue.component('mw-dns-icon', DnsIcon);
Vue.component('mw-email-icon', EmailIcon);
Vue.component('mw-exit-to-app-icon', ExitToAppIcon);
Vue.component('mw-expand-less-icon', ExpandLessIcon);
Vue.component('mw-expand-more-icon', ExpandMoreIcon);
Vue.component('mw-exposure-icon', ExposureIcon);
Vue.component('mw-import-contacts-icon', ImportContactsIcon);
Vue.component('mw-insert-chart-icon', InsertChartIcon);
Vue.component('mw-lock-icon', LockIcon);
Vue.component('mw-menu-icon', MenuIcon);
Vue.component('mw-people-icon', PeopleIcon);
Vue.component('mw-playlist-add-checkmark-icon', PlaylistAddCheckmarkIcon);
Vue.component('mw-security-icon', SecurityIcon);
Vue.component('mw-settings-icon', SettingsIcon);
Vue.component('mw-widgets-icon', WidgetsIcon);
Vue.component('mw-navigate-before-icon', NavigateBefore);
Vue.component('mw-navigate-next-icon', NavigateNext);

export default {
    'mw-wrapper': MainWrapper,
    'mw-notifications': NotificationWrapper
}