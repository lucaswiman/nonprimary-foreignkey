import django
from django.core import checks

if django.VERSION < (1, 8):
    from django.db.models.loading import get_model
else:
    from django.apps import apps
    get_model = apps.get_model


class NonPrimaryForeignKey(object):
    """
    Descriptor class for handling non-primary foreign keys.

    The implementation is loosely based on ``GenericForeignKey`` from the
    ``django.contrib.contenttypes`` module.
    """

    def __init__(self, to_model, from_field, to_field):
        self._to_model = to_model
        self.from_field = from_field
        self.to_field = to_field
        self.editable = False

    @property
    def to_model(self):
        return get_model(self._to_model)

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        self.cache_attr = "_%s_cache" % name
        setattr(cls, name, self)

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        try:
            return getattr(instance, self.cache_attr)
        except AttributeError:
            rel_obj = None
            f = self.model._meta.get_field(self.from_field)
            value = getattr(instance, f.get_attname(), None)
            if value is None:
                return None
            rel_obj = self.to_model._default_manager.get(
                **{self.to_field: value})
            setattr(instance, self.cache_attr, rel_obj)
            return rel_obj

    def __set__(self, instance, value):
        if not (value is None or isinstance(value, self.to_model)):
            raise TypeError('%r must is not a %s' % (value, self.to_model))
        to_f = self.to_model._meta.get_field(self.to_field)
        f = self.model._meta.get_field(self.from_field)
        set_value = getattr(value, to_f.get_attname(), None)
        setattr(instance, self.cache_attr, value)
        setattr(instance, f.get_attname(), set_value)

    def __str__(self):
        model = self.model
        app = model._meta.app_label
        return '%s.%s.%s' % (app, model._meta.object_name, self.name)

    def check(self, **kwargs):
        errors = []
        if self.name.endswith("_"):
            errors.append(
                checks.Error(
                    'Field names must not end with an underscore.',
                    hint=None,
                    obj=self,
                    id='fields.E001',
                )
            )
        return errors

    def get_prefetch_queryset(self, instances, queryset=None):
        raise NotImplementedError()