import numpy as np
import wave
import random

def sine_wave(frequency, amplitude, time, sample_rate, vibrato_width, vibrato_speed):
    return (float(amplitude) * np.sin(2.0 * np.pi * float(frequency) * np.arange(sample_rate*time) / float(sample_rate) + vibrato_width*float(frequency) * np.sin(2.0 * np.pi * vibrato_speed * np.arange(sample_rate*time) / float(sample_rate)))).astype(np.float32)

def saw_wave(frequency, amplitude, time, sample_rate, vibrato_width, vibrato_speed):
    return ((float(amplitude) * 2.0 * ((float(frequency) * ((np.arange(sample_rate*time) / float(sample_rate) - 1 / (2* float(frequency))) + vibrato_width*float(frequency) * np.sin(2.0 * np.pi * vibrato_speed * np.arange(sample_rate*time) / float(sample_rate))    )) % 1)) - 1).astype(np.float32) # vib in the big space

def sinesaw_wave(frequency, amplitude, time, sample_rate, vibrato_width, vibrato_speed):
    return sum([float(amplitude) * 1.0 / float(n) * np.sin(2.0 * np.pi * n * float(frequency) * np.arange(sample_rate*time) / float(sample_rate) + vibrato_width*float(frequency) * np.sin(2.0 * np.pi * vibrato_speed * np.arange(sample_rate*time) / float(sample_rate))) for n in range(1,10)]).astype(np.float32)


def triangle_wave(frequency, amplitude, time, sample_rate, vibrato_width, vibrato_speed):
    return (float(amplitude) * np.arcsin(np.sin(2.0 * np.pi * float(frequency) * np.arange(sample_rate*time) / float(sample_rate) + vibrato_width*float(frequency) * np.sin(2.0 * np.pi * vibrato_speed * np.arange(sample_rate*time) / float(sample_rate))    )) * 2.0 / np.pi).astype(np.float32) # vibrato in large space

def square_wave(frequency, amplitude, time, sample_rate, vibrato_width, vibrato_speed):
    sine =  float(amplitude) * np.sin(2.0 * np.pi * float(frequency) * np.arange(sample_rate*time) / float(sample_rate) + vibrato_width*float(frequency) * np.sin(2.0 * np.pi * vibrato_speed * np.arange(sample_rate*time) / float(sample_rate))  ) # Add vib into this line, just before the last closing paren
    square = []
    for sample in sine:
        if sample > 0:
            square.append(1 * float(amplitude))
        elif sample < 0:
            square.append(-1 * float(amplitude))
        else:
            square.append(0)
    return np.array(square).astype(np.float32)

def noise(amplitude, time, sample_rate):
    output = []
    for i in range(int(sample_rate*time)):
        output.append(amplitude * (2*random.random() - 1))
    return np.array(output).astype(np.float32)



def add_waves(*samples):
    wave_sum = np.sum(samples, axis=0)
    max_amp = max(np.absolute(wave_sum))
    return (wave_sum * 32767/max_amp).astype(np.int16)

def make_wav(samples,filename):
    w = wave.open("sound_library/%s" % filename,"wb")
    w.setparams((1, 2, 44100, len(samples), 'NONE', 'not compressed'))
    print "Writing " + filename
    w.writeframes(samples)
    w.close()

# This will make one octave of pitches with the given parameters
notes = ["C","Cs","D","Ds","E","F","Fs","G","Gs","A","As","B","C2"]
base_frequency = 220*2**(0.25)
rate = 44100

                        #(frequency, amplitude, time, sample_rate, vibrato_width, vibrato_speed)
equal_temperament = [2**(i/12.0) for i in range(13)]
just_intonation = [1.0, 16.0/15.0, 9.0/8.0, 6.0/5.0, 5.0/4.0, 4.0/3.0, 7.0/5.0, 3.0/2.0, 8.0/5.0, 5.0/3.0, 16.0/9.0, 15.0/8.0, 2.0]
pythagorean_intonation = [1.0, 256.0/243.0, 9.0/8.0, 32.0/27.0, 81.0/64.0, 4.0/3.0, 729.0/512.0, 3.0/2.0, 128.0/81.0, 27.0/16.0, 16.0/9.0, 243.0/128.0, 2.0]
x = 5**0.25 #x = meantone temperament perfect fifth ratio
meantone_temperament = [1.0, 8.0/x**5, x**2 / 2.0, 4.0/x**3, x**4/4.0, 2.0/x, 16.0/x**6, x, 8.0/x**4, x**3/2.0, 4.0/x**2, x**5/4.0,2.0]
ratios = meantone_temperament
for i in range(13):
    #freq = base_frequency * 2 ** ((i + 3) / 12.0)
    freq = base_frequency * ratios[i]
    samples = add_waves(sine_wave(1*freq, 1, 10, rate, 0, 0),
                        sine_wave(2*freq, 0.5, 10, rate, 0, 0),
                        sine_wave(3*freq, 0.33, 10, rate, 0, 0),
                        sine_wave(4*freq, 0.25, 10, rate, 0, 0),
                        sine_wave(5*freq, 0.2, 10, rate, 0, 0),
                        sine_wave(6*freq, 0.167, 10, rate, 0, 0),
                        sine_wave(7*freq, 0.143, 10, rate, 0, 0),
                        sine_wave(8*freq, 0.125, 10, rate, 0, 0),
                        sine_wave(9*freq, 0.111, 10, rate, 0, 0),
                        sine_wave(10*freq, 0.1, 10, rate, 0, 0),
                        #noise(0.001, 10, rate)
                        )
    make_wav(samples.tobytes(), "mean_sine_" + notes[i] + ".wav")
