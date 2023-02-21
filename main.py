from tkinter import *
from tkinter import ttk

root = Tk()
frm = ttk.Frame(root, padding=10)

list_subnet = []
nonbin_subnet = [0, 0, 0, 0]
bcast = [0, 0, 0, 0]
binary_sub = []
binary_ip = []
ipvar = StringVar()
subvar = StringVar()
ip_ent = Entry(frm)
snm_ent = Entry(frm)
ip_string = ""
frm.grid()


def calculate_bin():
    global binary_ip
    global ip_string
    ip = ip_ent.get()
    ip_split = ip.split(".")
    for octave in ip_split:
        altbinary_ip = [0, 0, 0, 0, 0, 0, 0, 0]
        try:
            octave = int(octave)
            bits = 128
            current_bin = 0

            while bits >= 1:
                if octave >= bits:
                    altbinary_ip[current_bin] = 1
                    octave -= bits
                bits = bits / 2
                current_bin += 1

            for x in altbinary_ip:
                binary_ip.append(x)
                ip_string = ip_string + str(x)
            if len(ip_string) < 32:
                ip_string += "."
        except ValueError:
            ip_string = "Error: Invalid IP address"
        ipvar.set(f"Binary form: {ip_string}")


def calculate_subnet():
    global binary_sub
    try:
        subnet = int(snm_ent.get())
        one_amount = 1
        while one_amount <= 32:
            if one_amount <= subnet:
                binary_sub.append(1)
            else:
                binary_sub.append(0)
            one_amount += 1
        bits = 128.0
        non_bin = []
        for x in binary_sub:
            if x == 1:
                non_bin.append(bits)
            bits = bits / 2
            if bits < 1:
                bits = 128.0
        octave1 = 0
        octave2 = 0
        octave3 = 0
        octave4 = 0
        subnetwhole = [octave1, octave2, octave3, octave4]
        currentoct = 0
        summan = 0
        for c in non_bin:
            summan += c
            subnetwhole[currentoct] = summan
            if c == 1.0:
                currentoct += 1
                summan = 0
        finalsum = ""
        for v in subnetwhole:
            finalsum = finalsum + str(int(v))
            if finalsum.count(".") < 3:
                finalsum += "."
        subvar.set(f"Subnet Mask: {finalsum}")
    except ValueError:
        subvar.set("Invalid subnet")


def calculate_thing():
    global binary_sub
    global binary_ip
    current_step = 0
    while current_step <= 31:
        if int(binary_sub[current_step]) * int(binary_ip[current_step]) == 1:
            list_subnet.append(1)
        else:
            list_subnet.append(0)
        current_step += 1
    print(list_subnet)

    bits = 128
    current_oct = 0
    bit_list = []
    for x in list_subnet:
        if int(x) == 1:
            bit_list.append(bits)
        else:
            bit_list.append(0)
        if bits > 1:
            bits /= 2
        else:
            bits = 128
    print(bit_list)
    while current_oct <= 3:
        for y in bit_list[0:8]:
            nonbin_subnet[current_oct] += y
        del bit_list[0:8]
        current_oct += 1
    print(nonbin_subnet)


def calculate_bcast():
    currentstep = 0
    snetmask = snm_ent.get()
    while currentstep <= 31 - int(snetmask):
        list_subnet[-1 - currentstep] = 1
        currentstep += 1

    bits = 128
    current_oct = 0
    bit_list = []
    for x in list_subnet:
        if int(x) == 1:
            bit_list.append(bits)
        else:
            bit_list.append(0)
        if bits > 1:
            bits /= 2
        else:
            bits = 128
    print(bit_list)
    while current_oct <= 3:
        for y in bit_list[0:8]:
            bcast[current_oct] += y
        del bit_list[0:8]
        bcast[current_oct] = int(bcast[current_oct])
        current_oct += 1
    print(bcast)


def calculate():
    calculate_bin()
    calculate_subnet()
    calculate_thing()
    calculate_bcast()


subnet_result = Label(frm, textvariable=subvar)
bin_result = Label(frm, textvariable=ipvar)
ttk.Label(frm, text="Enter a valid IP address then press \"Submit\" to calculate").grid(column=1, row=0)
ttk.Label(frm, text="Welcome to Python IP calculator!").grid(column=0, row=0)
Label(frm, text="Enter your IP address here").grid(column=0, row=2)
ip_ent.grid(column=0, row=3)
ttk.Button(frm, text="Submit", command=calculate).grid(column=0, row=6)
bin_result.grid(column=1, row=3)
Label(frm, text="Enter Mask bits here (0-32)").grid(column=0, row=4)
snm_ent.grid(column=0, row=5)
subnet_result.grid(column=1, row=5)
root.mainloop()
