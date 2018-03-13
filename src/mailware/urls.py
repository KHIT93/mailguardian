"""mailware URL Configuration

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
from frontend.views import IndexTemplateView
from rest_framework import routers
from core.viewsets import UserViewSet, MailScannerConfigurationViewSet
from mail.viewsets import MessageViewSet, SpamReportViewSet, RblReportViewSet, McpReportViewSet, HeaderViewSet, MailscannerReportViewSet
from mail.views import MessageActionAPIView
from core.views import CurrentUserView, MailScannerConfigurationFilePathsView
from lists.viewsets import ListEntryViewSet, BlacklistEntryViewSet, WhitelistEntryViewSet
from reports.views import SummaryApiView, MessageListApiView, MessagesByDateApiView, TopMailRelaysApiView
from domains.viewsets import DomainViewSet, MailUserViewSet

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
router.register(r'blacklist', BlacklistEntryViewSet)
router.register(r'whitelist', WhitelistEntryViewSet)
router.register(r'lists', ListEntryViewSet)
router.register(r'domains', DomainViewSet)
router.register(r'mail-users', MailUserViewSet)

urlpatterns = [
    path('', IndexTemplateView.as_view()),
    path('api/current-user/', CurrentUserView.as_view()),
    path('api/', include(router.urls)),
    path('api/message-actions/', MessageActionAPIView.as_view()),
    path('api/reports/summary/', SummaryApiView.as_view()),
    path('api/reports/messages/', MessageListApiView.as_view()),
    path('api/reports/messages-by-date/', MessagesByDateApiView.as_view()),
    path('api/reports/top-mail-relays/', TopMailRelaysApiView.as_view()),
    path('api/mailscanner-configuration-filepaths/', MailScannerConfigurationFilePathsView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]