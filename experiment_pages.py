from main import app


@app.route('/<experiment_name>', methods=['get'])
def see_exp(experiment_name):
    '''An experiment is selected from the main page and
    the result is given as a variable on this page. This
    page shows the files associated with this experiment'''

    return 'Experiment file view not implemented yet'
