# config.py
# 高德API KEY配置
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--key', type=str, default='', help='高德API KEY')
args, _ = parser.parse_known_args()

AMAP_KEY = args.key or os.environ.get('AMAP_KEY', '')

