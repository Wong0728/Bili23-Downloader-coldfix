from utils.module.ffmpeg.env import FFEnv
from utils.module.aria2.env import Aria2Env

FFEnv.detect()
Aria2Env.auto_detect_and_configure()