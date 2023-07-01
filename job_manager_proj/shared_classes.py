from django.contrib.admin import (
    ModelAdmin,
    models,
)


class AbstractModelAdmin(ModelAdmin):
    def get_logs_by(self, obj):
        return models.LogEntry.objects.filter(
            object_id=obj.pk, content_type__model=self.opts.model_name
        )

    def author(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).first(), "user", None)
        return "unknown"

    def editor(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).last(), "user", None)
        return "unknown"

    def created(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).first(), "action_time", None)
        return "unknown"

    def edited(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).last(), "action_time", None)
        return "unknown"
