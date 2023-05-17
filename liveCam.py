import cv2
import urllib.request
import numpy as np
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Capture live images from a URL and create a video.')
parser.add_argument('-u', '--url', type=str, help='URL of the live image capture link (must be in single quetes)', required=True)
parser.add_argument('-f', '--fps', type=float, help='FPS (frames per second) of the output video', default=24.0)
parser.add_argument('-n', '--num_images', type=int, help='Number of images to capture', default=100)
args = parser.parse_args()

# Define the video output file
output_file = 'output.avi'

# Define the video codec and frame rate
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Set up the video writer
out = cv2.VideoWriter(output_file, fourcc, args.fps, (640, 480))

# Loop through the images and write them to the video
for i in range(args.num_images):
    try:
        # Read the image from the URL
        resp = urllib.request.urlopen(args.url)
        img_array = np.array(bytearray(resp.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)

        # Check if the image is valid
        if img is None or img.size == 0:
            raise Exception("Invalid image")

        # Resize the image if necessary
        # img = cv2.resize(img, (640, 480))

        # Write the image to the video file
        out.write(img)

        # Display the current frame
        cv2.imshow('Live Video', img)
        if cv2.waitKey(1) == ord('q'):
            break

        # Print the shape of the retrieved image
        print("Image shape:", img.shape)

    except Exception as e:
        print("Error:", e)
        continue

# Release the video writer and close the window
out.release()
cv2.destroyAllWindows()
