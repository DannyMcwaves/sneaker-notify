
__all__ = ['check_availability', 'check_availability_yeezy']


def check_availability(container, item):
	common_name = [x['name'] for x in container]
	common_colors = [x['colors'] for x in container]

	data = item if item['name'] not in common_name and item['colors'] not in common_colors else []
	return data


def check_availability_yeezy(container, item):
	common_name = [x['name'] for x in container]

	data = item if item['name'] not in common_name else []
	return data
