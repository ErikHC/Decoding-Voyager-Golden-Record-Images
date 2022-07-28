## Decoding-Voyager-Golden-Record-Images
Using python to digitally decode the images encoded in the Voyager Golden Record's audio playback.

# Project as of 7/27/22
[A 16-bit PCM audio file](https://soundcloud.com/user-482195982/voyager-golden-record-encoded-images) sampled at 22050 Hz is manually clipped using Audacity to obtain selections of image encodings. The audio files are processed as WAV files for loading simplicity. The images are encoded through a straightforward analog audio amplitude modulation and are meant to be scanned top-bottom, left-to-right which corresponds, digitally, to a column-major order image matrix. The audio is written to a 1D NumPy array but is then reshaped based on an eyeballed average period sample width (i.e. column width) of 367 samples. This means each audio sample is directly converted to a pixel value.

To obtain a usable pixel, the audio sample quantization magnitude must be normalized to a range of 0:1 so it can be scaled by 255 to correspond to an (8-bit) RBG value. The actual analog audio encodings allow for RBG color images but my sampling will just be a simple grayscale (i.e a pixel will have equal R, G, and B values whose magnitude is proportional to the sample's relative magnitude).

The processed images I've provided are diagonal as a consequence of the "eyeballed average" period sample width which was determined manually using Audacity. The audio signals have a somewhat inconsistent period as a consequence of being analog and the file having a low sample rate. To obtain an accurate period, a more robust peak-detection function would have to be implemented (for instance, the max audio amplitude in the Calibration Circle waveform is ~0.20 units but the "scan-trigger" peaks are, from what I've eyeballed, usually <0.15 units and the function would have to account for this variation). It should also be noted that the audio magnitude is relatively weak so images must be enhanced (I used Windows' native photo editing tool). My grayscale scaling method also means that amplitude peaks will manifest whiter than the amplitude dips so my image will be color-inverted (which is undone using the PIL library).

I've also used the librosa library to plot the power spectrogram of the Calibration Circle's audio which, though only processing the signal's harmonic magnitudes over *time*, was able to produce an image of a semicircle (which "echo" across the spectrum). I'm not versed in DSP but I would imagine processes related to this would produce a more accurate image.

The Calibration circle (left audio channel's first image):

![](https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/CalibrationCircle_2022-07-27.png?raw=true "Calibration Circle")

Detail of the Milky Way (part of left audio channel's second image):

![](https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/EnhancedMilkyWayDetail_2022-07-27.png?raw=true "Milky Way detail")

Mathematical Definitions (left audio channel's third image):

![](https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/MathDefs_2022-07-27.png?raw=true "Mathematical Definitions")

Power Spectrogram:

![](https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/CalibrationCirclePowerSpec.png?raw=true)
