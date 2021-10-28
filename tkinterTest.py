from tkinter import *


# Function used to update Tkinter window using gathered binary data
def clock(array_position):
    color = color_mapping[half_bytes_array[array_position]]  # Get next color value
    f1['bg'] = color  # Update color of frame
    if array_position < len(half_bytes_array)-1:
        root.after(1000, clock, array_position+1) # Wait 1000ms to call clock again on next binary value


# Mapping of binary values to colors
# Colr Sources: https://sashamaps.net/docs/resources/20-colors/
color_mapping = {
    "00": "#ffffff",  # White
    "01": "#e6194B",  # Red
    "10": "#4363d8",  # Blue
    "11": "#000000"   # Black
}

# Get input desired to be sent and turn into binary
text = input('What to convert? ')
bytes_map = list(map(bin, bytearray(text, 'ascii')))

half_bytes_array = []
for byte in bytes_map:
    b = byte[2:]
    while len(b) < 8:
        b = '0' + b
    for i in range(4):
        half_bytes_array.append(b[i:i+2])

# Visualize binary
print(' '.join(bytes_map))
print(' '.join(half_bytes_array))

# Create Tkinter interface of 200x200 size
root = Tk()
root.geometry("200x200")

# Create Tkinter frame
f1 = Frame(root, width=200, height=200, bg='white')
f1.pack(side=TOP, anchor=NW)
# More frames for later use
'''f2=Frame(root,width=100,height=100,bg="blue")
f2.pack(side=TOP, anchor=NE)
f3=Frame(root,width=50,height=50,bg="green")
f3.pack(fill=Y)'''
# Call clock function to display binary data with Tkinter interface
clock(0)

root.mainloop()

