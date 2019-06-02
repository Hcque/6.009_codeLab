#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def get_pixel(self, x, y):
        return self.pixels[(y-1)*self.width + x-1]       
    
    def set_pixel(self, x, y, c):
        self.pixels[(y-1)*self.width + x-1] = c

    def apply_per_pixel(self, func):
        result = Image.new(self.width, self.height)
        for x in range(1,result.width+1):
            for y in range(1,result.height+1):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor)
        return result

    def inverted(self):
        return self.apply_per_pixel(lambda c: 255-c)
    
    # Handle with edge effect.
    def get_extended_pixel(self, m):
        """return (extended  image)"""
        # row extension
        res = []
        for j in range(self.height):
            a = 0 + j*self.width
            b = self.width + j*self.width
            row = self.pixels[a:b] # extract each row
            new_row = [row[0]]*m + row + [row[-1]]*m 
            res = res + new_row
        # add upward and downward rows
        firs_row = res[:self.width+2*m]
        last_row = res[-(self.width+2*m):]
        
        res = firs_row*m + res + last_row*m
        return Image(self.width+2*m, self.height+2*m, res)
    
    # Clip not well behaviored pixels.
    def clip(self,p):
        if p < 0:
            return 0
        if p > 255:
            return 255
        else:
            return int(round(p))

    # Apply 3*3 kernel.
    def kernel_3(self, ker):
        using_im = self.get_extended_pixel(1)
        result = Image.new(self.width, self.height)
        for x in range(1,result.width+1):
            for y in range(1,result.height+1):
                # create subimage
                sub_im = []
                for j in range(-1,2):
                    for i in range(-1,2):
                        sub_im.append(using_im.get_pixel(x+1+i, y+1+j))
                newcolor = 0
                for k in range(len(ker)):
                    newcolor = newcolor + ker[k]*sub_im[k]
                result.set_pixel(x, y, self.clip(newcolor))
        return result
    
    # Apply abrbitary kernel.
    def apply_kernel(self, ker, if_clip = True):
        ker_size = math.sqrt(len(ker))
        m = int((ker_size-1)/2) # extend number
        using_im = self.get_extended_pixel(m)
        result = Image.new(self.width, self.height)
        for x in range(1,result.width+1):
            for y in range(1,result.height+1):
                # create subimage
                sub_im = []
                for j in range(-m,m+1):
                    for i in range(-m,m+1):
                        sub_im.append(using_im.get_pixel(x+m+i, y+m+j))
                newcolor = 0
                for k in range(len(ker)):
                    newcolor = newcolor + ker[k]*sub_im[k]
                if if_clip:
                    result.set_pixel(x, y, self.clip(newcolor))
                else:
                    result.set_pixel(x, y, newcolor)
        return result
    
    def blurred(self, n):
        ker = [1/(n*n)]*(n*n)  # blur kernel
        return self.apply_kernel(ker)
    
    def sharpened(self, n):
        ker = [-1/(n*n)]*(n*n)
        center = int((n*n-1)/2)
        ker[center] = 2 - 1/(n*n)
        return self.apply_kernel(ker)
    
    def edges(self):
        K_x = [-1,0,1,
               -2,0,2,
               -1,0,1] 
        O_x = self.apply_kernel(K_x, if_clip=False)
        K_y = [-1,-2,-1,
               0,0,0,
               1,2,1]
        O_y = self.apply_kernel(K_y, if_clip=False)
        
        result = Image.new(self.width, self.height)
        for x in range(1,self.width+1):
            for y in range(1,self.height+1):
                O_x_pixel = O_x.get_pixel(x, y)
                O_y_pixel = O_y.get_pixel(x, y)
                newcolor = math.sqrt(O_x_pixel**2 + O_y_pixel**2)
                result.set_pixel(x, y, self.clip(newcolor))
        return result
    
    # Helper functions
    def get_sum(self, L):
        ans = 0
        for i in L:
            ans = ans + i
        return ans
    
    def get_minIdx(self, L):
        min = L[0]
        min_idx = 0
        for i in range(len(L)):
            if L[i] < min:
                min = L[i]
                min_idx = i
        return min_idx
    
    def del_min(self, L, idx):
        L1 = L[:idx]
        L2 = L[idx+1:]
        return L1 + L2
    
    def get_row(self, j):
        return self.pixels[(j-1)*self.width:j*self.width]
    
    def get_col(self, i):
        ans = []
        for k in range(1, self.height+1):
            row = self.get_row(k)
            ans.append(row[i-1])
        return ans
    # End help functions
    
    def rescale(self):
        # computer energy
        energy_im = self.edges()
        energy = []
        for x in range(1, self.width+1):
            col = energy_im.get_col(x)
            energy.append(self.get_sum(col))            
        # get min index
        min_idx = self.get_minIdx(energy)
        # delete min column
        new_pixels = []
        for y in range(1, self.height+1):
            row = self.get_row(y)
            new_row = self.del_min(row, min_idx)
            new_pixels = new_pixels + new_row
        return Image(self.width-1, self.height, new_pixels)
    
    def rescale_pic(self, num):
        im = self.rescale()
        for i in range(num-1):
            im = im.rescale()
        return im         
    
    
    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
#    im = Image.load('test_images/twocats.png')
#    
#    K_x = [-1,0,1,
#           -2,0,2,
#           -1,0,1] 
#    O_x = im.apply_kernel(K_x)
#    O_x.show()
#    K_y = [-1,-2,-1,
#           0,0,0,
#           1,2,1]
#    O_y = im.apply_kernel(K_y)
#    O_y.show()
    
    
    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
