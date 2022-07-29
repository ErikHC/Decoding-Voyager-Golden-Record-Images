import numpy as np
import librosa.display
from PIL import Image as Im
import PIL.ImageOps
import matplotlib.pyplot as plt

ROW_CONSTANT = 367  # Based on "eyeballed" average period sample width


def waveform_info(sample_array, array_print=False):
    """Provides length, min, and max of audio samples array. Can also print the entire array if desired."""
    print(f"min is: {min(sample_array)}\n"
          f"max is: {max(sample_array)}\n"
          f"size of array is {len(sample_array)}")
    if array_print:
        np.set_printoptions(threshold=np.inf)
        print(sample_array)


def normalize_waveform(sample_array):
    """Normalizes NumPy array data to range of 0:1 and scales to 255 for RGB"""
    return 255 * (sample_array - np.min(sample_array)) / (np.max(sample_array) - np.min(sample_array))


def process_image(sample_array):
    """Organizes the 1D NumPy array of samples into an image matrix and then generates the image."""
    cols = -(len(sample_array) // -ROW_CONSTANT)  # Ceiling division to determine image width
    # Padding image matrix with black pixels if rows*cols is under-filled
    aspect_missing = (cols * ROW_CONSTANT) - len(sample_array)
    sample_array = np.pad(sample_array, (0, aspect_missing), "constant", constant_values=1)
    sample_array = normalize_waveform(sample_array)
    # Organize image matrix in column-major order
    sample_array = sample_array.reshape(ROW_CONSTANT, cols, order='F')
    data = Im.fromarray(sample_array)
    if data.mode != "RGB":
        data = data.convert("RGB")
    img_file = "raw_img.png"
    data.save(img_file)
    invert_image(img_file)


def invert_image(img_file):
    """Inverts the RGB color of a given image. Images may need further editing for clarity."""
    image = Im.open(img_file)
    inverted_image = PIL.ImageOps.invert(image)
    return inverted_image.save(img_file)


def spectrogram(sample_array):
    """Generates a power spectrogram for a given audio sample array."""
    spec = np.abs(librosa.stft(sample_array))
    fig, ax = plt.subplots()
    img = librosa.display.specshow(librosa.amplitude_to_db(spec, ref=np.max), y_axis="log", x_axis="time", ax=ax)
    ax.set_title("Power Spectrogram")
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    plt.show()


def main():
    filename = "MathDefs_audio.wav"  # Dummy audio file
    y, sr = librosa.load(filename)
    process_image(y)
    # waveform_info(y)
    # spectrogram(y)


main()
