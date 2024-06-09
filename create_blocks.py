import argparse
from glob import glob
import numpy as np
import os
import shutil

def save_images_to_blocks(image_paths, outpath, n_blocks):
 block_size = len(image_paths) // n_blocks
 for block in range(n_blocks):
  block_path = os.path.join(outpath, f'block-{block + 1}')
  os.makedirs(block_path, exist_ok=True)
  start_idx = block * block_size
  end_idx = start_idx + block_size
  for img_path in image_paths[start_idx:end_idx]:
   shutil.copy(img_path, block_path)

def parse_args():
 parser = argparse.ArgumentParser()
 parser.add_argument('--img_path', type=str, default='src/img')
 parser.add_argument('--out_path', type=str, default='src/experiment')
 parser.add_argument('--n_participants', type=int, default=5)
 parser.add_argument('--n_trials_per_participant', type=int, default=100)
 parser.add_argument('--n_trials_per_block', type=int, default=50)
 return parser.parse_args()

# Split up the data into groups
if __name__ == '__main__':
 args = parse_args()
 img_paths = np.array(glob(os.path.join(args.img_path, '*.png')))

# Split up the data into groups
if __name__ == '__main__':
 args = parse_args()
 img_paths = np.array(glob(os.path.join(args.img_path, '*.png')))
 np.random.shuffle(img_paths)  # Randomly shuffle the images

 # Calculate the number of blocks and the number of images per participant
 n_blocks = args.n_trials_per_participant // args.n_trials_per_block
 images_per_group = args.n_trials_per_participant

 # Split the image paths into groups
 participant_groups = np.array_split(img_paths, args.n_participants)
 for i, group_images in enumerate(participant_groups):
  group_path = os.path.join(args.out_path, f'participant-group-{i + 1}')
  os.makedirs(group_path, exist_ok=True)  # Create the directory for the participant group

  # Save the images into blocks
  save_images_to_blocks(group_images, group_path, n_blocks)
