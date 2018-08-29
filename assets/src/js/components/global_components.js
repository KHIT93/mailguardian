import Vue from 'vue';
import Modal from './Modal.vue';
import MainWrapper from './MainWrapper.vue';
import NotificationWrapper from './NotificationWrapper.vue';
import PageLoading from './PageLoading.vue';

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
import DeviceHub from '../icons/DeviceHubIcon.vue';
import VerifiedUserIcon from '../icons/VerifiedUser.vue';

Vue.component('mg-modal', Modal);

Vue.component('mg-account-circle-icon', AccountCircleIcon);
Vue.component('mg-block-icon', BlockIcon);
Vue.component('mg-build-icon', BuildIcon);
Vue.component('mg-checkmark-icon', CheckmarkIcon);
Vue.component('mg-clear-icon', ClearIcon);
Vue.component('mg-dashboard-icon', DashboardIcon);
Vue.component('mg-delete-icon', DeleteIcon);
Vue.component('mg-dns-icon', DnsIcon);
Vue.component('mg-email-icon', EmailIcon);
Vue.component('mg-exit-to-app-icon', ExitToAppIcon);
Vue.component('mg-expand-less-icon', ExpandLessIcon);
Vue.component('mg-expand-more-icon', ExpandMoreIcon);
Vue.component('mg-exposure-icon', ExposureIcon);
Vue.component('mg-import-contacts-icon', ImportContactsIcon);
Vue.component('mg-insert-chart-icon', InsertChartIcon);
Vue.component('mg-lock-icon', LockIcon);
Vue.component('mg-menu-icon', MenuIcon);
Vue.component('mg-people-icon', PeopleIcon);
Vue.component('mg-playlist-add-checkmark-icon', PlaylistAddCheckmarkIcon);
Vue.component('mg-security-icon', SecurityIcon);
Vue.component('mg-settings-icon', SettingsIcon);
Vue.component('mg-widgets-icon', WidgetsIcon);
Vue.component('mg-navigate-before-icon', NavigateBefore);
Vue.component('mg-navigate-next-icon', NavigateNext);
Vue.component('mg-device-hub-icon', DeviceHub);
Vue.component('mg-verified-user-icon', VerifiedUserIcon);
Vue.component('mg-page', PageLoading);

export default {
    'mg-wrapper': MainWrapper,
    'mg-notifications': NotificationWrapper
}