from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import FieldDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.utils import formats, timezone
from django.utils.encoding import smart_str
from django.db.models import QuerySet, Q, Field
from dateutil.tz import gettz
from dateutil import parser
import json
import ast

class LogEntryManager(models.Manager):
    """
    Custom manager for the :py:class:`LogEntry` model.
    """

    def log_create(self, instance, **kwargs):
        """
        Helper method to create a new log entry. This method automatically populates some fields when no explicit value
        is given.
        :param instance: The model instance to log a change for.
        :type instance: Model
        :param kwargs: Field overrides for the :py:class:`DataLogEntry` object.
        :return: The new log entry or `None` if there were no changes.
        :rtype: LogEntry
        """
        changes = kwargs.get('changes', None)
        pk = self._get_pk_value(instance)

        if changes is not None:
            kwargs.setdefault('content_type', ContentType.objects.get_for_model(instance))
            kwargs.setdefault('object_pk', pk)
            kwargs.setdefault('object_repr', smart_str(instance))

            if isinstance(pk, int):
                kwargs.setdefault('object_id', pk)

            get_additional_data = getattr(instance, 'get_additional_data', None)
            if callable(get_additional_data):
                kwargs.setdefault('additional_data', get_additional_data())

            # Delete log entries with the same pk as a newly created model. This should only be necessary when an pk is
            # used twice.
            if kwargs.get('action', None) is 'created':
                if kwargs.get('object_id', None) is not None and self.filter(content_type=kwargs.get('content_type'),
                                                                             object_id=kwargs.get(
                                                                                     'object_id')).exists():
                    self.filter(content_type=kwargs.get('content_type'), object_id=kwargs.get('object_id')).delete()
                else:
                    self.filter(content_type=kwargs.get('content_type'), object_pk=kwargs.get('object_pk', '')).delete()
            # save LogEntry to same database instance is using
            db = instance._state.db
            return self.create(**kwargs) if db is None or db == '' else self.using(db).create(**kwargs)
        return None

    def get_for_object(self, instance):
        """
        Get log entries for the specified model instance.
        :param instance: The model instance to get log entries for.
        :type instance: Model
        :return: QuerySet of log entries for the given model instance.
        :rtype: QuerySet
        """
        # Return empty queryset if the given model instance is not a model instance.
        if not isinstance(instance, models.Model):
            return self.none()

        content_type = ContentType.objects.get_for_model(instance.__class__)
        pk = self._get_pk_value(instance)

        if isinstance(pk, int):
            return self.filter(content_type=content_type, object_id=pk)
        else:
            return self.filter(content_type=content_type, object_pk=smart_str(pk))

    def get_for_objects(self, queryset):
        """
        Get log entries for the objects in the specified queryset.
        :param queryset: The queryset to get the log entries for.
        :type queryset: QuerySet
        :return: The LogEntry objects for the objects in the given queryset.
        :rtype: QuerySet
        """
        if not isinstance(queryset, QuerySet) or queryset.count() == 0:
            return self.none()

        content_type = ContentType.objects.get_for_model(queryset.model)
        primary_keys = list(queryset.values_list(queryset.model._meta.pk.name, flat=True))

        if isinstance(primary_keys[0], int):
            return self.filter(content_type=content_type).filter(Q(object_id__in=primary_keys)).distinct()
        elif isinstance(queryset.model._meta.pk, models.UUIDField):
            primary_keys = [smart_str(pk) for pk in primary_keys]
            return self.filter(content_type=content_type).filter(Q(object_pk__in=primary_keys)).distinct()
        else:
            return self.filter(content_type=content_type).filter(Q(object_pk__in=primary_keys)).distinct()

    def get_for_model(self, model):
        """
        Get log entries for all objects of a specified type.
        :param model: The model to get log entries for.
        :type model: class
        :return: QuerySet of log entries for the given model.
        :rtype: QuerySet
        """
        # Return empty queryset if the given object is not valid.
        if not issubclass(model, models.Model):
            return self.none()

        content_type = ContentType.objects.get_for_model(model)

        return self.filter(content_type=content_type)

    def _get_pk_value(self, instance):
        """
        Get the primary key field value for a model instance.
        :param instance: The model instance to get the primary key for.
        :type instance: Model
        :return: The primary key value of the given model instance.
        """
        pk_field = instance._meta.pk.name
        pk = getattr(instance, pk_field, None)

        # Check to make sure that we got an pk not a model object.
        if isinstance(pk, models.Model):
            pk = self._get_pk_value(pk)
        return pk

# Create your models here.
class DataLogEntry(models.Model):
    class Meta:
        get_latest_by = 'timestamp'
        ordering = ['-timestamp']
        verbose_name = _("datalog entry")
        verbose_name_plural = _("datalog entries")

    content_type = models.ForeignKey(to='contenttypes.ContentType', on_delete=models.CASCADE, related_name='+',
                                     verbose_name=_("content type"))
    object_pk = models.CharField(db_index=True, max_length=255, verbose_name=_("object pk"))
    object_id = models.BigIntegerField(blank=True, db_index=True, null=True, verbose_name=_("object id"))
    object_repr = models.TextField(verbose_name=_("object representation"))
    action = models.CharField(choices=(
        ('created', _("create")),
        ('updated', _("update")),
        ('deleted', _("delete")),
    ), verbose_name=_("action"), max_length=32, null=True, blank=True)
    changes = models.TextField(blank=True, verbose_name=_("change message"))
    actor = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='+', verbose_name=_("actor"))
    remote_addr = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("remote address"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("timestamp"))
    additional_data = models.JSONField(blank=True, null=True, verbose_name=_("additional data"))

    objects = LogEntryManager()

    def __str__(self):
        if self.action == 'created':
            fstring = _("Created {repr:s}")
        elif self.action == 'updated':
            fstring = _("Updated {repr:s}")
        elif self.action == 'deleted':
            fstring = _("Deleted {repr:s}")
        else:
            fstring = _("Logged {repr:s}")

        return fstring.format(repr=self.object_repr)

    @property
    def changes_dict(self):
        """
        :return: The changes recorded in this log entry as a dictionary object.
        """
        try:
            return json.loads(self.changes)
        except ValueError:
            return {}

    @property
    def changes_str(self, colon=': ', arrow=' \u2192 ', separator='; '):
        """
        Return the changes recorded in this log entry as a string. The formatting of the string can be customized by
        setting alternate values for colon, arrow and separator. If the formatting is still not satisfying, please use
        :py:func:`LogEntry.changes_dict` and format the string yourself.
        :param colon: The string to place between the field name and the values.
        :param arrow: The string to place between each old and new value.
        :param separator: The string to place between each field.
        :return: A readable string of the changes in this log entry.
        """
        substrings = []

        for field, values in self.changes_dict.items():
            substring = '{field_name:s}{colon:s}{old:s}{arrow:s}{new:s}'.format(
                field_name=field,
                colon=colon,
                old=values[0],
                arrow=arrow,
                new=values[1],
            )
            substrings.append(substring)

        return separator.join(substrings)

    @property
    def changes_display_dict(self):
        """
        :return: The changes recorded in this log entry intended for display to users as a dictionary object.
        """
        # Get the model and model_fields
        from .registry import auditlog
        model = self.content_type.model_class()
        model_fields = auditlog.get_model_fields(model._meta.model)
        changes_display_dict = {}
        # grab the changes_dict and iterate through
        for field_name, values in self.changes_dict.items():
            # try to get the field attribute on the model
            try:
                field = model._meta.get_field(field_name)
            except FieldDoesNotExist:
                changes_display_dict[field_name] = values
                continue
            values_display = []
            # handle choices fields and Postgres ArrayField to get human readable version
            choices_dict = None
            if getattr(field, 'choices') and len(field.choices) > 0:
                choices_dict = dict(field.choices)
            if hasattr(field, 'base_field') and isinstance(field.base_field, Field) and getattr(field.base_field, 'choices') and len(field.base_field.choices) > 0:
                choices_dict = dict(field.base_field.choices)

            if choices_dict:
                for value in values:
                    try:
                        value = ast.literal_eval(value)
                        if type(value) is [].__class__:
                            values_display.append(', '.join([choices_dict.get(val, 'None') for val in value]))
                        else:
                            values_display.append(choices_dict.get(value, 'None'))
                    except ValueError:
                        values_display.append(choices_dict.get(value, 'None'))
                    except:
                        values_display.append(choices_dict.get(value, 'None'))
            else:
                try:
                    field_type = field.get_internal_type()
                except AttributeError:
                    # if the field is a relationship it has no internal type and exclude it
                    continue
                for value in values:
                    # handle case where field is a datetime, date, or time type
                    if field_type in ["DateTimeField", "DateField", "TimeField"]:
                        try:
                            value = parser.parse(value)
                            if field_type == "DateField":
                                value = value.date()
                            elif field_type == "TimeField":
                                value = value.time()
                            elif field_type == "DateTimeField":
                                value = value.replace(tzinfo=timezone.utc)
                                value = value.astimezone(gettz(settings.TIME_ZONE))
                            value = formats.localize(value)
                        except ValueError:
                            pass
                    # check if length is longer than 140 and truncate with ellipsis
                    if len(value) > 140:
                        value = "{}...".format(value[:140])

                    values_display.append(value)
            verbose_name = model_fields['mapping_fields'].get(field.name, getattr(field, 'verbose_name', field.name))
            changes_display_dict[verbose_name] = values_display
        return changes_display_dict