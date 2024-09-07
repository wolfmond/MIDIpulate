#   current version: 2024-09-08_058
#   
#   This is free and unencumbered software released into the public domain.
#   
#   Anyone is free to copy, modify, publish, use, compile, sell, or
#   distribute this software, either in source code form or as a compiled
#   binary, for any purpose, commercial or non-commercial, and by any
#   means.
#   
#   In jurisdictions that recognize copyright laws, the author or authors
#   of this software dedicate any and all copyright interest in the
#   software to the public domain. We make this dedication for the benefit
#   of the public at large and to the detriment of our heirs and
#   successors. We intend this dedication to be an overt act of
#   relinquishment in perpetuity of all present and future rights to this
#   software under copyright law.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#   OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#   OTHER DEALINGS IN THE SOFTWARE.
#   
#   For more information, please refer to <http://unlicense.org/>

# IMPORTANT NOTICE: I'm timestretching the exported MIDI file manually * 3,6. I'm creating a 100 seconds file for using it in a 6 minutes (360 seconds) track.

import random
from midiutil import MIDIFile
from datetime import datetime

midi_array = [
    36, 38, 40, 41, 43, 45, 47, # C2 bis B2
    48, 50, 52, 53, 55, 57, 59, # C3 bis B3
    60, 62, 64, 65, 67, 69, 71, # C4 bis B4
    72, 74, 76, 77, 79, 81, 83, # C5 bis B5
    84, # 86, 88, 89, 91, 93, 95, # C6 bis B6
    # 96 # C7
]

#pentatonic
midi_array = [
    36, 38, 40, 43, 45,  # C2, D2, E2, G2, A2 (C-Dur-Pentatonik)
    48, 50, 52, 55, 57,  # C3, D3, E3, G3, A3
    60, 62, 64, 67, 69,  # C4, D4, E4, G4, A4
    72, 74, 76, 79, 81,  # C5, D5, E5, G5, A5
    84  # C6
]

midi_array = [
    # C major pentatonic with octaves: C, D, E, G, A
    36, 38, 40, 43, 45,  # C2, D2, E2, G2, A2
    48, 50, 52, 55, 57,  # C3, D3, E3, G3, A3
    60, 62, 64, 67, 69,  # C4, D4, E4, G4, A4
    72, 74, 76, 79, 81,  # C5, D5, E5, G5, A5
    84, 86, 88, 91, 93   # C6, D6, E6, G6, A6
]

midi_array = [
    # D major pentatonic: D, E, F#, A, B
    38, 40, 42, 45, 47,  # D2, E2, F#2, A2, B2
    50, 52, 54, 57, 59,  # D3, E3, F#3, A3, B3
    62, 64, 66, 69, 71,  # D4, E4, F#4, A4, B4
    #74, 76, 78, 81, 83,  # D5, E5, F#5, A5, B5
    #86, 88, 90, 93, 95   # D6, E6, F#6, A6, B6
]

# Function for creating a MIDI file based on random notes
def create_random_midi(duration_in_seconds, output_file='random_midi.mid', tempo=120):
    midi = MIDIFile(1)
    midi.addTempo(0, 0, tempo)
    
    time = 0 
    while time < duration_in_seconds:
        # Select random note from the array
        pitch = random.choice(midi_array)
        # Random velocity between 60 and 127
        velocity = random.randint(60, 127)
        # Random duration of the note in quarter notes (0.25 to 1 second)
        duration = random.uniform(0.25, 1.0)
        # Add the note (track 0, channel 0)
        midi.addNote(0, 0, pitch, time, duration, velocity)
        # Increase the time by the duration of the note
        time += duration
    
    # Save the MIDI file
    with open(output_file, 'wb') as midi_file:
        midi.writeFile(midi_file)
    
    print(f"MIDI file was created: {output_file}")

def main():
    # Ask user for the length of the MIDI file in seconds
    try:
        duration = int(input("Duration in seconds: "))
    except ValueError:
        print("Please enter a valid number.")
        return
        
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # Create MIDI file
    #create_random_midi(duration_in_seconds=duration, output_file='random_midi.mid', tempo=120)
    create_random_midi(duration_in_seconds=duration, output_file= f'random_midi_{timestamp}.mid', tempo=120)

if __name__ == "__main__":
    main()
