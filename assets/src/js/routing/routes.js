/**
 * Import Vue components to use for Vue-Router
 */
import NotFound from '../pages/NotFound.vue';
import AccessDenied from '../pages/AccessDenied.vue';
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
import DomainForm from '../pages/Admin/Domains/Form.vue';
import Users from '../pages/Admin/Users/Index.vue';
import UserForm from '../pages/Admin/Users/Form.vue';
import Hosts from '../pages/Admin/Hosts/Index.vue';
import HostForm from '../pages/Admin/Hosts/Form.vue';
import SpamAssassinRules from '../pages/Admin/SpamAssassin/Rules/Index.vue';
import SpamAssassinRuleForm from '../pages/Admin/SpamAssassin/Rules/Form.vue';
import MailScannerConfiguration from '../pages/Admin/MailscannerConfig/Index.vue';
import MailScannerConfigurationForm from '../pages/Admin/MailscannerConfig/Form.vue';
import Settings from '../pages/Admin/Settings/Index.vue';
import PasswordReset from '../pages/PasswordReset/Index.vue';
import PasswordResetConfirm from '../pages/PasswordReset/Confirm.vue';

import SetupIndex from '../setup/Index.vue';

export default [
    { path: '/', component: Home, name: 'home', meta: { requiresAuth: true } },
    { path: '/login', component: Login, name: 'login', meta: { requiresAuth: false } },
    { path: '/messages', component: Messages, name: 'messages.index', meta: { requiresAuth: true } },
    { path: '/messages/:uuid', component: MessageDetails, name: 'messages.detail', props: true, meta: { requiresAuth: true } },
    { path: '/lists', component: Lists, name: 'lists.index', meta: { requiresAuth: true } },
    { path: '/reports', component: Reports, name: 'reports.index', meta: { requiresAuth: true } },
    { path: '/reports/messages', component: ReportMessageList, name: 'reports.messages', meta: { requiresAuth: true } },
    { path: '/reports/message-operations', component: ReportMessageOperations, name: 'reports.messages.operations', meta: { requiresAuth: true } },
    { path: '/reports/messages-by-date', component: ReportMessagesByDate, name: 'reports.messages.date', meta: { requiresAuth: true } },
    { path: '/reports/top-mail-relays', component: ReportMessageRelays, name: 'reports.messages.relays', meta: { requiresAuth: true } },
    { path: '/reports/messages-per-hour', component: ReportMessagePerHour, name: 'reports.message.hour', meta: { requiresAuth: true } },
    { path: '/reports/top-senders-by-quantity', component: ReportTopSendersByQuantity, name: 'reports.messages.sender.quantity', meta: { requiresAuth: true } },
    { path: '/reports/top-senders-by-volume', component: ReportTopSendersByVolume, name: 'reports.messages.sender.volume', meta: { requiresAuth: true } },
    { path: '/reports/top-recipients-by-quantity', component: ReportTopRecipientsByQuantity, name: 'reports.messages.recipient.quantity', meta: { requiresAuth: true } },
    { path: '/reports/top-recipients-by-volume', component: ReportTopRecipientsByVolume, name: 'reports.messages.recipient.volume', meta: { requiresAuth: true } },
    { path: '/reports/top-sender-domains-by-quantity', component: ReportTopSenderDomainsByQuantity, name: 'reports.messages.sender.domains.quantity', meta: { requiresAuth: true } },
    { path: '/reports/top-sender-domains-by-volume', component: ReportTopSenderDomainsByVolume, name: 'reports.messages.sender.domains.volume', meta: { requiresAuth: true } },
    { path: '/reports/top-recipient-domains-by-quantity', component: ReportTopRecipientDomainsByQuantity, name: 'reports.messages.recipient.domains.quantity', meta: { requiresAuth: true } },
    { path: '/reports/top-recipient-domains-by-volume', component: ReportTopRecipientDomainsByVolume, name: 'reports.messages.recipient.domains.volume', meta: { requiresAuth: true } },

    { path: '/tools', component: Tools, name: 'tools.index', meta: { requiresAuth: true } },
    { path: '/tools/mailqueue', component: Mailqueue, name: 'tools.mailqueue', meta: { requiresAdmin: true } },
    { path: '/tools/sa-status', component: SpamAssassinUpdateStatus, name: 'tools.sa.status', meta: { requiresAdmin: true } },

    { path: '/admin/domains', component: Domains, name: 'admin.domains.index', meta: { requiresAdmin: true } },
    { path: '/admin/domains/add', component: DomainForm, name: 'admin.domains.add', meta: { requiresAdmin: true } },
    { path: '/admin/domains/:id', component: DomainForm, name: 'admin.domains.edit', props: true, meta: { requiresAdmin: true } },
    { path: '/admin/users', component: Users, name: 'admin.users.index', meta: { requiresDomainAdmin: true } },
    { path: '/admin/users/add', component: UserForm, name: 'admin.users.add', meta: { requiresDomainAdmin: true } },
    { path: '/admin/users/:id', component: UserForm, name: 'admin.users.edit', props: true, meta: { requiresDomainAdmin: true } },
    { path: '/admin/hosts', component: Hosts, name: 'admin.hosts.index', meta: { requiresAdmin: true } },
    { path: '/admin/hosts/add', component: HostForm, name: 'admin.hosts.add', meta: { requiresDomainAdmin: true } },
    { path: '/admin/hosts/:id', component: HostForm, name: 'admin.hosts.edit', props: true, meta: { requiresDomainAdmin: true } },

    { path: '/admin/spamassassin/rules', component: SpamAssassinRules, name: 'admin.spamassassin.rules.index', meta: { requiresAdmin: true } },
    { path: '/admin/spamassassin/rules/add', component: SpamAssassinRuleForm, name: 'admin.spamassassin.rules.add', meta: { requiresAdmin: true } },
    { path: '/admin/spamassassin/rules/:id', component: SpamAssassinRuleForm, name: 'admin.spamassassin.rules.edit', props: true, meta: { requiresAdmin: true } },

    { path: '/admin/mailscanner/configuration', component: MailScannerConfiguration, name: 'admin.mailscanner.configuration.index', meta: { requiresAdmin: true } },
    { path: '/admin/mailscanner/configuration/add', component: MailScannerConfigurationForm, name: 'admin.mailscanner.configuration.add', meta: { requiresAdmin: true } },
    { path: '/admin/mailscanner/configuration/:id', component: MailScannerConfigurationForm, name: 'admin.mailscanner.configuration.edit', props: true, meta: { requiresAdmin: true } },
    { path: '/admin/settings', component: Settings, name: 'admin.settings.index', meta: { requiresAdmin: true } },

    { path: '/password-reset', component: PasswordReset, name: 'password.reset'},
    { path: '/password-reset/confirm/:uid/:token/', component: PasswordResetConfirm, name: 'password.reset.confirm', props: true},

    /** Routing for initial setup wizard */
    { path: '/setup', component: SetupIndex, name: 'setup.index' },

    /** Route to handle 'Access Denied' errors */
    { path: '/403', component: AccessDenied, name: 'access_denied' },
    
    /** Catchall route to display 404 page */
    { path: '*', component: NotFound, name: 'not_found' }
]