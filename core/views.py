from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView , DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import FormView
from .models import *
from .forms import *



# Create your views here.

class Home(TemplateView):
    template_name = "home.html"

class SchoolCreateView(CreateView):
    model = School
    template_name = "school/school_form.html"
    fields = ['title', 'description']
    success_url = reverse_lazy('school_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SchoolCreateView, self).form_valid(form)

class SchoolListView(ListView):
    model = School
    template_name = 'school/school_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(SchoolListView, self).get_context_data(**kwargs)
        user_votes = School.objects.filter(vote__user=self.request.user)
        context['user_votes'] = user_votes
        return context

class SchoolDetailView(DetailView):
    model = School
    template_name = 'school/school_detail.html'

    def get_context_data(self, **kwargs):
        context = super (SchoolDetailView, self).get_context_data(**kwargs)
        school = School.objects.get(id=self.kwargs['pk'])
        reviews = Review.objects.filter(school=school)
        context['reviews'] = reviews
        user_reviews = Review.objects.filter(school=school, user=self.request.user)
        context['user_reviews'] = user_reviews
        user_votes = Review.objects.filter(vote__user=self.request.user)
        context['user_votes'] = user_votes
        return context

class SchoolUpdateView(UpdateView):
    model = School
    template_name = 'school/school_form.html'
    fields = ['title', 'description']

    def get_object(self, *args, **kwargs):
          object = super(SchoolUpdateView, self).get_object(*args, **kwargs)
          if object.user != self.request.user:
              raise PermissionDenied()
          return object

class SchoolDeleteView(DeleteView):
    model = School
    template_name = 'school/school_confirm_delete.html'
    success_url = reverse_lazy('school_list')

    def get_object(self, *args, **kwargs):
          object = super(SchoolDeleteView, self).get_object(*args, **kwargs)
          if object.user != self.request.user:
              raise PermissionDenied()
          return object

class ReviewCreateView(CreateView):
    model = Review
    template_name = "review/review_form.html"
    fields = ['text']

    def get_success_url(self):
        return self.object.school.get_absolute_url()

    def form_valid(self, form):
          school = School.objects.get(id=self.kwargs['pk'])
          if Review.objects.filter(school=school, user=self.request.user).exists():
            raise PermissionDenied()
          form.instance.user = self.request.user
          form.instance.school = School.objects.get(id=self.kwargs['pk'])
          return super(ReviewCreateView, self).form_valid(form)

class ReviewUpdateView(UpdateView):
    model = Review
    pk_url_kwarg = 'review_pk'
    template_name = 'review/review_form.html'
    fields = ['text']

    def get_success_url(self):
        return self.object.school.get_absolute_url()

        def get_object(self, *args, **kwargs):
          object = super(ReviewUpdateView, self).get_object(*args, **kwargs)
          if object.user != self.request.user:
              raise PermissionDenied()
          return object



class ReviewDeleteView(DeleteView):
    model = Review
    pk_url_kwarg = 'review_pk'
    template_name = 'review/review_confirm_delete.html'

    def get_success_url(self):
        return self.object.school.get_absolute_url()
    def get_object(self, *args, **kwargs):
          object = super(ReviewDeleteView, self).get_object(*args, **kwargs)
          if object.user != self.request.user:
            raise PermissionDenied()
            return

class VoteFormView(FormView):
    form_class = VoteForm

    def form_valid(self, form):
      user = self.request.user
      school = School.objects.get(pk=form.data["school"])
      try:
        review = Review.objects.get(pk=form.data["review"])
        prev_votes = Vote.objects.filter(user=user, review=review)
        has_voted = (prev_votes.count()>0)
        if not has_voted:
            Vote.objects.create(user=user, review=review)
        else:
            prev_votes[0].delete()
        return redirect(reverse('school_detail', args=[form.data["school"]]))
      except:
        prev_votes = Vote.objects.filter(user=user, school=school)
        has_voted = (prev_votes.count()>0)
        if not has_voted:
            Vote.objects.create(user=user, school=school)
        else:
            prev_votes[0].delete()
      return redirect('school_list')

class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'user/user_detail.html'
    context_object_name = 'user_in_view'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user_in_view = User.objects.get(username=self.kwargs['slug'])
        schools = School.objects.filter(user=user_in_view)
        context['schools'] = schools
        reviews = Review.objects.filter(user=user_in_view)
        context['reviews'] = reviews
        return context



class UserUpdateView(UpdateView):
    model = User
    slug_field = "username"
    template_name = "user/user_form.html"
    fields = ['email', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('user_detail', args=[self.request.user.username])

    def get_object(self, *args, **kwargs):
        object = super(UserUpdateView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

class UserDeleteView(DeleteView):
    model = User
    slug_field = "username"
    template_name = 'user/user_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('logout')

    def get_object(self, *args, **kwargs):
        object = super(UserDeleteView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

    def delete(self, request, *args, **kwargs):
        user = super(UserDeleteView, self).get_object(*args)
        user.is_active = False
        user.save()
        return redirect(self.get_success_url())


class SearchSchoolListView(SchoolListView):
    def get_queryset(self):
        incoming_query_string = self.request.GET.get('query','')
        return School.objects.filter(title__icontains=incoming_query_string)


