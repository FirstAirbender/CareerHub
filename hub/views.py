from django.shortcuts import render, get_object_or_404, Http404
from django.http import FileResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import Files, FileViewing, ViewingPermissionToken

# Create your views here.
# @login_required
def displayfile(request, slug):
	file = get_object_or_404(Files, slug=slug)
	# generate file loading permission token
	token = ViewingPermissionToken.objects.create(user=request.user, file=file)
	# check if user has viewed this file in the last /x/ hours
	timeframe = timezone.now() - timedelta(hours=24)
	fileviewing = FileViewing.objects.filter(timestamp__lte=timeframe, file=file, user=request.user).first()
	if fileviewing is None:
		fileviewing = FileViewing.objects.create(file=file, user=request.user)

	# get filetype...
	filetype = None

	# generate context
	context = {
		"fileviewing": fileviewing,
		"token": token
	}

	if filetype == "video":
		pass
	else:
		return render(request, 'display/generic.html', context)


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

def posttime(request):
	if request.POST:
		fileviewing = get_object_or_404(FileViewing, pk=request.POST.get("id"))
		if fileviewing.user!=request.user:
			raise Http404
		else:
			fileviewing.seconds_viewed = fileviewing.seconds_viewed + 1
			fileviewing.save()
	return HttpResponse('success')