from apps.audit.models import AuditLog

class AuditService:
    @classmethod
    def log_action(cls, action: str, entity: str, actor=None, ip_address=None, extra_data=None):
        return AuditLog.objects.create(
            actor=actor,
            action=action,
            entity=entity,
            ip_address=ip_address,
            extra_data=extra_data or {}
        )
