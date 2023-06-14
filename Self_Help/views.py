from urllib.parse import urlparse, parse_qs

from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from Self_Help.email import send
from Self_Help.forms import NewProject, NewNote, EditProject, EditNote, AddUserToProject
from Self_Help.models import ErrorMessages, InfoMessages, Project, Note

USER_MODEL = get_user_model()


# Create your views here.


class StandardPage(View):
    def get(self, request):
        return redirect(reverse_lazy('home'))


class HomePage(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            return render(request, 'signin_home.html', context={
                'username': username,
            })
        return render(request, 'homepage.html')


class SignUp(View):
    def get(self, request):
        return render(request, "signup.html", context={
            'error_message': request.GET.get('error_message')})

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if USER_MODEL.objects.filter(username=username).exists():
            request.session['error_message'] = ErrorMessages.objects.get(name='wrong_username').full_text
            return redirect("{0}?error_message={1}".format(reverse_lazy('sign_up'),
                                                           ErrorMessages.objects.get(name='wrong_username').full_text))
        if USER_MODEL.objects.filter(email=email).exists():
            return redirect("{0}?error_message={1}".format(reverse_lazy('sign_up'),
                                                           ErrorMessages.objects.get(name='wrong_email').full_text))
        user = USER_MODEL.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False)
        send(subject=InfoMessages.objects.get(name='vrfy').full_text,
             to_email=user.email,
             template_name='verification_email.html',
             context={'subject': f"{InfoMessages.objects.get(name='hi').full_text} {user.username}.",
                      'link': reverse_lazy('verify_account', kwargs={
                          'uid': urlsafe_base64_encode(force_bytes(user.id)),
                          'token': default_token_generator.make_token(user)}),
                      'request': request})
        hi_message = f"{InfoMessages.objects.get(name='hi').full_text} {user.username}.\n" \
                     f" {InfoMessages.objects.get(name='acc_created').full_text} "
        return render(request, 'show_important_message.html', context={
            'important_message': hi_message})


def verify_account(request, uid, token):
    try:
        user = USER_MODEL.objects.get(id=urlsafe_base64_decode(uid))
    except (TypeError, ValueError, OverflowError, USER_MODEL.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        hi_message = f"{InfoMessages.objects.get(name='hi').full_text} {user.username}!\n " \
                     f"{InfoMessages.objects.get(name='acc_activated').full_text}"
        return render(request, 'show_important_message.html', context={
            'important_message': hi_message})
    return render(request, 'show_important_message.html', context={
        'important_message': ErrorMessages.objects.get(name='inv_token').full_text})


class SignIn(View):
    def get(self, request):
        error_message = request.GET.get('error_message')
        return render(request, "signin.html", context={
            'error_message': error_message})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(reverse_lazy('home'))
        elif user is None:
            return redirect("{0}?error_message={1}".format(reverse_lazy('sign_in'),
                                                           ErrorMessages.objects.get(name='wrong_signin').full_text))
        elif not user.is_active:
            return redirect("{0}?error_message={1}".format(reverse_lazy('sign_in'),
                                                           ErrorMessages.objects.get(name='acc_not_activ').full_text))
        else:
            return redirect("{0}?error_message={1}".format(reverse_lazy('sign_in'),
                                                           ErrorMessages.objects.get(
                                                               name='unexpected_error').full_text))


class SignOut(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('home'))


class ProjectsPage(View):
    def get(self, request):
        form = NewProject()
        my_projects = Project.objects.all().filter(host=request.user.id).order_by('id')
        other_projects = Project.objects.all().filter(users=request.user.id). \
            filter(~Q(host=request.user.id)).order_by('id')
        return render(request, "projects.html", context={
            'my_projects': my_projects,
            'other_projects': other_projects,
            'form': form
        })


def new_project_form(request, *args, **kwargs):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    form = NewProject()
    data = {}
    user = request.user
    if is_ajax:
        form = NewProject(request.POST)
        if form.is_valid():
            projects = Project.objects.filter(users=request.user).order_by('id')
            titles = [None] * len(projects)
            for i in range(len(projects)):
                titles[i] = projects[i].title
            project_title = form.cleaned_data.get('project_title')
            project_title = get_unused_title(project_title, titles)
            data['status'] = 'ok'
            data['success'] = True
            new_project = Project.objects.create(
                title=project_title,
            )
            new_project.save()
            new_project.host.add(user.id)
            new_project.users.add(user.id)
            return JsonResponse(data)
        elif form.cleaned_data.get('project_title') is None:
            data['success'] = False
            data['status'] = ErrorMessages.objects.get(name='empty_proj_title').full_text
            return JsonResponse(data)
        else:
            data['status'] = ErrorMessages.objects.get(name='unexpected_error').full_text
            data['success'] = False
            return JsonResponse(data)
    context = {
        'form': form
    }

    return render(request, 'projects.html', context)


def get_video_id(value):
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None


def new_note_form(request, *args, **kwargs):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    form = NewNote()
    data = {}
    if is_ajax:
        form = NewNote(request.POST)
        if form.is_valid():
            data['note_title'] = form.cleaned_data.get('note_title')
            data['note_text'] = form.cleaned_data.get('note_text')
            project = Project.objects.all().filter(slug=request.POST.get('project_slug')).get()
            notes = Note.objects.filter(project_id=project.id).order_by('id')
            vid_url = form.cleaned_data.get('vid_url')
            titles = [None] * len(notes)
            for i in range(len(notes)):
                titles[i] = notes[i].title
            data['note_title'] = get_unused_title(data['note_title'], titles)
            vid_id = None
            if vid_url:
                vid_id = get_video_id(vid_url)
                if vid_id is not None:
                    if len(vid_id) != 11 or vid_id is None:
                        data['success'] = False
                        data['status'] = ErrorMessages.objects.get(name='damaged_url').full_text
                        return JsonResponse(data)
            new_note = Note.objects.create(
                title=data['note_title'],
                text=data['note_text'],
                vid_id=vid_id
            )
            new_note.project_id.add(project.id)
            new_note.save()
            data['status'] = 'ok'
            data['success'] = True
            return JsonResponse(data)
        elif form.cleaned_data.get('note_title') is None:
            data['success'] = False
            data['status'] = ErrorMessages.objects.get(name='empty_note_title').full_text
            return JsonResponse(data)
        else:
            data['status'] = ErrorMessages.objects.get(name='unexpected_error').full_text
            data['success'] = False
            return JsonResponse(data)
    context = {
        'form': form
    }

    return render(request, 'project_detail.html', context)


def switch_notes(current_note_title, notes):
    if notes:
        if current_note_title == 'None' or current_note_title is None or current_note_title == '':
            return notes.first()
        return notes.filter(title=current_note_title).order_by('id').get()
    else:
        return None


class ProjectDetailPage(View):
    def get(self, request, **kwargs):
        project_slug = request.GET.get('project_slug')
        current_note_title = request.GET.get('current_note_title')
        project = Project.objects.all().filter(users=request.user.id, slug=project_slug).get()
        users = project.users.filter(~Q(id=request.user.id))
        form_edit_note = EditNote()
        form_new_note = NewNote()
        form_project = EditProject()
        form_add_user_to_project = AddUserToProject()
        notes = Note.objects.all().filter(project_id=project.id).order_by('id')
        labels = [InfoMessages.objects.get(name='note_performed').full_text,
                  InfoMessages.objects.get(name='note_unperformed').full_text]
        done_notes = int(notes.filter(is_done=True).count())
        not_done_notes = int(notes.filter(is_done=False).count())
        data = [done_notes, not_done_notes]
        current_note = switch_notes(current_note_title, notes)
        context = {'notes': notes,
                   'form_new_note': form_new_note,
                   'form_edit_note': form_edit_note,
                   'form_project': form_project,
                   'form_add_user_to_project': form_add_user_to_project,
                   'project': project,
                   'current_note': current_note,
                   'current_user': request.user,
                   'added_users': users,
                   'labels': labels,
                   'data': data}
        if request.GET.get('vid_err') == 'true':
            context['error_message'] = ErrorMessages.objects.get(name='damaged_url').full_text
        return render(request, "project_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        new_note_title = request.POST.get('new_note_title')
        new_note_text = request.POST.get('new_note_text')
        new_vid_url = request.POST.get('new_vid_url')
        note = Note.objects.get(id=request.POST.get('note_id'))
        new_vid_id = None
        if new_vid_url:
            new_vid_id = get_video_id(new_vid_url)
            if new_vid_id is not None:
                if len(new_vid_id) != 11:
                    return redirect(
                        "{0}?project_slug={1}&current_note_title={2}&vid_err=true".format(
                            reverse_lazy('project_detail'),
                            request.POST.get('project_slug'),
                            note.title))
        notes = Note.objects.filter(project_id=request.POST.get('project_id')).order_by('id')
        titles = [None] * len(notes)
        for i in range(len(notes)):
            titles[i] = notes[i].title
        k = 1
        while True:
            if note.title == new_note_title:
                break
            if new_note_title not in titles:
                break
            if (k - 1) > 0:
                new_note_title = new_note_title[:len(new_note_title) - len(str(k - 1))]
            new_note_title = new_note_title + str(k)
            k += 1
        note.title = new_note_title
        note.text = new_note_text
        if new_vid_id is not None:
            note.vid_id = new_vid_id
        note.save()
        return redirect("{0}?project_slug={1}&current_note_title={2}".format(reverse_lazy('project_detail'),
                                                                             request.POST.get('project_slug'),
                                                                             note.title))


def test_video(request):
    return render(request, 'project_detail.html')


def delete_project(request):
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        project = Project.objects.filter(slug=request.POST.get('project_slug')).get()
        project.delete()
        data['success'] = True
        return JsonResponse(data)
    data['status'] = ErrorMessages.objects.get(name='unexpected_error').full_text
    data['success'] = False
    return JsonResponse(data)


def delete_note(request):
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        note = Note.objects.filter(slug=request.POST.get('note_slug')).get()
        note.delete()
        data['success'] = True
        return JsonResponse(data)
    data['status'] = ErrorMessages.objects.get(name='unexpected_error').full_text
    data['success'] = False
    return JsonResponse(data)


def get_unused_title(new_title, titles):
    j = 1
    while True:
        if new_title not in titles:
            return new_title
        if (j - 1) > 0:
            new_title = new_title[:len(new_title) - len(str(j - 1))]
        new_title = new_title + str(j)
        j += 1


def edit_project(request):
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    form = EditProject()
    if is_ajax:
        form = EditProject(request.POST)
        if form.is_valid():
            project = Project.objects.filter(slug=request.POST.get('project_slug')).get()
            projects = Project.objects.filter(users=request.user).order_by('id')
            titles = [None] * len(projects)
            for i in range(len(projects)):
                titles[i] = projects[i].title
            new_project_title = form.cleaned_data.get('new_project_title')
            project.title = get_unused_title(new_project_title, titles)
            project.save()
            data['success'] = True
            data['new_project_title'] = project.title
            return JsonResponse(data)
        elif form.cleaned_data.get('new_project_title') is None:
            data['success'] = False
            data['status'] = ErrorMessages.objects.get(name='empty_proj_title').full_text
            return JsonResponse(data)
        else:
            data['status'] = ErrorMessages.objects.get(name='unexpected_error').full_text
            data['success'] = False
            return JsonResponse(data)
    else:
        context = {
            'form': form
        }
        return render(request, 'project_detail.html', context)


def note_is_done(request):
    note = Note.objects.filter(id=request.GET.get('note_id')).get()
    note.is_done = True
    note.save()
    return redirect("{0}?project_slug={1}&current_note_title={2}".format(reverse_lazy('project_detail'),
                                                                         request.GET.get('project_slug'),
                                                                         note.title))


def note_is_not_done(request):
    note = Note.objects.filter(id=request.GET.get('note_id')).get()
    note.is_done = False
    note.save()
    return redirect("{0}?project_slug={1}&current_note_title={2}".format(reverse_lazy('project_detail'),
                                                                         request.GET.get('project_slug'),
                                                                         note.title))


def still_in_progress(request):
    return render(request, 'still_in_progress.html')


def add_user_to_project(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    form = AddUserToProject()
    data = {}
    if is_ajax:
        form = AddUserToProject(request.POST)
        if form.is_valid():
            project = Project.objects.filter(slug=request.POST.get('project_slug')).get()
            try:
                user_being_added = USER_MODEL.objects.filter(email=request.POST.get('new_user_email')).get()
            except ObjectDoesNotExist:
                data['success'] = False
                data['status'] = ErrorMessages.objects.get(name='no_such_user').full_text
                return JsonResponse(data)
            user_being_added_projects = Project.objects.filter(users=user_being_added).order_by('id')
            if user_being_added in user_being_added_projects:
                data['success'] = False
                data['status'] = ErrorMessages.objects.get(name='user_already_in').full_text
                return JsonResponse(data)
            project.users.add(user_being_added)
            project.save()
            send(subject=InfoMessages.objects.get(name='added_to_project').full_text,
                 to_email=user_being_added.email,
                 template_name='added_to_project_email.html',
                 context={'subject': f"{InfoMessages.objects.get(name='hi').full_text} {user_being_added.username}.",
                          'link': f"{reverse_lazy('project_detail')}?project_slug={project.slug}",
                          'project_title': project.title,
                          'request': request})
            data['success'] = True
            return JsonResponse(data)
        elif form.cleaned_data.get('new_user_email') is None:
            data['success'] = False
            data['status'] = ErrorMessages.objects.get(name='empty_user_email').full_text
            return JsonResponse(data)
        else:
            data['status'] = ErrorMessages.objects.get(name='unexpected_error').full_text
            data['success'] = False
            return JsonResponse(data)
    else:
        context = {
            'form': form
        }
        return render(request, 'project_detail.html', context)


def delete_user_from_project(request):
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        project = Project.objects.filter(slug=request.POST.get('project_slug')).get()
        user_being_removed = project.users.filter(email=request.POST.get('user_email')).get()
        project.users.remove(user_being_removed)
        project.save()
        send(subject=InfoMessages.objects.get(name='deleted_from_project').full_text,
             to_email=user_being_removed.email,
             template_name='deleted_from_project_email.html',
             context={'subject': f"{InfoMessages.objects.get(name='hi').full_text} {user_being_removed.username}.",
                      'project_title': project.title,
                      'request': request})
        data['success'] = True
        return JsonResponse(data)
    data['status'] = ErrorMessages.objects.get(name='unexpected_error').full_text
    data['success'] = False
    return JsonResponse(data)
