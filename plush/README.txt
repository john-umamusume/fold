v9.5 update

major changes to images format
compression and decompression
readme changes

the folder will now contain all the compressed webp formatted images in a zip archive, alongside the python compress.py and decompress.py codes used with requirements.txt
you can either just extract the zip file, which the images will be in webp format, or you can decompress them by the code provided, you do not need to use compress.py if you only wish to get the current repository images
due to the webp format being able to cause some issues with specific software, the decompress.py will read the zip file and convert all images to jpeg format, may increase storage usage


the compress.py code in this state will not work in your pc due to the lack of the original images folder, however if you wish to compress your own images, follow these steps:

1. leave a folder named "images" as a sibling of the folder "plush" (i.e: C:/Users/Downloads/images and C:/Users/Downloads/plush)
2. open a terminal and find the directory of the "plush" folder, alternatively you can use an IDE like Vscode to run it
3. in the cmd type "  python -m pip install -r requirements.txt  " in order to download the Pillow library
4. you can use the same console as before typing "  python compress.py  " or just run through the aforementioned IDE

notes: 
every time the compress.py code is executed, it will replace the previous zip file in this folder
decompress.py will not replace the entire "decompressed" folder, it will only replace the ones that are in both files
before trying with your own, remember to save somewhere else the current compressed images in this repository
the python code will not modify any of your files outside of the "plush" directory, it only creates the compressed and decompressed ones in this folder
compressed images may have reduced visual quality due to obvious reasons

i dont even know why im doing this


yea