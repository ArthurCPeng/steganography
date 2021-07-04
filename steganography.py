import cv2
import numpy as np
import os.path
from tkinter import *
from tkinter import filedialog

root = Tk()
root.title("Steganographer")
root.geometry("500x380")
frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)

chosen_file_directory = ""


def decode(directory, password):
        
    image = cv2.imread(directory)
            
    image = list(np.reshape(image, -1))

    message_binary = ""
    message_text = ""

    for number in image:
        number = int(number)
        unit_info = format(number, "b")[-2:]
        message_binary += unit_info

    for i in range(int(len(message_binary)/8)-1):
        letter_binary = message_binary[i*8:(i+1)*8]
        letter_ascii = int(letter_binary, 2)
        letter_char = chr(letter_ascii)
        message_text += letter_char

    message_length = int(message_text[:8])
    password_length = int(message_text[8:12])
    password_true = message_text[12:12+password_length]

    if(password_true == password):
        message = message_text[12+password_length:12+password_length+message_length]
        message_box.delete(1.0, END)
        message_box.insert(1.0, message)
        root3 = Tk()
        root3.title("Successful!")
        warning_label = Label(root3, text = "Extraction successful!", justify = "center", width = 20, height = 5)
        warning_label.pack()
    else:
        root3 = Tk()
        root3.title("Warning")
        warning_label = Label(root3, text = "Password incorrect or wrong file. Try again.", justify = "center", width = 30, height = 5)
        warning_label.pack()
    
    
def encode(directory, message, password):
    
    image_org = cv2.imread(directory)
    h = image_org.shape[0]
    w = image_org.shape[1]
    c = image_org.shape[2]

    image_new = np.copy(image_org)


    #Shows an error if the image is not large enough to encode the message
    image_capacity = h * w * 3 / 4

    if(len(message) + len(password) + 12 > image_capacity):
        root4 = Tk()
        root4.title("Encoding Unsuccessful")
        unsuccessful_label = Label(root4, text = "Encoding unsuccessful.\nPlease find a larger image.", width = 30, height = 3, justify = "center")
        unsuccessful_label.pack()
        return False

    #Concatenate password to the messsage
    message = password + message 

    #Insert data on password length
    password_length_string = str(len(password))
    if(len(password_length_string) < 4):
        password_length_string = (4-len(password_length_string)) * "0" + password_length_string
    message = password_length_string + message

    #Insert metadata on message length
    message_length_string = str(len(message))
    if(len(message_length_string) < 8):
        message_length_string = (8-len(message_length_string)) * "0" + message_length_string
    message = message_length_string + message


    message_binary = ""
    for letter in message:
        letter_binary = str(format(ord(letter), "b")) #Convert string into binary message
        letter_binary = "0" * (8-len(letter_binary)) + letter_binary #Add leading zeroes to ensure length is 8
        message_binary += letter_binary #Add the binary representation of the letter to the binary message

    #Encode the message into the image.
    for i in range(int(len(message_binary) / 2)):
        unit_index = i
        unit_info = message_binary[i*2:(i+1)*2] 

        
        unit_c = i % c
        unit_w = int(i / c) % w
        unit_h = int(i / (c*w))

        unit_pixel_org = image_org[unit_h, unit_w, unit_c]
        unit_pixel_org_binary = format(unit_pixel_org, "b")
        unit_pixel_org_binary_string = str(format(unit_pixel_org, "b"))
        if(len(unit_pixel_org_binary_string) < 8):
            unit_pixel_org_binary_string = "0" * (8-len(unit_pixel_org_binary_string)) + unit_pixel_org_binary_string
                                                  
        unit_pixel_new_binary_string = unit_pixel_org_binary_string[0:6] + unit_info

        image_new[unit_h][unit_w][unit_c] = int(unit_pixel_new_binary_string, 2)

    cv2.imwrite(os.path.splitext(directory)[0] +"_EMBEDDED.png", image_new)
    return True


def selectFile():
    global chosen_file_directory 
    chosen_file_directory = filedialog.askopenfilename()
    if(chosen_file_directory != ""):
        chosen_file_entrybox.delete(0, END)
        chosen_file_entrybox.insert(0, chosen_file_directory)
    

def startEncode():
    password = password_entrybox.get()
    message = message_box.get(1.0, END).strip("\n")
    results = encode(chosen_file_directory, message, password)

    if results == True:
        root2 = Tk()
        root2.title("Success!")
        success_label = Label(root2, text = "Encoding Successful!", width = 15, height = 3, justify = "center")
        success_label.pack()

def startDecode():
    password = password_entrybox.get()
    decode(chosen_file_directory, password)


w = 15
h = 2

w_mb = 55
h_mb = 20

w_encode = 10
h_encode = 2
    
choose_file_button = Button(frame1, text = "Choose Image", justify = "center", width = w, height = h, command = selectFile)
choose_file_button.grid(row = 0, column = 0)

password_label = Label(frame1, text = "Encryption Password", justify = "center", width = w, height = h)
password_label.grid(row = 0, column = 1)

chosen_file_entrybox = Entry(frame1, text = chosen_file_directory, justify = "left", width = w)
chosen_file_entrybox.grid(row = 1, column = 0)

password_entrybox = Entry(frame1, show = "*", width = w)
password_entrybox.grid(row = 1, column = 1)

message_box = Text(frame2, width = w_mb, height = h_mb, padx = 10)
message_box.pack()

encode_button = Button(frame3, text = "Encode", justify = "center", width = w_encode, height = h_encode, command = startEncode)
encode_button.grid(row = 0, column = 0)

decode_button = Button(frame3, text = "Decode", justify = "center", width = w_encode, height = h_encode, command = startDecode)
decode_button.grid(row = 0, column = 1)

frame1.pack()
frame2.pack()
frame3.pack()



