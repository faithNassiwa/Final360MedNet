from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Post, Comment
from userprofile.models import Doctor
from .forms import PostForm, CommentForm, PhotoForm
from django.views.generic.edit import DeleteView, ModelFormMixin
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from event.models import Event
from medicalcase.models import MedicalCase
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Context
from django.conf import settings

home = settings.SITE_HOST


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    success_url = '/feed/'

    def form_valid(self, form):
        form.instance.doctor = Doctor.objects.get(user=self.request.user)
        form.instance.save()
        return super(PostCreate, self).form_valid(form)


class Posts(ListView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts')

    def render_to_response(self, context, **response_kwargs):
        top_five_latest_medical_cases = MedicalCase.objects.order_by('-created_at')[:5]
        top_five_latest_events = Event.objects.order_by('-created_on')[:5]
        top_five_latest_posts = Post.objects.order_by('-created_on')[:5]
        top_five_latest_medical_professionals = Doctor.objects.order_by('-created_at')[:5]


        # get events
        all_events = Event.objects.all()
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        month_events = {}
        ii = 1
        for month in months:
            month_events[month] = Event.objects.filter(start__month=ii).count()
            ii += 1

        context = {'top_five_latest_medical_cases': top_five_latest_medical_cases,
                   'top_five_latest_events': top_five_latest_events, 'all_events': all_events,
                   'month_events': month_events, 'top_five_latest_posts':top_five_latest_posts,
                   'top_five_latest_medical_professionals': top_five_latest_medical_professionals}

        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
                                   using=self.template_engine)


class PostList(ListView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts')
    template_name = 'post/posts_list.html'

    def render_to_response(self, context, **response_kwargs):
        all_posts = Post.objects.order_by('-created_at').all()
        paginator = Paginator(all_posts, 2)
        page = self.request.GET.get('page', 1)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        top_five_latest_medical_cases = MedicalCase.objects.order_by('-created_at')[:5]
        top_five_latest_events = Event.objects.order_by('-created_on')[:5]
        top_five_latest_posts = Post.objects.order_by('-created_on')[:5]
        top_five_latest_medical_professionals = Doctor.objects.order_by('-created_at')[:5]


        # get events
        all_events = Event.objects.all()
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        month_events = {}
        ii = 1
        for month in months:
            month_events[month] = Event.objects.filter(start__month=ii).count()
            ii += 1

        context = {'all_posts': all_posts, 'top_five_latest_medical_cases': top_five_latest_medical_cases,
                   'top_five_latest_events': top_five_latest_events, 'all_events': all_events,
                   'month_events': month_events, 'top_five_latest_posts':top_five_latest_posts,
                   'top_five_latest_medical_professionals': top_five_latest_medical_professionals}

        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
                                   using=self.template_engine)


class PostDetail(ModelFormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def comments(self):
        return Comment.objects.filter(post=Post.objects.get(pk=self.object.pk)).all().order_by('-created_at')


@login_required
def post_comment_add_view(request, pk):
    form = CommentForm(request.POST or None)

    if form.is_valid() and pk:
        form.instance.doctor = Doctor.objects.get(user=request.user)
        form.instance.post = Post.objects.get(pk=pk)
        form.save()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.doctor = Doctor.objects.get(user=request.user)
            comment.save()
            return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': post.pk}))
    else:
        form = CommentForm()
    return render(request, 'post/add_comment_to_post.html', {'form': form})


@login_required
def add_image_on_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.post = post
            image.doctor = Doctor.objects.get(user=request.user)
            image.save()
            return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))


@login_required
def send_top_five_discussions_weekly(request):
    subject_discussion = Post.objects.last()
    weekly_top_five_discussions = Post.weekly_top_five_discussions()
    registered_doctors = Doctor.objects.all()
    for registered_doctor in registered_doctors:
        context = Context({
            'weekly_top_five_discussions': weekly_top_five_discussions,
            'doctor': registered_doctor,
            'domain': home,
        })
        Post.send_weekly_top_five_discussions(subject_discussion, context, registered_doctor)
        # registered_doctors_mailing_list.append(registered_doctor.user.email) ## might need to accesss name of the docs
        # current_site = get_current_site(request)
        # subject = subject_medical_case.title
        # message = render_to_string('medicalcase/medical_case_email_update.html', {
        #     'weekly_five_medical_cases': weekly_five_medical_cases,
        #     'weekly_top_five_discussions': weekly_top_five_discussions,
        #     'doctor': registered_doctor,
        #     'domain': current_site.domain,
        #
        # })
        # to_email1 = registered_doctor.user.email
        # email = EmailMessage(subject, message, to=[to_email1])
        # email.content_subtype = "html"
        # email.send()

    return HttpResponse("Successfully sent")


