from django.db.models import Max
def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def filter_or_none(model, *args, **kwargs):
    try:
        return model.objects.filter(*args, **kwargs)
    except model.DoesNotExist:
        return None


def get_max_value(query, field):
    try:
        ans = query.aggregate(Max(field))
        field = str(field + '__max')
        ans = ans[field]
        return ans
    except:
       return None


def get_max_obj(query, field):
    try:
        ans = query.aggregate(Max(field))
        return ans
    except:
        return None
