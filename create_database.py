from db_models import *

db.create_tables([Experiment, WatchedFolder, Settings,
                  Scripts, Files, ExperimentScripts])
