from django.shortcuts import render, get_object_or_404, Http404
from .models import Files, FileViewing, ViewingPermissionToken
from django.contrib.auth.decorators import login_required
from django.utils.six.moves import range
from django.utils import timezone
from datetime import timedelta
import cStringIO as StringIO
from django.http import *
import csv
import magic


# Create your views here.
@login_required
def displayfile(request, slug):
	file = get_object_or_404(Files, slug=slug)
	# generate file loading permission token
	token = ViewingPermissionToken.objects.create(user=request.user, file=file)
	# check if user has viewed this file in the last /x/ hours
	# timeframe = timezone.now() - timedelta(hours=24)
	timeframe = timezone.now().replace(hour=0, minute=0, second=0, microsecond=1)
	print timezone.now()-timedelta(hours = 4)
	print timeframe
	print timezone.now() - timedelta(hours=24)

	fileviewing = FileViewing.objects.filter(timestamp__gte=timeframe, file=file, user=request.user).first()
	if fileviewing is None:
		fileviewing = FileViewing.objects.create(file=file, user=request.user)

	# get filetype...
	filetype = str(file.extenstion())

	# generate context
	context = {
		"fileviewing": fileviewing,
		"token": token
	}

	if filetype == ".mp4":
		return render(request, 'display/generic.html', context)
	else:
		return render(request, 'display/generic_pdf.html', context)

@login_required
def getFileViaToken(request, uuid):
	token = get_object_or_404(ViewingPermissionToken, id=uuid)
	file = token.file
	timeframe = timezone.now() - timedelta(seconds=5)
	if token.timestamp < timeframe:
		token.delete()
		raise Http404
	else:
		token.delete()
		return FileResponse(file.file)



class Echo(object):
	"""An object that implements just the write method of the file-like
	interface.
	"""
	def write(self, value):
		"""Write the value by returning it, instead of storing in a buffer."""
		return value

@login_required
def getFileAdmin(request,id):
	"""A view that streams a large CSV file."""
	# Generate a sequence of rows. The range is based on the maximum number of
	# rows that can be handled by a single sheet in most spreadsheet
	# applications.
	file = get_object_or_404(Files, pk = id)
	fileviewing = FileViewing.objects.filter(file = file)
	rows = [["File Title",file.title],['User Name', 'Time Stamp', 'Seconds spend']]
	rows.extend([[fv.user, (fv.timestamp-timedelta(hours = 4)).strftime("%Y-%m-%d %H:%M:%S"), fv.seconds_viewed] for fv in fileviewing])
	pseudo_buffer = Echo()
	writer = csv.writer(pseudo_buffer)
	response = StreamingHttpResponse((writer.writerow(row) for row in rows),
									 content_type="text/csv")
	response['Content-Disposition'] = 'attachment; filename="'+file.slug+'-report.csv"'
	return response

@login_required
def posttime(request):
	if request.POST:
		fileviewing = get_object_or_404(FileViewing, pk=request.POST.get("id"))
		if fileviewing.user!=request.user:
			raise Http404
		else:
			fileviewing.seconds_viewed += 1
			fileviewing.save()
	return HttpResponse(fileviewing.id)