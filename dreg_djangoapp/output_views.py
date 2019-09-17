from django.template.loader import render_to_string
from airavata.model.application.io.ttypes import DataType
from airavata.model.data.replica.ttypes import (
    ReplicaLocationCategory,
)
from django.conf import settings
from urllib.parse import urlparse, urlencode
import base64


class DregGenomeBrowserViewProvider:
    display_type = 'html'
    name = 'dREG Genome Browser'
    # Optionally provide path to a file to test with when data isn't available
    # locally
    # fixture_output_file = ""

    def generate_data(self, request, experiment_output, experiment, output_file=None):
        #Changing test experiment as all files are not present in the provided experiment
        #experiment =  request.airavata_client.getExperiment(request.authz_token, 'Clone_of_dREG_peak_calling_on_Aug_9,_2019_10:30_AM_2a27c8d8-6985-4795-9bd3-f6d28619c57f')

        exp_data_dir = experiment.userConfigurationData.experimentDataDir
        data_root = settings.GATEWAY_DATA_STORE_DIR
        #data_root = "/var/www/portals/gateway-user-data/cornelldna/"

        #remove data root from the path so that gbfile and gbrowser views can
        #read the data root from settings
        if exp_data_dir.startswith(data_root):
            exp_data_dir = exp_data_dir.replace(data_root, "", 1)

        param_prefix = "out"

        filelist = ''
        if ( len(experiment.experimentInputs) > 0):
            for input in experiment.experimentInputs:
                if(input.type == DataType.URI):
                    data_product_model = request.airavata_client.getDataProduct(
                                    request.authz_token, input.value)
                    for rp in data_product_model.replicaLocations:
                        if rp.replicaLocationCategory == ReplicaLocationCategory.GATEWAY_DATA_STORE:
                            current_ouput_path = rp.filePath
                            path = urlparse(current_ouput_path).path.replace(data_root+exp_data_dir,"",1).replace('/',"",1)
                            break

                    filelist = filelist + path + "\n"
                else:
                    filelist = filelist + input.value + "\n"

        filelist = exp_data_dir + "/\n" + filelist
        filelist = filelist + param_prefix + "\n";

        encoded_filelist = base64.b64encode(bytes(filelist, 'utf-8')).decode('utf-8')

        #build url
        http_protocol = request.scheme

        gbURL = "http://epigenomegateway.wustl.edu/browser/?datahub=" + \
                        http_protocol + "://" + request.META['HTTP_HOST'] +\
                        "/dreg/gbrowser/?filelist=" + encoded_filelist + "&genome="
        js = 'alert("Js is executed")';
        return {
            'output': render_to_string(
                'dreg_djangoapp/dreg_genome_browser.html', {'gbURL' : gbURL}),
            'js': "/static/dreg/gbrowser.js"
            }
