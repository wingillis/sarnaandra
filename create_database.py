from db_models import *

# only needed when first running sarnaandra
db.create_tables([Experiment, WatchedFolder, Settings,
                  Scripts, Files, ExperimentScripts])
