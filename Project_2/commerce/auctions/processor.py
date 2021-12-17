from .models import Item
def watchlist_items_count(request):
    if request.user.is_authenticated:
      context = {
          'item_count': request.user.watchlist.all().count(),
      }
    else:
      context = { 'item_count': 0 }
    return context
