v9 update

webp conversion

the folder will now contain all the images in reduced webp format, alongside the python compress.py and decompress.py codes used with requirements.txt

optional: 
due to the webp format being able to cause some issues with specific software, the decompress.py will read the zip file and restore the images to its original format, may increase storage usage

the code in this state will not work in your pc due to the lack of the original images folder, however you can try it with your own images:

1. leave a folder named "images" within the same directory as the folder "plush" (i.e: C:/Users/Downloads/images and C:/Users/Downloads/plush)
2. open a console tab and find the directory of the "plush" folder, alternatively you can use an IDE like Vscode to run it
3. in the cmd type "  python -m pip install -r requirements.txt  " in order to download the Pillow extension
4. the code will now properly work, you can use the same console as before typing "  python compress.py  "

notes: 
every time the code is executed, it will replace the previous zip file in this folder
before trying with your own, remember to save somewhere else the current zip file in this repository
the python code will not modify any of your files, it only creates the compressed one
webp images in your folder will not be recompressed
compressed images may have reduced visual quality due to obvious reasons

i dont even know why im doing this


yea
