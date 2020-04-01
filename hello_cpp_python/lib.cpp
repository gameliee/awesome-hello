#include "lib.hpp"
#include <opencv2/opencv.hpp>

LIB_API void saveImage(unsigned char*data, int h, int w)
{
	cv::Mat mat(cv::Size(w, h), CV_8UC3, data);
	cv::imwrite("image.jpg", mat);
}