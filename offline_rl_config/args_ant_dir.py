import argparse
import torch
from utils.cli import boolean_argument


def get_args(rest_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-name', default='AntDir-v0')
    parser.add_argument('--seed', type=int, default=3)

    parser.add_argument('--num-train-tasks', default=20)
    parser.add_argument('--num-eval-tasks', default=20)
    parser.add_argument('--max-rollouts-per-task', default=1) # should be 1, not BAMDP
    parser.add_argument('--num-trajs-per-task', type=int, default=None,
                        help='how many trajs per task to use. If None - use all')

    parser.add_argument('--meta-batch', type=int, default=16,
                        help='number of tasks to average the gradient across')
    parser.add_argument('--num-iters', type=int, default=1000, help='number meta-training iterates')

    # RL configs
    parser.add_argument('--rl-updates-per-iter', type=int, default=200, help='number of RL steps per iteration')
    parser.add_argument('--rl-batch-size', type=int, default=256, help='number of transitions in RL batch (per task)')
    parser.add_argument('--dqn-layers', nargs='+', default=[256, 256])
    parser.add_argument('--policy-layers', nargs='+', default=[256, 256])
    parser.add_argument('--actor-lr', type=float, default=0.0003, help='learning rate for actor (default: 3e-4)')
    parser.add_argument('--critic-lr', type=float, default=0.0003, help='learning rate for critic (default: 3e-4)')
    parser.add_argument('--vf-lr', type=float, default=0.0003, help='learning rate for v network (default: 3e-4)')
    parser.add_argument('--clip-grad-value', type=float, default=None, help='clip gradients')
    parser.add_argument('--entropy-alpha', type=float, default=0.2, help='Entropy coefficient')
    parser.add_argument('--automatic-entropy-tuning', default=False)
    parser.add_argument('--alpha-lr', type=float, default=None,
                        help='learning rate for entropy coeff, if automatic tuning is True (default: 3e-4)')
    parser.add_argument('--gamma', type=float, default=0.99, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--soft-target-tau', type=float, default=0.005,
                        help='soft target network update (default: 5e-3)')
    parser.add_argument('--eval-deterministic', default=True, type=int)
    parser.add_argument('--agent-sac', default=False)   
    parser.add_argument('--c-lr', type=float, default=1e-4, help='dual critic learning rate (BRAC dual)')
    parser.add_argument('--c-iter', type=float, default=3, help='number of dual critic steps per iteration')


    # general encoder configs
    parser.add_argument('--num-context-trajs', type=int, default=1, help='number of trajs provided \
        for task encoding. context-batch-size=1*traj_len=200')
    parser.add_argument('--encoder-lr', type=float, default=0.0003, help='learning rate for encoder (default: 3e-4)')

    # offline Pearl encoder configs
    parser.add_argument('--pearl-deterministic-encoder', type=int, default=True, help='if true, use deterministic\
        encoder; otherwise, use gaussian encoder, regularize with KL loss')
    parser.add_argument('--encoder-type', type=str, default='mlp', help='choose: rnn, mlp')
    parser.add_argument('--task-embedding-size', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--enc-stochastic', default=True)
    parser.add_argument('--aggregator-hidden-size', type=int, default=64, help='for both rnn and mlp')
    parser.add_argument('--layers-before-aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers-after-aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action-embedding-size', type=int, default=5)
    parser.add_argument('--state-embedding-size', type=int, default=5)
    parser.add_argument('--reward-embedding-size', type=int, default=5)

    # relabelling configs
    # gt: relabel with gt reward/transition. separate: learn a model for each task. generative: learn a generative model
    parser.add_argument('--relabel-type', type=str, default='generative', help='choose: gt, separate, generative, reward_randomize')
    parser.add_argument('--cvae-hidden-size', type=int, default=128)
    parser.add_argument('--cvae-num-hidden-layers', type=int, default=1)
    parser.add_argument('--cvae-z-dim', type=int, default=64, help='dimensionality of latent space')
    parser.add_argument('--generative-model-path', type=str)
    parser.add_argument('--aggregate-encoder-type', type=str, default='selfattn', help='choose: selfattn, mean')
    parser.add_argument('--reward-std', type=float, default=0.5)


    parser.add_argument('--contrastive-batch-size', type=int, default=64)
    parser.add_argument('--n-negative-per-positive', type=int, default=16)
    parser.add_argument('--normalize-z', type=int, default=True, help='encoding normalization')
    parser.add_argument('--infonce-temp', type=float, default=0.1, help='temperature param')
    parser.add_argument('--encoder-model-path', type=str)

    # debug configs, use gt task supervision
    parser.add_argument('--use-additional-task-info', type=int, default=False, help='')
    parser.add_argument('--context-encoder-output-layers', type=int, default=0)


    # logging, saving, evaluation
    parser.add_argument('--log-interval', type=int, default=5,
                        help='log interval, one log per n iterations (default: 10)')
    parser.add_argument('--log-vis-interval', type=int, default=100,
                        help='log interval for embedding visualization')
    parser.add_argument('--save-interval', type=int, default=100,
                        help='save models interval, every # iterations (default: 100)')
    parser.add_argument('--save-model', type=int, default=True)
    parser.add_argument('--log-tensorboard', type=int, default=True)
    parser.add_argument('--log-train-time', type=int, default=False, help='log training time cost')
    parser.add_argument('--use-gpu', default=True, help='whether to use gpu')
    parser.add_argument('--results-log-dir', default=None, help='directory to save agent logs (default: ./logs)')
    parser.add_argument('--output-file-prefix', default='offline')
    parser.add_argument('--data-dir', default='data')
    parser.add_argument('--main-data-dir', default='./batch_data')    
    
    ## extra
    parser.add_argument('--ensemble-size', type=int, default=1)
    parser.add_argument('--max-replay-size', default=500000)
    parser.add_argument('--use-decoder', default=True)  
    parser.add_argument('--beta-encoder', default=0.15, type=float)
    parser.add_argument('--alpha-encoder', default=0.1, type=float)
    parser.add_argument('--gamma-encoder', default=0.5, type=float)

    parser.add_argument('--decoder-iter', default=1, type=int)

    # CQL configs
    parser.add_argument('--use-cql', default=False, help='whether to use cql')
    parser.add_argument('--alpha-cql', type=float, default=2.0)
    # IQL configs
    parser.add_argument('--use-iql', default=False, help='whether to use iql')
    parser.add_argument('--quantile', type=float, default=0.8)
    parser.add_argument('--beta', type=float, default=0.05)
    parser.add_argument('--clip-score', type=int, default=100)

    # speed configs
    parser.add_argument('--update_delay_frequency', type=int, default=1)
    parser.add_argument('--update_advance_frequency', type=int, default=1)

    args = parser.parse_args(rest_args)

    return args
