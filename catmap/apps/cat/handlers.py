# -*- coding: utf-8 -*-
def add_log_for_cat(instance, *args, **kwargs):
    """
    Set the cats current status
    """
    cat = instance.obj
    cat.current_status = instance.action
    cat.save(update_fields=['current_status'])
