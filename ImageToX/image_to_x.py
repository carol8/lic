import os
import glob
import argparse
from PIL import Image
import cv2


# Function to create a GIF from screenshots
def create_gif(image_files, output_path, duration):
    frames = [Image.open(image) for image in image_files]
    frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0, duration=duration)
    print(f"GIF saved at {output_path}")


# Function to create a video from screenshots
def create_video(image_files, output_path, fps):
    frame = cv2.imread(image_files[0])
    height, width, layers = frame.shape
    output_path = output_path + '.mp4'
    video = cv2.VideoWriter(output_path, cv2.VideoWriter.fourcc('m', 'p', '4', 'v'), fps, (width, height))
    for image in image_files:
        video.write(cv2.imread(image))
    video.release()
    print(f"Video saved at {output_path}")


# Main function to handle command line arguments and call the appropriate functions
def main():
    parser = argparse.ArgumentParser(description="Convert screenshots to GIFs or videos.")
    parser.add_argument('image_folder', type=str, help='Path to the folder containing screenshots.')
    parser.add_argument('output_folder', type=str, help='Path to save the output GIFs or videos.')
    parser.add_argument('--type', type=str, choices=['gif', 'video'], required=True, help='Output type: gif or video.')
    parser.add_argument('--duration', type=int, default=100,
                        help='Duration between frames in milliseconds for GIF (default: 100)')
    parser.add_argument('--fps', type=int, default=10, help='Frames per second for video (default: 10)')

    args = parser.parse_args()

    # Ensure the output folder exists
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    # Get all screenshot files
    image_files = glob.glob(os.path.join(args.image_folder, 'screenshot_seq_*.png'))

    # Group images by sequence
    sequences = {}
    for image_file in image_files:
        sequence_id = '_'.join(os.path.basename(image_file).split('_')[:3])
        if sequence_id not in sequences:
            sequences[sequence_id] = []
        sequences[sequence_id].append(image_file)

    sorted_images = sorted(image_files, key=lambda x: (int(x.split('_')[2]), int(x.split('_')[4].split('.')[0])))

    # Group images by sequence
    sequences = {}
    for image_file in sorted_images:
        sequence_id = '_'.join(os.path.basename(image_file).split('_')[:3])
        if sequence_id not in sequences:
            sequences[sequence_id] = []
        sequences[sequence_id].append(image_file)

    # Process each sequence
    for sequence_id, files in sequences.items():
        output_path = os.path.join(args.output_folder, f"{sequence_id}.{args.type}")

        if args.type == 'gif':
            create_gif(files, os.path.join(args.output_folder, f"{sequence_id}.{args.type}"), args.duration)
        elif args.type == 'video':
            create_video(files, os.path.join(args.output_folder, f"{sequence_id}"), args.fps)


if __name__ == "__main__":
    main()

