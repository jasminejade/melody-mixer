from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

from model.core import *
from model.components import *
from model.input_data import *
from model.config import *
from pianoroll_mysong import run_piano_roll
from npy2mid import run_npy_2_mid


def run_main(inputName):
    inputName=inputName

    # run preprocessing pianoroll_mysong.py
    run_piano_roll(inputName)


    """ Create TensorFlow Session """

    t_config = TrainingConfig

    os.environ['CUDA_VISIBLE_DEVICES'] = t_config.gpu_num
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    downloadReady=False

    with tf.Session(config=config) as sess:

        # === Prerequisites ===
        # Step 1 - Initialize the training configuration
        t_config = TrainingConfig
        t_config.exp_name = r'./exps/nowbar_hybrid'

        # Step 2 - Select the desired model
        model = NowbarHybrid(NowBarHybridConfig)

        # Step 3 - Initialize the input data object
        input_data = InputDataNowBarHybrid(model)


        # Step 5 - Initialize a museGAN object
        musegan = MuseGAN(sess, t_config, model)

        # === Load a Pretrained Model ===
        musegan.load(musegan.dir_ckpt)

        # === Generate Samples ===
        path_x_test_bar = r'./constantFiles/x_bar_chroma.npy'
        # only replace this part ...y_bar_chroma_name
        path_y_test_bar = r'./preFiles_'+inputName+'/'+inputName+'y_bar_chroma_test.npy'
        input_data.add_data_test(path_x_test_bar, path_y_test_bar, key='test')
        print('--------------Start arrangement generation !!--------------')
        musegan.gen_test(input_data, is_eval=True)
        downloadReady=True
        print('--------------arrangement completed !!--------------')

        # run postprocessing npy2mid.py
        run_npy_2_mid(inputName)
        print("ALL DONE!!!!!!!")
        return inputName


# inputName = 'humanlifeleadsheet'
# run_main(inputName)