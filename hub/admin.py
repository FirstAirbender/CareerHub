from django.contrib import admin
from .models import Files, FileViewing
from django.shortcuts import render, get_object_or_404, Http404
from django.http import FileResponse, HttpResponse

# Register your models here.
class FilesAdmin(admin.ModelAdmin):
	list_display = ("title", "document_url", "download_report")
	# fields = ("title", "slug", "file", "document_url", "download_report")
	fields = ("title", "slug", "file")
	readonly_fields = ("document_url", "download_report",)
	prepopulated_fields = {"slug": ("title",) }
	def document_url(self, obj):
		return '<a href="/files/%s/" target = "_blank">Link to Document</a>' % obj.slug
	def download_report(self, obj):
		return '<button><a download="file" href="/files/getfile/%s/">Download</a></button>' % obj.id
	document_url.allow_tags = True
	download_report.allow_tags = True



admin.site.register(Files, FilesAdmin)