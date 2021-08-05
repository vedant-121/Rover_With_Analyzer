import tkinter
from tkinter import *
from tkinter import Tk
from tkinter import ttk
import datetime as dt
from cv2 import cv2
from PIL import Image, ImageTk
import tkinter.font as tkFont

import imutils
import tkinter.simpledialog
import tkinter.filedialog
from tkinter import messagebox
from firebase_admin import credentials, firestore
import firebase_admin
from scipy.spatial.distance import euclidean
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
from PIL import Image


# Function to show array of images (intermediate results)
# def show_images(images):
# 	for i, img in enumerate(images):
# 		# print(str(i))
# 		cv2.imshow("image_" + str(i), img)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()


def img_dimension(img):
    image = img

    # Read image and preprocess
    # image = cv2.imread(img_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    edged = cv2.Canny(blur, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    # show_images([blur, edged])

    # Find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Sort contours from left to right as leftmost contour is reference object
    (cnts, _) = contours.sort_contours(cnts)

    # Remove contours which are not large enough
    cnts = [x for x in cnts if cv2.contourArea(x) > 100]

    # cv2.drawContours(image, cnts, -1, (0,255,0), 3)

    # show_images([image, edged])
    print(len(cnts))

    # Reference object dimensions
    # Here for reference I have used a 2cm x 2cm square
    ref_object = cnts[0]
    box = cv2.minAreaRect(ref_object)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    (tl, tr, br, bl) = box
    dist_in_pixel = euclidean(tl, tr)
    dist_in_cm = 2
    pixel_per_cm = dist_in_pixel / dist_in_cm

    # Draw remaining contours
    count = 0
    for cnt in cnts:
        count = count + 1
        if (count == 2):
            box = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            (tl, tr, br, bl) = box
            cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
            mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0]) / 2), tl[1] + int(abs(tr[1] - tl[1]) / 2))
            mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0]) / 2), tr[1] + int(abs(tr[1] - br[1]) / 2))
            wid = euclidean(tl, tr) / pixel_per_cm
            ht = euclidean(tr, br) / pixel_per_cm
        # if (count == 2):
            # e_text3.delete(1.0, "END")
            width="{:.1f}cm".format(wid)

            e_text3.delete("1.0", "end")
            e_text3.insert("end-1c",width)

            height="{:.1f}cm".format(ht)

            e_text4.delete("1.0", "end")
            e_text4.insert("end-1c",height)
            # e_text3.insert("hi")
            print("{:.1f}cm".format(wid), "{:.1f}cm".format(ht))

            cv2.putText(image, "{:.1f}cm".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            cv2.putText(image, "{:.1f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    # show_images([image])




def img_texture(img2):
    # im = img

    # im = img
    # Setting the points for cropped image
    width, height = img2.size
    left = 150
    top = 5
    right = width
    bottom = height

    # Cropped image of above dimension
    # (It will not change original image)
    im1 = img2.crop((left, top, right, bottom))
    img=cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
    # show thresh and result
    # cv2.imshow("thresh", img)
    # # cv2.imshow("contours", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # Shows the image in image viewer
    # im1.show()

    # from here
    #
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # threshold
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # invert
    thresh = 255 - thresh
    # get contours and compute average number of vertices per character (contour)
    result = img.copy()
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    num_contours = 0
    sum = 0
    for cntr in contours:
        cv2.drawContours(result, [cntr], 0, (0, 0, 255), 1)
        num_vertices = len(cntr)
        sum = sum + num_vertices
        num_contours = num_contours + 1

    smoothness = (sum / num_contours)
    print("smooth", smoothness)
    print("sum=", sum)
    print("num_c", num_contours)
    txtr="smooth"
    if (sum > 450):
        txtr="rough"
        print("rough")
    else:
        txtr="smooth"
        print("smooth")
    e_text2.delete("1.0", "end")
    e_text2.insert("end-1c", txtr)

    cv2.destroyAllWindows()
def ok():

    global d
    # if v == 1:
    f = tkinter.filedialog.askopenfile(mode='r')

    if f != None:
        try:
            d.cap.release()
            cv2.destroyAllWindows()
            del (d)
        except NameError:
            print("Choosing pic again")


        img = cv2.imread(f.name)

        img2 = Image.open(f.name)

        img_dimension(img)
        img_texture(img2)



def rb_left():
    status_label.config(text="move rover left")


def rb_right():
    status_label.config(text="move rover right")


def rb_front():
    status_label.config(text="move rover forward")


def rb_rear():
    status_label.config(text="move rover rear")


def ab_left():
    status_label2.config(text="move arm left")


def ab_right():
    status_label2.config(text="move arm right")


def ab_front():
    status_label2.config(text="move arm forward")


def ab_rear():
    status_label2.config(text="move arm rear")

def open_s():
    door_status.config(state='normal')
    door_status.delete("1.0", "end")
    door_status.insert(END,"Door status:- \nOpened")
    door_status.config(state='disabled')

def close_s():
    door_status.config(state='normal')

    door_status.delete("1.0", "end")
    door_status.insert(END,"Door status:- \nClosed")
    door_status.config(state='disabled')

def clicked():
    image_s.config(text="Image Captured")



if __name__ == "__main__":
    # d = Video()

    root = Tk()
    root.geometry("990x740")
    root.configure(background='gray5', bd=1, relief=SUNKEN, )
    root.minsize(990, 740)
    root.maxsize(990, 740)

    root.title("ROVER & ANALYZER")
    root.iconbitmap('images/circle_red.ico')

    # theme for tabs

    myblack = "#000000"
    myyellow = "#FFFF00"

    style = ttk.Style()

    style.theme_create("theme", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": "gray5"}, },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": myblack, "foreground": myyellow},
            "map":       {"background": [("selected", myyellow)], "foreground": [("selected", myblack)],
                          "expand": [("selected", [1, 1, 1, 0])]}}})

    style.theme_use("theme")

    # theme ended
    top_top_frame = Frame(root, bg="black", relief=SUNKEN)
    top_top_frame.grid(row=0, column=0, sticky="nsew")

    # making tabs
    tabControl = ttk.Notebook(root)
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text="ROVER/ARM")
    tabControl.grid(row=1, column=0, sticky="nsew")
    # tabControl.pack(expand=True, fill="both")

    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab2, text="ANALYZER", )
    tabControl.grid(row=1, column=0, sticky="nsew")
    # tabControl.pack(expand=True, fill="both")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # elements of tab1

    top_frame = Frame(tab1, bg='black', relief=SUNKEN)
    center = Frame(tab1, bg='gray2', relief=SUNKEN)
    btm_frame = Frame(tab1, bg='black', relief=SUNKEN)

    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="nsew")
    btm_frame.grid(row=3, sticky="ew")

    tab1.grid_rowconfigure(1, weight=1)
    tab1.grid_columnconfigure(0, weight=1)

    # heading

    heading_label = Label(top_top_frame, text="ROVER & ANALYZER",
                          bd=5,
                          bg="black",
                          fg="white",
                          relief=SUNKEN,
                          font="Verdana 15 bold",
                          anchor=CENTER, )
    heading_label.pack(fill=X)

    center_frame = Frame(center, bg=myyellow, relief=SUNKEN, bd=1)
    center_frame.pack(fill=BOTH, side=LEFT, expand=True)

    right_frame = Frame(center, bg=myblack, relief=SUNKEN, )
    right_frame.pack(side=RIGHT, fill=Y)



    '''frame for start and stop button'''

    ss_frame = Frame(right_frame, bg=myblack)
    ss_frame.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

    start = Image.open("images/start1.png")
    # width,height
    start = start.resize((150, 50), Image.ANTIALIAS)
    photoImg = ImageTk.PhotoImage(start)

    my_button = Button(ss_frame,
                       image=photoImg,
                       borderwidth=0,
                       bg='gray5',
                       width=150,
                       height=50,
                       activebackground="#2a2c32")
    my_button.pack(fill=X, side=LEFT, padx=5)

    stop = Image.open("images/stop1.png")
    # width,height
    stop = stop.resize((150, 50), Image.ANTIALIAS)
    photoImg2 = ImageTk.PhotoImage(stop)

    my_button = Button(ss_frame,
                       image=photoImg2,
                       borderwidth=0,
                       bg='gray5',
                       width=150,
                       height=50,
                       activebackground="#2a2c32")
    my_button.pack(fill=X, side=RIGHT, padx=5)

    r_label = Label(right_frame,
                    text="Rover Controller",
                    bd=5,
                    bg=myyellow,
                    fg=myblack,
                    relief=SUNKEN,
                    font="Verdana 15 bold",
                    anchor=CENTER
                    )
    r_label.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)

    rover = Frame(right_frame, bg='gray5')
    rover.grid(row=2, column=0)

    '''rover button'''
    left = PhotoImage(file='images/circle_blue.png')
    right = PhotoImage(file='images/circle_blue.png')
    front = PhotoImage(file='images/circle_blue.png')
    rear = PhotoImage(file='images/circle_blue.png')

    r_left = Button(rover, command=rb_left, image=left, borderwidth=0, bg='gray5', activebackground="#2a2c32")
    r_right = Button(rover, command=rb_right, image=right, borderwidth=0, bg='gray5', activebackground="#2a2c32")
    r_front = Button(rover, command=rb_front, image=front, borderwidth=0, bg='gray5', activebackground="#2a2c32")
    r_rear = Button(rover, command=rb_rear, image=rear, borderwidth=0, bg='gray5', activebackground="#2a2c32")

    r_left.pack(side=LEFT, padx=5)
    r_right.pack(side=RIGHT, padx=5)
    r_front.pack(side=TOP, pady=5)
    r_rear.pack(side=BOTTOM, pady=5)





    a_label = Label(right_frame,
                    text="Arm Controller",
                    bd=5,
                    bg=myyellow,
                    fg=myblack,
                    relief=SUNKEN,
                    font="Verdana 15 bold",
                    anchor=CENTER,
                    )
    a_label.grid(row=3, column=0, sticky='nsew', pady=25, padx=10)

    arm = Frame(right_frame, bg='gray5')
    arm.grid(row=4, column=0)
    # hline = Frame(right_frame, bg='white')

    '''arm button'''

    ileft = PhotoImage(file='images/circle_grey.png')
    iright = PhotoImage(file='images/circle_grey.png')
    ifront = PhotoImage(file='images/circle_grey.png')
    irear = PhotoImage(file='images/circle_grey.png')

    a_left  = Button(arm, image=ileft, command=ab_left, borderwidth=0, bg='gray5', activebackground="#2a2c32")
    a_right = Button(arm, image=iright, command=ab_right, borderwidth=0, bg='gray5', activebackground="#2a2c32")
    a_front = Button(arm, image=ifront, command=ab_front, borderwidth=0, bg='gray5', activebackground="#2a2c32")
    a_rear  = Button(arm, image=irear, command=ab_rear, borderwidth=0, bg='gray5', activebackground="#2a2c32")

    a_left.pack(side=LEFT, padx=5)
    a_right.pack(side=RIGHT, padx=5)
    a_front.pack(side=TOP, pady=5)
    a_rear.pack(side=BOTTOM, pady=5)


    '''frames for video output'''

    frame1 = Frame(center_frame,
                      bg="#383838",
                      bd=10,
                      width=310,
                      height=315,
                      cursor="target")
    frame1.grid(row=0, column=1, sticky='nsew', pady=5, padx=5)

    frame2 = Frame(center_frame,
                   bg="#383838",
                   bd=10,
                   width=310,
                   height=315,
                   cursor="target")
    frame2.grid(row=1, column=0, sticky='nsew',pady=5, padx=5 )

    frame3 = Frame(center_frame,
                   bg="#383838",
                   bd=10,
                   width=310,
                   height=315,
                   cursor="target")
    frame3.grid(row=1, column=1, sticky='nsew',pady=5, padx=5)

    frame4 = Frame(center_frame,
                   bg="#383838",
                   bd=10,
                   width=310,
                   height=315,
                   cursor="target")
    frame4.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

    status_label = Label(btm_frame, text="",
                         relief=SUNKEN,
                         font="ComicSansMs 10",
                         fg='linen',
                         bg='gray3',
                         bd=0.5,
                         anchor=W)
    status_label.pack(fill=X, side=LEFT)
    # status_label.grid(row=0,column=0)

    status_label2 = Label(btm_frame, text="",
                         relief=SUNKEN,
                         font="ComicSansMs 10",
                         fg='linen',
                         bg='gray3',
                         bd=0.5,
                         anchor=W)
    status_label2.pack(fill=X, side=RIGHT)

    '''elements of tab2'''

    tab2_top_frame = Frame(tab2, bg='black', relief=SUNKEN)
    tab2_center = Frame(tab2, bg='gray2', relief=SUNKEN)
    tab2_btm_frame = Frame(tab2, bg='white', relief=SUNKEN)

    tab2_top_frame.grid(row=0, sticky="ew")
    tab2_center.grid(row=1, sticky="nsew")
    tab2_btm_frame.grid(row=3, sticky="ew")

    tab2.grid_rowconfigure(1, weight=1)
    tab2.grid_columnconfigure(0, weight=1)

    '''top frame------frames for photo output'''

    tab2frame1 = Frame(tab2_top_frame,
                   bg="#383838",
                   bd=10,
                   width=310,
                   height=315,
                   cursor="target")
    tab2frame1.grid(row=0, column=0, sticky='nsew', pady=5, padx=10)

    tab2frame2 = Frame(tab2_top_frame,
                   bg="#383838",
                   bd=10,
                   width=310,
                   height=315,
                   cursor="target")
    tab2frame2.grid(row=0, column=1, sticky='nsew', pady=5, padx=10)

    tab2frame3 = Frame(tab2_top_frame,
                   bg="#383838",
                   bd=10,
                   width=310,
                   height=315,
                   cursor="target")
    tab2frame3.grid(row=0, column=2, sticky='nsew', pady=5, padx=4)

    tab2_left_frame = Frame(tab2_center, bg="gray5", relief=SUNKEN, width=660 )
    tab2_left_frame.pack(fill=BOTH, side=LEFT, padx=10)

    tab2_right_frame = Frame(tab2_center, bg="gray5", relief=SUNKEN,width=440)
    tab2_right_frame.pack(fill=BOTH, side=RIGHT,  padx=10)
    # tab2_right_frame.mi

    tab2_control_label = Label(tab2_left_frame,
                               text="Controls",
                               bd=5,
                               bg=myyellow,
                               fg=myblack,
                               relief=SUNKEN,
                               font="Verdana 15 bold",
                               anchor=CENTER
                               )
    tab2_control_label.pack(fill=X, side=TOP)

    tab2_control_label = Label(tab2_right_frame,
                               text="DATA",
                               bd=5,
                               bg=myyellow,
                               fg=myblack,
                               relief=SUNKEN,
                               font="Verdana 15 bold",
                               anchor=CENTER
                               )
    tab2_control_label.pack(fill=X, side=TOP, padx=(5, 2))


    door=Frame(tab2_left_frame, bg="gray5", relief=SUNKEN, )
    door.pack(fill=BOTH,  padx=10)

    openimg = PhotoImage(file='images/green.gif')
    d_open = Button(door, command=open_s, image=openimg, borderwidth=0, bg='gray5', activebackground="#2a2c32")
    d_open.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

    door_status = Text(door, height=3, width=15,
                       relief=RAISED,
                       font="ComicSansMs 10",
                       fg='linen',
                       bg='gray3',
                       bd=0.1,
                       )
    door_status.tag_configure('tag-center', justify='center')

    # door_status = Label(door, bg='white', text="door is closed")
    door_status.grid(row=0, column=1,)
    fontStatus = tkFont.Font(family="Arial", size=16, weight="bold", )

    door_status.insert(END,"Door status:- \n......................")
    door_status.configure(font=fontStatus, state='disabled')

    closeimg = PhotoImage(file='images/circle_red.png')
    d_close = Button(door, command=close_s, image=closeimg, borderwidth=0, bg='gray5', activebackground="#2a2c32")
    d_close.grid(row=0, column=2, sticky='nsew', pady=10, padx=5)
    #


    data=Frame(tab2_right_frame, bg="black", relief=SUNKEN )
    data.pack(fill=BOTH, padx=10)



    '''T = Text(root, bg, fg, bd, height, width, font,..)'''

    # text1 = Button(data, bg='white', height=1, width=15)
    text2 = Text(data, bg='white',  height=1, width=15)
    text3 = Text(data, bg='white', height=1, width=15)
    text4 = Text(data, bg='white',  height=1, width=15)
    text6 = Text(data, bg='white',  height=1, width=15)
    text7 = Text(data, bg='white',  height=1, width=15)

    # clear = Button(data,text="clear", bg='white', activebackground="#2a2c32",height=1, width=15)
    # text1.grid(row=0, column=0,)
    text2.grid(row=1, column=0, )
    text3.grid(row=2, column=0, )
    text4.grid(row=3, column=0, )
    # clear.grid(row=7, column=0, )
    text6.grid(row=5, column=0, )
    text7.grid(row=6, column=0, )

    # text1.insert(END, "colour")
    text2.insert(END, "Texture")
    text3.insert(END, "Dimension_X")
    text4.insert(END, "Dimension_Y")
    # clear.insert(END, "Dimension_Z")
    text6.insert(END, "Temperature")
    text7.insert(END, "Weight")

    # data from image
    fontExample = tkFont.Font(family="Arial", size=16, weight="bold", slant="italic")

    # text1.configure(state="disabled", font=fontExample)
    text2.configure(state="disabled",font=fontExample)
    text3.configure(state="disabled",font=fontExample)
    text4.configure(state="disabled",font=fontExample)
    # text5.configure(state="disabled",font=fontExample)
    text6.configure(state="disabled",font=fontExample)
    text7.configure(state="disabled",font=fontExample)



    # e_text1 = Text(data, bg='white', height=1, width=15)
    e_text2 = Text(data, bg='white',  height=1, width=15)
    e_text3 = Text(data, bg='white', height=1, width=15)
    e_text4 = Text(data, bg='white',  height=1, width=15)
    # e_text5 = Text(data, bg='white',  height=1, width=15)
    e_text6 = Text(data, bg='white',  height=1, width=15)
    e_text7 = Text(data, bg='white',  height=1, width=15)
    # clear = Button(text="clear", bg='white', activebackground="#2a2c32")

    # e_text1.grid(row=0, column=1,)
    e_text2.grid(row=1, column=1, )
    e_text3.grid(row=2, column=1, )
    e_text4.grid(row=3, column=1, )
    # e_text5.grid(row=4, column=1, )
    e_text6.grid(row=5, column=1, )
    e_text7.grid(row=6, column=1, )

    e_text2.configure(font=fontExample)
    e_text3.configure(font=fontExample)
    e_text4.configure(font=fontExample)
    # e_text5.configure(font=fontExample)
    e_text6.configure(font=fontExample)
    e_text7.configure(font=fontExample)




    capture = Image.open("images/metal_button.png")
    # width,height
    capture = capture.resize((250, 100), Image.ANTIALIAS)
    cap_img = ImageTk.PhotoImage(capture)


    # cap_img = PhotoImage(file='images/metal_button.png')
    click = Button(tab2_left_frame, command=ok, image=cap_img, borderwidth=0, bg='gray5', activebackground="#2a2c32")
    click.pack(expand=TRUE, padx=10)


    image_s = Label(tab2_btm_frame, text=(f"{dt.datetime.now():%a, %b %d %Y}"),
                         relief=SUNKEN, font="ComicSansMs 10", fg='linen', bg='gray3', bd=0.5, anchor=W)
    image_s.pack(fill=X, side=BOTTOM)

    # elements of tab2 ended

    root.mainloop()
