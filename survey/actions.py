from django.utils.translation import ungettext, ugettext_lazy

# Actions
def make_published(modeladmin, request, queryset):
	"""
	Mark the given survey as published
	"""
	count = queryset.update(is_published=True)
	message = ungettext(
			u'%(count)d survey was successfully marked as published.',
			u'%(count)d surveys were successfully marked as published',
			count) % {'count': count,}
	modeladmin.message_user(request, message)
make_published.short_description = ugettext_lazy(u"Mark selected surveys as published")