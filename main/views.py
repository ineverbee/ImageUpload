from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
from .models import ImageModel
from .forms import AddImageForm, ChangeForm
from PIL import Image
import os
import requests
import shutil
import io
import base64

class value:
	name = ''

# Create your views here.
def homepage(request):
	obj = ImageModel.objects.all()
	context = {
		'images': obj,
	}
	return render(request, 'main/home.html', context)

def uploadpage(request):
	if request.method == 'POST':
		if request.POST.get('img') != '' and request.POST.get('url') == '':
			form = AddImageForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				obj = ImageModel.objects.get(id=ImageModel.objects.all().count())
				img = Image.open(os.path.join('static/', str(request.FILES['img'])))
				obj.width = img.width
				obj.height = img.height
				obj.save()
				return redirect('image', ImageModel.objects.all().count())

		elif request.POST.get('url') != '' and request.POST.get('img') == '':
			url = request.POST.get('url')
			try:
				value.name=url.split('/')[-1]
				validate_image_file_extension(value)
				resp = requests.get(url, stream=True)
				local_file = open(os.path.join('static/',url.split('/')[-1]), 'wb')
				resp.raw.decode_content = True
				shutil.copyfileobj(resp.raw, local_file)
				del resp
				local_file.close()
				img = Image.open(os.path.join('static/',url.split('/')[-1]))
				form = AddImageForm({'img':img, 'url':url, 'width':img.width, 'height':img.height})
				if form.is_valid():
					form.save()
					return redirect('image', ImageModel.objects.all().count())
			except ValidationError:
				form = AddImageForm()
				context = {
					'form': form,
					'error': 'Ошибка: неверная ссылка',
				}
				return render(request, 'main/upload.html', context)

		else:
			form = AddImageForm()
			context = {
				'form': form,
				'error': 'Ошибка: заполните одно из полей',
			}
			return render(request, 'main/upload.html', context)
	form = AddImageForm()
	context = {
		'form': form,
	}
	return render(request, 'main/upload.html', context)

def imagepage(request, index):
	img = ImageModel.objects.get(id=index)
	if request.method == 'POST':
		w = int(request.POST.get('width'))
		h = int(request.POST.get('height'))
		resized = False
		error = False
		if w == img.width and h != img.height:
			w = int(h*img.width/img.height)
			resized = resize(img, w, h)
		elif h == img.height and w != img.width:
			h = int(w*img.height/img.width)
			resized = resize(img, w, h)
		elif w == img.width and h == img.height:
			pass
		elif w == h*img.width/img.height:
			resized = resize(img, w, h)
		else:
			error = 'Ошибка: введите либо ширину, либо высоту, либо оба значения, сохраняя пропорции'
		form = ChangeForm({'width':int(w), 'height':int(h)})
		context = {
			'image': img,
			'resized': resized,
			'form': form,
			'error': error,
		}
		return render(request, 'main/image.html', context)
	
	form = ChangeForm({'width':img.width, 'height':img.height})
	context = {
		'image': img,
		'form': form,
	}
	return render(request, 'main/image.html', context)

def resize(img, w, h):
	image = Image.open(os.path.join('static/', str(img).split('/')[-1]))
	new = image.resize((w,h), resample=0, box=None)
	buffered = io.BytesIO()
	new.save(buffered, format="PNG")
	encoded = base64.b64encode(buffered.getvalue())
	return encoded.decode('utf-8')