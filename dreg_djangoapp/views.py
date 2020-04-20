import base64
import os
import json
import re

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.conf import settings

# Create your views here.
def hello_world(request):
    return render(request, "dynamic_djangoapp/hello.html")


def gbrowser_dreg(request, filelist):
    print("Dreg view is called....")

    #Check if the list of file is included in the request
    if filelist:
        #filelist = request.GET['filelist']
        data_root = settings.GATEWAY_DATA_STORE_DIR
        #data_root = "/var/www/portals/gateway-user-data/cornelldna/"
        http_protocol = request.scheme
        text_format = 'utf-8'
        json_data = []
        content = {}

        decoded_filelist = base64.b64decode(filelist).decode(text_format).split("\n")
        out_prefix = decoded_filelist[3]
        filelist_encoded = list()
        print(decoded_filelist)
        # input file 1
        content['type']= "bigwig"
        encoded_file = base64.b64encode(bytes(decoded_filelist[0] + decoded_filelist[1], text_format)).decode(text_format)
        content['url'] =  http_protocol + '://' + request.META['HTTP_HOST'] + '/dreg/gbfile/?file=' + encoded_file
        content['name'] = decoded_filelist[1]
        content['summarymethod'] = "max"
        content['colorpositive'] = "#C5000B"
        content['colornegative'] = "#0084D1"
        content['height'] = 100
        content['mode'] = "show"
        json_data.append(dict(content))

        # input file 2
        encoded_file = base64.b64encode(bytes(decoded_filelist[0] + decoded_filelist[2], text_format)).decode(text_format)
        content['url'] = http_protocol + '://' + request.META['HTTP_HOST'] + '/dreg/gbfile/?file=' + encoded_file
        content['name'] = decoded_filelist[2]
        json_data.append(dict(content))

        # out file 1
        encoded_file = base64.b64encode(bytes(decoded_filelist[0]+'ARCHIVE/out.dREG.infp.bw', text_format)).decode(text_format)
        content['url'] = http_protocol + '://' + request.META['HTTP_HOST'] + '/dreg/gbfile/?file=' + encoded_file
        content['name'] = "dREG Info. Sites:"
        content['mode'] = "show"
        content['colorpositive'] = "#B30086"
        content['colornegative'] = "#0000e5"
        content['backgroundcolor'] = "#ffffe5"
        content["height"] =  40
        content['fixedscale'] = dict({'min':0, 'max':1})
        json_data.append(dict(content))

        # out file 2
        encoded_file = base64.b64encode(bytes(decoded_filelist[0]+'ARCHIVE/out.dREG.peak.score.bw', text_format)).decode(text_format)
        content['url'] = http_protocol + '://' + request.META['HTTP_HOST'] + '/dreg/gbfile/?file=' + encoded_file
        content['name'] = "dREG Peak Calling:"
        content['mode'] = "show"
        content['colorpositive'] = "#B30086"
        content['colornegative'] = "#0000e5"
        content['backgroundcolor'] = "#ffffe5"
        content["height"] =  40
        content['fixedscale'] = dict({'min':0.2, 'max':1.0})
        json_data.append(dict(content))
        print(json_data)

        dump = json.dumps(json_data)
        dump_cleaned = re.sub(r'"(\w*?)": ', r'\1:', dump)
        #print(dump)
    return HttpResponse(dump_cleaned, content_type='text/plain')


def gbfile_download(request):
    #TODO: decode filenames and path from the url text
    text_format = 'utf-8'
    file_path = ""
    if 'file' in request.GET:
        file = request.GET['file']
        decoded_filepath = base64.b64decode(file).decode(text_format)
        filename = os.path.basename(decoded_filepath)
        data_root = settings.GATEWAY_DATA_STORE_DIR
        # Change this to test it locally
        #data_root = "/var/www/portals/gateway-user-data/cornelldna/"
        #data_root = settings.MEDIA_ROOT + '/dreg/'
        file_path = os.path.join(data_root, decoded_filepath.lstrip("/"))

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404
