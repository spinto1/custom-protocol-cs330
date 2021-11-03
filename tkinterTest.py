from tkinter import *
import binascii

scale = 3  # Scale value. Increasing by 1 will increase total size of interface by 100x100px
scaled = scale*100


# Function used to update Tkinter window using gathered binary data
def clock(array_position):
    color = color_mapping[half_bytes_array[array_position]]  # Get next color value
    f1['bg'] = color  # Update color of frame
    if array_position < len(half_bytes_array)-1:
        root.after(1000, clock, array_position+1) # Wait 1000ms to call clock again on next binary value


def clock2(arr):
    current_byte = arr.pop(0)
    color = color_mapping[current_byte]  # Get next color value
    f1['bg'] = color  # Update color of frame
    if len(arr) > 0:
        root.after(1000, clock2, arr)  # Wait 1000ms to call clock again on next binary value


def multi_color_clock(arr):
    for n in range(4):
        if arr:
            current_byte = arr.pop(0)
            color = color_mapping[current_byte]  # Get next color value
            frames[n]['bg'] = color  # Update color of frame
        else:
            frames[n]['bg'] = "purple"
    if len(arr) > 0:
        root.after(1000, multi_color_clock, arr)  # Wait 1000ms to call clock again on next binary value


# Mapping of binary values to colors
# Color Sources: https://sashamaps.net/docs/resources/20-colors/
color_mapping = {
    "00": "#ffffff",  # White
    "01": "#e6194B",  # Red
    "10": "#4363d8",  # Blue
    "11": "#000000"   # Black
}

# Create Tkinter interface of 200x200 size
root = Tk()
root.geometry("{}x{}".format(scaled, scaled))  # Can change size at top of code

# Create Tkinter frame
f1 = Frame(root, width=scaled/2, height=scaled/2, bg='#ffffff')
f1.place(x=0, y=0)
# More frames for later use
f2 = Frame(root, width=scaled/2,height=scaled/2, bg="#ffffff")
f2.place(x=scaled/2, y=0)
f3 = Frame(root, width=scaled/2,height=scaled/2, bg="#ffffff")
f3.place(x=0, y=scaled/2)
f4 = Frame(root, width=scaled/2,height=scaled/2, bg="#ffffff")
f4.place(x=scaled/2, y=scaled/2)

frames = [f1, f2, f3, f4]

# Get input desired to be sent and turn into binary
text = input('What to convert? ')
bytes_map = list(map(bin, bytearray(text, 'ascii')))

half_bytes_array = []  # Start with DLE STX
for byte in bytes_map:
    b = byte[2:]
    while len(b) < 8:
        b = '0' + b
    if b == '00010000':  # If DLE character, add it twice
        b *= 2
    print(len(b), b)
    for i in range(int(len(b)/2)):
        print(b[i*2:i*2+2])
        half_bytes_array.append(b[i*2:i*2+2])

# "Half" byte version of DLE STX and DLE ETX
start_frame = ['00', '01', '00', '00', '00', '00', '00', '10']
end_frame = ['00', '01', '00', '00', '00', '00', '00', '11']

# Create full message including starting and ending frame
full_message = start_frame[:]
full_message.extend(half_bytes_array)
full_message.extend(end_frame)

# Visualize binary
print(' '.join(bytes_map))
print(' '.join(full_message))

# Call clock function to display binary data with Tkinter interface
#clock(0)
multi_color_clock(half_bytes_array)

root.mainloop()

# Code to decode from binary back to text
# https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
# test = int(2)
# print(test.to_bytes((test.bit_length() + 7) // 8, 'big').decode())
