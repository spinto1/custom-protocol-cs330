from tkinter import *

scale = 1200  # Interface size in pixels


# Function used to update single frame in Tkinter window using gathered binary data
# Primarily use multi_color_clock function below, though
def clock(arr):
    current_byte = arr.pop(0)
    color = color_mapping[current_byte]  # Get next color value
    f1['bg'] = color  # Update color of frame
    if len(arr) > 0:
        root.after(1000, clock, arr)  # Wait 1000ms to call clock again on next binary value


# Function to update multiple (4) frames in Tkinter with binary data
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
    "ST": "#911eb4",  # Purple
    "EN": "#911eb4",  # Use purple again! Ended up working out very well
    "00": "#3cb44c",  # Green
    "01": "#e6194B",  # Red
    "10": "#4363d8",  # Blue
    "11": "#ffe119"   # Yellow
}

# Create Tkinter interface
root = Tk()
root.geometry("{}x{}".format(int(scale*1.5), scale))  # Can change size at top of code

# Create Tkinter frames
f1 = Frame(root, width=int(scale*1.5), height=scale/2, bg='#ffffff')
f1.place(x=0, y=0)
f2 = Frame(root, width=int(scale*1.5), height=scale/2, bg="#ffffff")
f2.place(x=int(scale*1.5)/2, y=0)
f3 = Frame(root, width=int(scale*1.5), height=scale/2, bg="#ffffff")
f3.place(x=0, y=scale/2)
f4 = Frame(root, width=int(scale*1.5), height=scale/2, bg="#ffffff")
f4.place(x=int(scale*1.5)/2, y=scale/2)

frames = [f1, f2, f3, f4]

# Get input desired to be sent and turn into binary
text = input('What to convert? ')
bytes_map = list(map(bin, bytearray(text, 'ascii')))

# Create array of 2-bit groupings of the ASCII binary message with checksum
half_bytes_array = []  # Start with DLE STX
for byte in bytes_map:
    b = byte[2:]
    while len(b) < 7:
        b = '0' + b
    # Add checksum:
    # If even number of 1's, first bit will be 1
    # If  odd number of 1's, first bit will be 0
    zero_count = b.count('0')
    checksum = zero_count % 2
    b = str(checksum) + b

    # Append byte to array containing 2 bits at a time
    for i in range(int(len(b)/2)):
        half_bytes_array.append(b[i*2:i*2+2])

# "Half" byte version of DLE STX and DLE ETX
start_frame = ["ST"] * 4
end_frame = ["EN"] * 4

# Create full message including starting and ending frame
full_message = start_frame[:]
full_message.extend(half_bytes_array*2)
full_message.extend(half_bytes_array[-4:])
full_message.extend(end_frame)

print(half_bytes_array)

# Visualize binary
print(''.join(full_message[4:-4]))
print(' '.join(full_message))

# Call clock function to display binary data with Tkinter interface
multi_color_clock(full_message)

root.mainloop()
