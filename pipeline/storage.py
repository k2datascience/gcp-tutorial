import pickle
import sh
import subprocess

def archive_data(df, name, bucket):
    "Stores the data locally as a pickle file"

    pickle.dump(df, open('../data/{}.pkl'.format(name), 'wb'))

    return None
