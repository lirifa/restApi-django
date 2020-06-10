# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
