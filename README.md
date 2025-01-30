# Reining Task Representation Shift

## 1. Prepare for the dataset
As collecting the dataset need a huge amount of time, we provide two datasets to valid as an example. You can download the datasets like [env_name].tar.bz2 [At Anonymous Site Here](https://drive.google.com/file/d/1CW37J4msh3nzSnEwIWnSQ472L3_IfgIE/view?usp=sharing), and then extract them under the directory called **batch_data**.
```
--batch_data/
    --AntDir-v0/
        --data/
            --seed_1_goal_2.62/
                --obs.npy
                --actions.npy
                --next_obs.npy
                --rewards.npy
                --terminals.npy
            --seed_2_goal_2.739/
            ...
            --seed_40_goal_2.562/
```

## 2. Reproducing Environment
- GPU: NVIDIA 3090
- CPU: Intel(R) Core(TM) i9-10940X CPU @ 3.30GHz
- NVIDIA-SMI: 525.105.17
- CUDA Version: 11.7

We recommend you to reproduce the enviroment using Docker.

Install the MuJoCo according to [OpenAI guideline](https://github.com/openai/mujoco-py). To reproduce, you need to set the directory **.mujoco** under this directory **where the Dockerfile is** as the following file-tree:
```
--RETRO
    --.mujoco/
        --mjkey.txt
        --mjpro131/
        --mujoco210/
    --Dockerfile
```

Then do the following procedures to install retro.
- `sudo docker build -t retro:test1 .`
- `sudo docker run -itd --runtime=nvidia --gpus all retro:test1 /bin/bash`

**Note.** You may need to install `nvidia-docker` as follows:
```
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd
```

## 3. Run the code
You can use the following command to run the code:
```
conda activate retro
python [TRAIN_FILE_NAME] --env-type ant_dir --[OTHER_ARGS]
```
## 4. File Overview

### Purpose

This section is primarily intended to briefly introduce the purpose of the training file.

### Contents

#### 1. `train_[classifier/contrastive/reconstruction]_advance.py`

This section contains the training code for `k = a × bs` and `acc = 1`. You can set the value of parameter `a` through setting `--update_advance_frequency`.

#### 2. `train_[classifier/contrastive/reconstruction]_delay.py`

This section contains the training code for `k = 1 × bs` and `acc = a`. You can set the value of parameter `a` through setting `--update_delay_frequency`.

#### 3. `train_[classifier/contrastive/reconstruction]_pretrain.py`

This section contains the training code for `pretrain`. You should change the following code in the train file to correspond to the model file you have obtained.

##### contrastive/reconstruction
```
pretrained_base_logs_dir = "./logs/AntDir-v0-Mixed"
pretrained_logs_dir = "/contrastive_iter1500_seed" + str(self.args.seed) + "/models"
encoder_pt_name = "/encoder1500.pt"
decoder_pt_name = "/decoder1500.pt"
encoder_state_dict_dir = pretrained_base_logs_dir + pretrained_logs_dir + encoder_pt_name
decoder_state_dict_dir = pretrained_base_logs_dir + pretrained_logs_dir + decoder_pt_name
```

##### classifier
```
pretrained_classifier_base_logs_dir = "./logs/AntDir-v0-Mixed"
pretrained_classifier_logs_dir = "/classifier_iter1500_seed" + str(self.args.seed) + "/models"
pt_name = "/context_classifier1500.pt"
state_dict_dir = pretrained_classifier_base_logs_dir + pretrained_classifier_logs_dir + pt_name
```

#### 4. `train_[classifier/contrastive/reconstruction].py`

This section contains the training code for the original method.

#### 5. `offline_rl_config/args_ant_dir.py`
You can find the most detailed parameter information in this file.