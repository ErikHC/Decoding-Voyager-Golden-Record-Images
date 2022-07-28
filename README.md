# Decoding-Voyager-Golden-Record-Images
Using python to digitally decode the images encoded in the Voyager Golden Record's audio playback.

## Background
[A 16-bit PCM audio file](https://soundcloud.com/user-482195982/voyager-golden-record-encoded-images) sampled at 22050 Hz is manually clipped using Audacity to obtain selections of image encodings. Audio is processed as WAV files for loading simplicity. The images are encoded through a straightforward analog audio amplitude modulation and are meant to be scanned top-to-bottom, left-to-right which corresponds, digitally, to a column-major order image matrix. The audio samples are loaded directly into a 1D NumPy array and the array is then reshaped based on an eyeballed average period sample width (i.e. column length) of 367 samples. This means each audio sample is directly converted to a pixel value.

To obtain a usable pixel, the audio sample quantization magnitude must be normalized to a range of 0:1 so it can be scaled by 255 to correspond to an (8-bit) RBG value. The actual analog audio encodings allow for RBG color images but my sampling will just be a simple grayscale (i.e a pixel will have equal R, G, and B values whose magnitude is proportional to the sample's relative magnitude).

The processed images I've provided are diagonal as a consequence of the "eyeballed" average period sample width which was determined manually using Audacity. The audio signals have a somewhat inconsistent period as a consequence of being analog and the file having a low sample rate. To obtain an accurate period, a more robust peak-detection function would have to be implemented (for instance, the max audio amplitude in the Calibration Circle waveform is ~0.20 units but the "scan-trigger" peaks are, from what I've eyeballed, usually <0.15 units and the function would have to account for this variation). It should also be noted that the audio magnitude is relatively weak so images must be enhanced (I used Windows' native photo editing tool). My grayscale scaling method also means that amplitude peaks will manifest whiter than the amplitude dips so my image will be color-inverted (which is undone using the PIL library).

I've also used the librosa library to plot the power spectrogram of the Calibration Circle's audio which, though only processing the signal's harmonic magnitudes over *time*, was able to produce an image of semicircles that "echo" across the spectrum. I'm not versed in DSP but I would imagine processes related to this would produce a more accurate image. A future goal of this project would be to actually use analog methods to decode the images (starting off with a study of TV signal demodulation).

## Generated Images

The Calibration Circle (left audio channel's first image):

![](https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/CalibrationCircle_2022-07-27.png?raw=true "Calibration Circle")

Detail of the Milky Way (part of left audio channel's second image):

![](https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/EnhancedMilkyWayDetail_2022-07-27.png?raw=true "Milky Way detail")

Mathematical Definitions (left audio channel's third image):

![](https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/MathDefs_2022-07-27.png?raw=true "Mathematical Definitions")

Power Spectrogram:

![](https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/CalibrationCirclePowerSpec.png?raw=true)

## Understanding Audio playback on the Record Glyphs

<img src="https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/The_Sounds_of_Earth_Record_Cover_-_GPN-2000-001978.jpg" width="443" height="443"/>

The front cover features glyphs that hint at universal constants to aid extraterrestrial life in properly extracting the information it contains. The cover includes a binary number system where '|' and '-' correspond to '1' and '0' respectively. The key to understanding the seemingly arbitrary binary number system is found in the bottom right glyph. The glyph is two circles connected with a horizontal line in between them. Each circle contains a "pinpoint" in their center and another pinpoint that, for left circle, points out and, for the right circle, points in. This glyph hints at the time it takes for the electron in a neutral hydrogen atom to transition to a higher energy state: 0.7e-9 seconds. With this constant, we can then scale the binary numbers to create a timing system for the playback devices.

Since our audio has already been recorded into some file, we only really care about the right side glyphs (the left side is for the extraterrestrials to have fun with). At the top right, there are three periods of an audio waveform, denoted by |, -|, and || (1, 2, and 3) respectively. Underneath period 1 is the number "101101001100000000000000" -> 11845632 which scales to 0.0082919424 indicating that the period of the waveform is ~8.3ms. Directly below this glyph is a sawtooth wave that, for each period, has two points circled. Below that glyph is a rectangular frame with binary numbers at the top left and right and a zigzag is featured inside the frame. Finally, below *that* glyph, there is another rectangular frame but this time a circle appears in the center.

As humans, we, of course, know that the record's output is an audio signal. The ET life is then supposed understand that the audio can correspond to an image. Our other advantage over ET life is that we intuitively understand that the waveform is amplitude as a function of (playback) time. As indicated by the sawtooth glyph, two points/sections in each period are of interest. These two points are amplitude peaks that can be understood as increases in signal intensity over a period. A crafty ET can then assign values to these intensities (in my case, a higher intensity means a whiter pixel). To then get a usable image, the ET will have to conform to the top-to-bottom, left-to-right scanning technique the zigzag glyph indicates. The binary at the top of the zigzag glyph is *sideways* and, if read bottom-to-top, left-to-right, will read "1 10 11 ... 1000000000" -> "1 2 3 ... 512" meaning there will be 512 periods for every image which will be "columns" as indicated by the zigzag on the zigzag glyph. The vertical distance will have to be proportional to the 8.3ms period (meaning the horizontal distance should be covered in 512*8.3e-3 = 4.2 seconds). If this is understood and implemented, images can then be generated and displayed on a screen of some sort.

If you actually plot the waveform, you'll find that there are two sections of peaks within a single period. A period will always have at least one peak at the end which is the "scan trigger" and indicates that a new vertical line scan is coming up. The other peaks that appear before the scan trigger are the image encodings. In the case of the Calibration Circle, there only needs to be two peaks (one takes care of the top semicircle and the other, occurring at a later point in time (i.e. more towards the bottom of the image), takes care of the bottom semicircle). These peaks as they appear in the actual waveform are circled in the image below.

![](https://github.com/ErikHC/Decoding-Voyager-Golden-Record-Images/blob/main/SawtoothPeaks.png?raw=true)

However, this scanning technique has a few subtleties when working with them digitally. As mentioned in the background section, the signal becomes discrete and the quality becomes highly dependent on the sample rate. If the typical 44100 Hz sample rate is used, we should get ~366 samples per period and, with 512 periods, there will be ~187407 samples for the entire image. Ideally this is the case for every image. Most importantly, the audio source I used for my audio file is at half speed and I'm using a 22050 Hz sample rate which, conveniently enough, corresponds to the same image dimensions as just described (except I found 36*7* to be the optimal sample size). For this project, I just manually selected the image waveforms to avoid having the deal with the transition signal separating the images.
