#ifndef LIB_H
#define LIB_H

#ifndef LIB_API
	#ifdef LIB_EXPORTS
		#define LIB_API __attribute__((visibility("default")))
	#else
		#define LIB_API
	#endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

LIB_API void saveImage(unsigned char* data, int h, int w);

#ifdef __cplusplus
}
#endif


#endif //LIB_H
