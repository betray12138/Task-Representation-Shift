import json
import datetime
import os
from tensorboardX import SummaryWriter
from torchkit import pytorch_utils as ptu

class TBLogger:
    def __init__(self):

        # initialise name of the file (optional(prefix) + seed + start time)
        self.output_name ='model' + datetime.datetime.now().strftime('%d_%m_%H_%M_%S')


        log_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        log_dir = os.path.join(log_dir, 'logs')

        if not os.path.exists(log_dir):
            try:
                os.mkdir(log_dir)
            except:
                dir_path_head, dir_path_tail = os.path.split(log_dir)
                if len(dir_path_tail) == 0:
                    dir_path_head, dir_path_tail = os.path.split(dir_path_head)
                os.mkdir(dir_path_head)
                os.mkdir(log_dir)

        # create a subdirectory for the environment
        env_dir = os.path.join(log_dir, 'model')

        if not os.path.exists(env_dir):
            os.makedirs(env_dir)


        # finally, get full path of where results are stored
        self.full_output_folder = os.path.join(env_dir, self.output_name)

        self.writer = SummaryWriter(self.full_output_folder)

        print('logging under', self.full_output_folder)
