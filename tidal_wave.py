#   current version: 2024-09-08_0111
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

# IMPORTANT NOTICE: please get in contact with Bundesamt für Seeschifffahrt und Hydrographie (https://www.bsh.de) to receive a license to use the JSON-data. Please adjust the scripts to your needs and use OpenSource data.

import json
import requests
from midiutil import MIDIFile
from datetime import datetime
import numpy as np

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
velocity_array = list(range(120, 59, -1))  # Descending values for smooth dynamics

def get_midi_note(value, min_value, max_value):
    percentage = (value - min_value) / (max_value - min_value) * 100
    index = round((len(midi_array) - 1) * (percentage / 100))
    return midi_array[max(0, min(index, len(midi_array) - 1))]

def get_velocity(value, min_value, max_value):
    percentage = (value - min_value) / (max_value - min_value) * 100
    index = round((len(velocity_array) - 1) * (percentage / 100))
    return velocity_array[max(0, min(index, len(velocity_array) - 1))]

def create_midi_from_notes(notes, output_file='water_sonification.mid', tempo=120):
    midi = MIDIFile(1)
    midi.addTempo(0, 0, tempo)
    midi.addProgramChange(0, 0, 0, 11)  # Instrument
    
    time = 0
    for note in notes:
        pitch, velocity, duration = note
        midi.addNote(0, 0, pitch, time, duration, velocity)
        time += duration
    
    with open(output_file, 'wb') as midi_file:
        midi.writeFile(midi_file)

def main():
    # Retrieve JSON data
    response = requests.get('https://wasserstand-nordsee.bsh.de/data/DE__764B.json')
    data = response.json()
    
    # Processing the JSON data
    curve_data = data['curve_forecast']['data']
    
    # Extract measured values and calculate min/max
    curveforecasts = [entry['curveforecast'] for entry in curve_data if entry['curveforecast'] is not None]
    if not curveforecasts:
        print("No valid measurements found.")
        return
    min_curveforecast = min(curveforecasts)
    max_curveforecast = max(curveforecasts)
    
    notes = []
    note_alt = None
    note_length = 1
    
    for entry in curve_data:
        timestamp = datetime.fromisoformat(entry['timestamp'])
        #curveforecast = entry['curveforecast']
        curveforecast = entry['curveforecast']
        
        if curveforecast is None:
            continue
        
        note = get_midi_note(curveforecast, min_curveforecast, max_curveforecast)
        velocity = get_velocity(curveforecast, min_curveforecast, max_curveforecast)
        
        if note_alt is not None and note_alt != note:
            if note_alt is not None and velocity is not None:
                notes.append((note_alt, velocity, note_length))
        
        if note_alt != note:
            note_alt = note
            note_length = 1
        else:
            note_length += 1
    
    # Erstelle die MIDI-Datei
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    create_midi_from_notes(notes, output_file= f'tidal_wave_{now}.mid', tempo=120)
    print(f"MIDI file was created: tidal_wave_{now}.mid")

if __name__ == "__main__":
    main()
