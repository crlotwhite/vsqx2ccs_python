import mimetypes
import os
from os.path import join

from django.http import HttpResponse
from django.shortcuts import render

from vsqx2ccs.settings import MEDIA_ROOT
from .forms import UploadFileForm

from ccs.from_vsqx import from_vsqx


# Create your views here.
def test(request):
    def get_xml_tree(xml_str):
        from xml.etree.ElementTree import fromstring
        return fromstring(xml_str)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            xml_string = request.FILES['vocal_sequence_file'].read().decode("utf-8")
            tree = get_xml_tree(xml_string)
            file_name = request.COOKIES['csrftoken'] + '^' + request.FILES['vocal_sequence_file'].name
            is_hiragana = bool(int(request.POST.get('is_hiragana')))

            # process file
            from_vsqx(file_name, tree, is_hiragana)

            # post process; make file name, path
            save_file_name = file_name.split('.')[0] + '.ccs'
            mime_type, _ = mimetypes.guess_type(save_file_name)
            save_file_path = join(join(MEDIA_ROOT, 'files'), save_file_name)

            # make HttpResponse
            response = HttpResponse(
                open(save_file_path, 'r', encoding='utf-8'), content_type=mime_type
            )
            response['Content-Disposition'] = f'attachment; filename={save_file_name.split("^")[1]}'
            os.remove(save_file_path)
            return response
    else:
        language = request.GET.get('lang')
        if language == 'en':
            translated_strings = {
                'sub_title': 'File converter for Cevio users',
                'convert': 'Convert',
                'just_convert': 'Just Convert',
                'auto_hiragana': 'Change to Hiragana',
            }
        elif language == 'jp':
            translated_strings = {
                'sub_title': 'Cevioユーザーのためのファイルコンバータ',
                'convert': 'ファイルを変換する',
                'just_convert': '変換するだけ',
                'auto_hiragana': 'ひらがなに変更',
            }
        elif language == 'kr':
            translated_strings = {
                'sub_title': '체비오 사용자를 위한 파일 변환기',
                'convert': '변환 하기',
                'just_convert': '그대로 변환하기',
                'auto_hiragana': '히라가나로 변환하기',
            }
        else:
            translated_strings = {
                'sub_title': '체비오 사용자를 위한 파일 변환기',
                'convert': '변환 하기',
                'just_convert': '그대로 변환하기',
                'auto_hiragana': '히라가나로 변환하기',
            }
        return render(request, 'index.html', translated_strings)

