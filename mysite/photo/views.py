from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from photo.models import Album, Photo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin
from photo.forms import PhotoInlineFormset


class AlbumLV(ListView):
    model = Album
    template_name = "photo/album_list.html"

class AlbumDV(DetailView):
    model = Album
    template_name = "photo/album_detail.html"

class PhotoDV(DetailView):
    model = Photo
    template_name = "photo/photo_detail.html"

class PhotoCV(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = "photo/photo_form.html"
    fields = ('album', 'title', 'image', 'description')
    success_url = reverse_lazy('photo:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PhotoChangeLV(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_change_list.html'

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)

class PhotoUV(OwnerOnlyMixin, UpdateView):
    model = Photo
    template_name = "photo/photo_form.html"
    fields = ('album', 'title', 'image', 'description')
    success_url = reverse_lazy('photo:index')

class PhotoDelV(OwnerOnlyMixin, DeleteView):
    model = Photo
    template_name = "photo/photo_confirm_delete.html"
    success_url = reverse_lazy('photo:index')

#--- Change-list/Delete for Album
class AlbumChangeLV(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'photo/album_change_list.html'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)

class AlbumDelV(OwnerOnlyMixin, DeleteView):
    model = Album
    template_name = "photo/album_confirm_delete.html"
    success_url = reverse_lazy('photo:index')

#--- (InlineFormSet) Create/Update for Album
class AlbumPhotoCV(LoginRequiredMixin, CreateView):
    model = Album
    template_name = "photo/album_form.html"
    fields = ('name', 'description')
    success_url = reverse_lazy('photo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoInlineFormset(self.request.POST, self.request.FILES)
        else:
            context['formset'] = PhotoInlineFormset()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        for photoform in formset:
            photoform.instance.owner = self.request.user
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class AlbumPhotoUV(OwnerOnlyMixin, UpdateView):
    model = Album
    template_name = "photo/album_form.html"
    fields = ('name', 'description')
    success_url = reverse_lazy('photo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoInlineFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = PhotoInlineFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

