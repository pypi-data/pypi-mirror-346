def superusers_and_external_services(*, hijacker=None, hijacked=None):
    """
    Superusers, global superusers, and external service team users may hijack other users.
    """
    if hijacker.is_superuser or hijacker.is_global_superuser:
        return True

    if hijacker.is_external_service_team_user:
        return True
