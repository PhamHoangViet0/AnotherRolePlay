from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from decorators import *
from ajax_decorator import *
from models import *


@login_required
def filler(request):
    return HttpResponse(0)


@logged
def home_page(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render({}, request))


@logged
@have_ajax
def login_page(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render({}, request))


@logged
def logout_page(request):
    template = loader.get_template('forwarding.html')
    context = {
        "instant": True,
        "url": "../",
        "title": "Logout"
    }
    return HttpResponse(template.render(context, request))


@have_ajax
@logged
def guild_general_page(request):
    template = loader.get_template('guild_list.html')
    context = {}
    return HttpResponse(template.render(context, request))


@logged
def guild_page(request, guild_id):
    guild = Guilds.objects.get(pk=guild_id)
    template = loader.get_template('guild.html')
    context = {}
    return HttpResponse(template.render(context, request))


@have_ajax
@logged
def member_general_page(request, guild_id):
    guild = Guilds.objects.get(pk=guild_id)
    members = Members.objects.filter(guild_id=guild.guild_id)
    template = loader.get_template('member_list.html')
    context = {}
    return HttpResponse(template.render(context, request))


@logged
def member_page(request, guild_id, member_id):
    guild = Guilds.objects.get(pk=guild_id)
    member = Members.objects.get(pk=member_id)
    template = loader.get_template('member.html')
    context = {}
    return HttpResponse(template.render(context, request))


