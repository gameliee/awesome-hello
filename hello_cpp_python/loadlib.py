#!python3
from ctypes import *
import numpy as np
import cv2

lib = CDLL("/home/dat/source/hello_cpp_python/libfoo.so", RTLD_GLOBAL)

saveImage = lib.saveImage
saveImage.argtypes= [POINTER(c_ubyte), c_int, c_int]
saveImage.restype = c_void_p


if __name__ == '__main__':
	mat = cv2.imread("/home/dat/Pictures/10.jpg")
	h, w, c = mat.shape
	mat_p = mat.ctypes.data_as(POINTER(c_ubyte))
	saveImage(mat_p, h, w)
