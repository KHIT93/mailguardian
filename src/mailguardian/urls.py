"""MailGuardian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from frontend.views import IndexTemplateView, DashboardApiView
from rest_framework import routers
from core.viewsets import (
    UserViewSet,
    MailScannerConfigurationViewSet,
    SettingsViewSet,
    MailScannerHostViewSet,
    ApplicationTaskViewSet,
    ApplicationNotificationViewSet,
    TwoFactorConfigurationViewSet,
    TwoFactorBackupCodeViewSet
)
from mail.viewsets import (
    MessageViewSet,
    SpamReportViewSet,
    RblReportViewSet,
    McpReportViewSet,
    HeaderViewSet,
    MailscannerReportViewSet,
    TransportLogViewSet,
    SmtpRelayViewSet
)
from core.views import CurrentUserView, MailScannerConfigurationFilePathsView, LoginView, DataImportUploadAPIView
from lists.viewsets import ListEntryViewSet, BlocklistEntryViewSet, AllowlistEntryViewSet
from reports.views import (
    SummaryApiView,
    MessageListApiView,
    MessagesByDateApiView,
    TopMailRelaysApiView,
    MessagesPerHourApiView,
    TopSendersByQuantityApiView,
    TopSendersByVolumeApiView,
    TopRecipientsByQuantityApiView,
    TopRecipientsByVolumeApiView,
    TopSenderDomainsByQuantityApiView,
    TopSenderDomainsByVolumeApiView,
    TopRecipientDomainsByQuantityApiView,
    TopRecipientDomainsByVolumeApiView
)
from domains.viewsets import DomainViewSet
from setup_wizard.views import LicenseAPIView, InstalledAPIView, InitializeDatabaseAPIView
from spamassassin.viewsets import RuleDescriptionViewSet, RuleViewSet
from rest_auth.views import (
    LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'mailscanner-configuration', MailScannerConfigurationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'message-headers', HeaderViewSet)
router.register(r'spam-reports', SpamReportViewSet)
router.register(r'rbl-reports', RblReportViewSet)
router.register(r'mcp-reports', McpReportViewSet)
router.register(r'mailscanner-reports', MailscannerReportViewSet)
router.register(r'transport-logs', TransportLogViewSet)
router.register(r'smtp-relays', SmtpRelayViewSet)
router.register(r'sa-rules', RuleViewSet)
router.register(r'sa-rule-descriptions', RuleDescriptionViewSet)
router.register(r'blocklist', BlocklistEntryViewSet)
router.register(r'allowlist', AllowlistEntryViewSet)
router.register(r'lists', ListEntryViewSet)
router.register(r'domains', DomainViewSet)
router.register(r'hosts', MailScannerHostViewSet)
router.register(r'settings', SettingsViewSet)
router.register(r'tasks', ApplicationTaskViewSet)
router.register(r'notifications', ApplicationNotificationViewSet)
router.register(r'two-factor', TwoFactorConfigurationViewSet)
router.register(r'two-factor-codes', TwoFactorBackupCodeViewSet)

urlpatterns = [
    path('', IndexTemplateView.as_view()),
    path('api/', include(router.urls))
]

if not settings.API_ONLY:
    urlpatterns += [
        path('api/current-user/', CurrentUserView.as_view()),
        path('api/dashboard/', DashboardApiView.as_view()),
        path('api/reports/summary/', SummaryApiView.as_view()),
        path('api/reports/messages/', MessageListApiView.as_view()),
        path('api/reports/messages-by-date/', MessagesByDateApiView.as_view()),
        path('api/reports/top-mail-relays/', TopMailRelaysApiView.as_view()),
        path('api/reports/messages-per-hour/', MessagesPerHourApiView.as_view()),
        path('api/reports/top-senders-by-quantity/', TopSendersByQuantityApiView.as_view()),
        path('api/reports/top-senders-by-volume/', TopSendersByVolumeApiView.as_view()),
        path('api/reports/top-recipients-by-quantity/', TopRecipientsByQuantityApiView.as_view()),
        path('api/reports/top-recipients-by-volume/', TopRecipientsByVolumeApiView.as_view()),
        path('api/reports/top-sender-domains-by-quantity/', TopSenderDomainsByQuantityApiView.as_view()),
        path('api/reports/top-sender-domains-by-volume/', TopSenderDomainsByVolumeApiView.as_view()),
        path('api/reports/top-recipient-domains-by-quantity/', TopRecipientDomainsByQuantityApiView.as_view()),
        path('api/reports/top-recipient-domains-by-volume/', TopRecipientDomainsByVolumeApiView.as_view()),
        path('api/mailscanner-configuration-filepaths/', MailScannerConfigurationFilePathsView.as_view()),
        path('api/data-import/', DataImportUploadAPIView.as_view()),
        path('api/license/', LicenseAPIView.as_view()),
        path('api/installed/', InstalledAPIView.as_view()),
        path('api/setup/install/', InitializeDatabaseAPIView.as_view()),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]
    # URL for rest-auth
    urlpatterns += [
        # URLs that do not require a session or valid token
        re_path(r'^rest-auth/password/reset/$', PasswordResetView.as_view(),
            name='rest_password_reset'),
        re_path(r'^rest-auth/password/reset/confirm/$', PasswordResetConfirmView.as_view(),
            name='rest_password_reset_confirm'),
        re_path(r'^rest-auth/login/$', LoginView.as_view(), name='rest_login'),
        # URLs that require a user to be logged in with a valid session / token.
        re_path(r'^rest-auth/logout/$', LogoutView.as_view(), name='rest_logout'),
        re_path(r'^rest-auth/user/$', UserDetailsView.as_view(), name='rest_user_details'),
        re_path(r'^rest-auth/password/change/$', PasswordChangeView.as_view(),
            name='rest_password_change'),
    ]

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]

# Add final wildcard route to catch the deep links
# into the frontend SPA
urlpatterns += [
    path('<path:spa_path>', IndexTemplateView.as_view()),
    # This needs to be below in order to allow for the system to generate
    # the Password reset confirmation URL
    re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
]