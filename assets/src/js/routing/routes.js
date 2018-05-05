/**
 * Import Vue components to use for Vue-Router
 */
import NotFound from '../pages/NotFound.vue';
import Home from '../pages/Home.vue';
import Login from '../pages/Login.vue';
import Messages from '../pages/Messages/Index.vue';
import MessageDetails from '../pages/Messages/Detail.vue';
import Lists from '../pages/Lists/Index.vue';
import Reports from '../pages/Reports/Index.vue';
import ReportMessageList from '../pages/Reports/Messages.vue';
import ReportMessageOperations from '../pages/Reports/MessageOperations.vue';
import ReportMessagesByDate from '../pages/Reports/MessagesByDate.vue';
import ReportMessageRelays from '../pages/Reports/MessageRelays.vue';
import ReportMessagePerHour from '../pages/Reports/MessagePerHour.vue';
import ReportTopSendersByQuantity from '../pages/Reports/TopSendersByQuantity.vue';
import ReportTopSendersByVolume from '../pages/Reports/TopSendersByVolume.vue';
import ReportTopRecipientsByQuantity from '../pages/Reports/TopRecipientsByQuantity.vue';
import ReportTopRecipientsByVolume from '../pages/Reports/TopRecipientsByVolume.vue';
import ReportTopSenderDomainsByQuantity from '../pages/Reports/TopSenderDomainsByQuantity.vue';
import ReportTopSenderDomainsByVolume from '../pages/Reports/TopSenderDomainsByVolume.vue';
import ReportTopRecipientDomainsByQuantity from '../pages/Reports/TopRecipientDomainsByQuantity.vue';
import ReportTopRecipientDomainsByVolume from '../pages/Reports/TopRecipientDomainsByVolume.vue';
import Tools from '../pages/Tools/Index.vue';
import Mailqueue from '../pages/Tools/Mailqueue.vue';
import SpamAssassinUpdateStatus from '../pages/Tools/SpamAssassinUpdateStatus.vue';
import Domains from '../pages/Admin/Domains/Index.vue';
import Users from '../pages/Admin/Users/Index.vue';
import UserForm from '../pages/Admin/Users/Form.vue';
import DomainForm from '../pages/Admin/Domains/Form.vue';
import MailScannerConfiguration from '../pages/Admin/MailscannerConfig/Index.vue';
import MailScannerConfigurationForm from '../pages/Admin/MailscannerConfig/Form.vue';
import Settings from '../pages/Admin/Settings/Index.vue';

export default [
    { path: '/', component: Home, name: 'home' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/messages', component: Messages, name: 'messages.index' },
    { path: '/messages/:uuid', component: MessageDetails, name: 'messages.detail', props: true },
    { path: '/lists', component: Lists, name: 'lists.index' },
    { path: '/reports', component: Reports, name: 'reports.index' },
    { path: '/reports/messages', component: ReportMessageList, name: 'reports.messages' },
    { path: '/reports/message-operations', component: ReportMessageOperations, name: 'reports.messages.operations' },
    { path: '/reports/messages-by-date', component: ReportMessagesByDate, name: 'reports.messages.date' },
    { path: '/reports/top-mail-relays', component: ReportMessageRelays, name: 'reports.messages.relays' },
    { path: '/reports/messages-per-hour', component: ReportMessagePerHour, name: 'reports.message.hour' },
    { path: '/reports/top-senders-by-quantity', component: ReportTopSendersByQuantity, name: 'reports.messages.sender.quantity'},
    { path: '/reports/top-senders-by-volume', component: ReportTopSendersByVolume, name: 'reports.messages.sender.volume'},
    { path: '/reports/top-recipients-by-quantity', component: ReportTopRecipientsByQuantity, name: 'reports.messages.recipient.quantity'},
    { path: '/reports/top-recipients-by-volume', component: ReportTopRecipientsByVolume, name: 'reports.messages.recipient.volume'},
    { path: '/reports/top-sender-domains-by-quantity', component: ReportTopSenderDomainsByQuantity, name: 'reports.messages.sender.domains.quantity'},
    { path: '/reports/top-sender-domains-by-volume', component: ReportTopSenderDomainsByVolume, name: 'reports.messages.sender.domains.volume'},
    { path: '/reports/top-recipient-domains-by-quantity', component: ReportTopRecipientDomainsByQuantity, name: 'reports.messages.recipient.domains.quantity'},
    { path: '/reports/top-recipient-domains-by-volume', component: ReportTopRecipientDomainsByVolume, name: 'reports.messages.recipient.domains.volume'},

    { path: '/tools', component: Tools, name: 'tools.index' },
    { path: '/tools/mailqueue', component: Mailqueue, name: 'tools.mailqueue' },
    { path: '/tools/sa-status', component: SpamAssassinUpdateStatus, name: 'tools.sa.status'},

    { path: '/admin/domains', component: Domains, name: 'admin.domains.index' },
    { path: '/admin/domains/add', component: DomainForm, name: 'admin.domains.add' },
    { path: '/admin/domains/:id', component: DomainForm, name: 'admin.domains.edit', props: true },
    { path: '/admin/users', component: Users, name: 'admin.users.index' },
    { path: '/admin/users/add', component: UserForm, name: 'admin.users.add' },
    { path: '/admin/users/:id', component: UserForm, name: 'admin.users.edit', props: true },
    { path: '/admin/mailscanner/configuration', component: MailScannerConfiguration, name: 'admin.mailscanner.configuration.index'},
    { path: '/admin/mailscanner/configuration/add', component: MailScannerConfigurationForm, name: 'admin.mailscanner.configuration.add' },
    { path: '/admin/mailscanner/configuration/:id', component: MailScannerConfigurationForm, name: 'admin.mailscanner.configuration.edit', props: true },
    { path: '/admin/settings', component: Settings, name: 'admin.settings.index'},

    /** Catchall route to display 404 page */
    { path: '*', component: NotFound, name: 'not_found' }
]