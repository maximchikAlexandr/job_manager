from django.contrib.admin import models

class LoggedAdminModelMixin:
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


class ReadOnlyAdminModelMixin:
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, _=None):
        return False

    def delete_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_delete"] = False
        return super().delete_view(request, object_id, extra_context=extra_context)
