from django.forms import ModelForm, ClearableFileInput, URLInput, NumberInput
from PIL import Image
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import ImageModel

class AddImageForm(ModelForm):

	class Meta:
		model = ImageModel
		fields = [
			'img',
			'url',
			'width',
			'height',
		]
		widgets = {
			'img': ClearableFileInput(),
			'url': URLInput(),
			'width': NumberInput(),
			'height': NumberInput(),
		}

class ChangeForm(ModelForm):

	class Meta:
		model = ImageModel
		fields = [
			'width',
			'height',
		]
		widgets = {
			'width': NumberInput(attrs={
					'min': '1',
					'step':'1',
				}),
			'height': NumberInput(attrs={
					'min': '1',
					'step':'1',
				})
		}
