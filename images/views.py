from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

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


