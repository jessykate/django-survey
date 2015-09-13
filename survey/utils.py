from django.core.exceptions import ValidationError

def validate_list(value):
	"""
	takes a text value and verifies that there is at least one comma
	"""
	values = value.split(',')
	if len(values) < 2:
		raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")
