import swmixer
from pynput.keyboard import Key, Listener

RATE = 44100
swmixer.init(samplerate=RATE, chunksize=1024, stereo=False)
swmixer.start()

prefix = "mean_sine_"
notes = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B", "C2"]
files = ["sound_library/%s%s.wav" % (prefix, note) for note in notes]
mixers = [swmixer.Sound(filename) for filename in files]

pitchstring = "awsedftgyhujk"
playing = dict()
for key in pitchstring:
    playing[key] = False
pitches = dict()
for i in range(13):
    pitches[pitchstring[i]] = notes[i]

def envelope(max_amplitude, attack_duration, decay_duration, sustain_amplitude, release_duration):
    # max_amplitude represents volume and should be in in [0,1]
    # All durations are measured in seconds
    if attack_duration > 0:
        return [(0, 0), (attack_duration*RATE, 1*max_amplitude), ((attack_duration+decay_duration)*RATE, sustain_amplitude*max_amplitude)], max_amplitude, release_duration*RATE
    else:
        return [(attack_duration * RATE, 1 * max_amplitude), ((attack_duration + decay_duration) * RATE, sustain_amplitude * max_amplitude)], max_amplitude, release_duration * RATE

#env, vol, release_time = envelope(0.1, 0.1, .05, 0.8, 0.2)
env, vol, release_time = envelope(0.25, 0, 0.05, 0.4, 0.2)


# Never need to change anything below this line!
channels = dict()
def on_press(key):
    try:
        if key.char in pitchstring:
            index = pitchstring.index(key.char)
            if not playing[key.char]:
                print pitches[key.char],
                channels[key.char] = mixers[index].play(volume=vol, envelope=env)
                playing[key.char] = True
    except AttributeError:
        if key == Key.esc:
            return False
        elif key == Key.space:
            print ""

def on_release(key):
    try:
        if key.char in pitchstring:
            index = pitchstring.index(key.char)
            channels[key.char].set_volume(0,fadetime=release_time)
            playing[key.char] = False
    except:
        pass


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
