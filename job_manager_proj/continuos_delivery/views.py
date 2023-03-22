from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import HttpResponse

import git


class Webhook(View):
    def post(self):
        repo = git.Repo(settings.PATH_OF_GITHUB)
        origin = repo.remotes.origin
        origin.pull()
        return HttpResponse("Updated PythonAnywhere successfully", status=200)
