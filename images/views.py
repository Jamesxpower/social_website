from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ImageCreateForm
from .models import Image

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()

            messages.success(request=request, message='照片存檔成功')

            # redirect to new created item detail view
            return redirect(to=new_image.get_absolute_url())

    else:
        form = ImageCreateForm(data=request.GET)

    return render(request=request,
                  template_name="images/image/create.html",
                  context={'section': 'images',
                           'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request=request, template_name='images/image/detail.html',
                  context={'section': 'images', 'image': image})

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)

            return JsonResponse(data={'status': 'OK'})
        except Image.DoesNotExist:
            pass

    return JsonResponse(data={'status': 'error'})