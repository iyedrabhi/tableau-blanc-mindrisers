from django.shortcuts import render


def test_notifications(request):
	"""Serve a simple integrated test page for notifications.

	This view is intentionally minimal and does not modify any business logic.
	"""
	return render(request, 'test_notifications.html')
