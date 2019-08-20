from django.template.loader import render_to_string


class DregGenomeBrowserViewProvider:
    display_type = 'html'
    name = 'dREG Genome Browser'
    # Optionally provide path to a file to test with when data isn't available
    # locally
    # fixture_output_file = ""

    def generate_data(self, experiment_output, experiment, output_file=None):
        return {
            'output': render_to_string(
                'dreg_djangoapp/dreg_genome_browser.html')
        }
