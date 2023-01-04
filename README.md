# ColorMaskMap

# What does it do?
This program provides an easy way to recolor parts of an image. If you have the color masks defined, you can simply set colors in the "Colors" image and run the script to apply the colors to the image. This is intended to be used for game modding (hence the use of DDS textures).

Here's a quick demo of what it can do. We start with the diffuse image, the color mask map (CMM) and the selected color image. We also have a ColorMasks.txt file to set what images to use. When we run the code, we get the output image shown.
![alt text](https://github.com/Arsinia/ColorMaskMap/blob/main/PicturesForREADME/ColorMaskMapExample.png?raw=true)

All the end user has to do is change the colors file (just 3 pixels) and they can change what colors get applied

# How do I use it?
#### I installed a mod that uses this
If you downloaded a mod that uses this, all you need to do is change the colors of the selected colors file(s) and run the ApplyColorMask.exe or ApplyColorMask.py. The three colors will determine what color gets applied to the image. If you look at the CMM file, the first color will be applied to the red section, second to green, and third to blue. If you set the color to pure white (255,255,255) the color will not be applied to that section. This means if you want the section to be white, it needs to be slightly off-white. 

#### I'm making a mod with this
If you want to make a mod using this, you need to get ApplyColorMask.exe from the releases section or ApplyColorMask.py. You the need to put [texconv.exe](https://github.com/Microsoft/DirectXTex/wiki/Texconv) into the same folder. You can the make a CMM using whatever image editing app you want. Finally you will need to make a file called "ColorMasks.txt" in the same folder as the program. This file will define what image gets used and where it is written to. Here is a quick example:

"Input.dds Output.dds CMM.png Colors.png"

In this case, we're taking Input.dds, changing it using CMM.png and Colors.png, and writing to Output.dds. You can specify multiple lines in a single ColorMasks.txt file and each line can have more pairs of CMM and selected color if you want to apply more than 3 colors. In this case it would look like this:

"Input.dds Output.dds CMM1.png Colors1.png CMM2png Colors2.png

It's also important to note that this code uses BC7 SRGB dds files with mip maps enabled. If you don't want your textures configured this way, you can pretty easily edit the code to do that

#### I don't want to run it as an EXE
EXE files can be a huge security risk if you don't trust where they came from. If you want to use this without an EXE, you can just run the Python file instead. Mods using this should provide the Python file for anyone who doesn't want to use EXEs. To run the Python file, you will need to install Python and the packages Numpy and ImageIO. Then you should be able to run it just like the EXE. You can also build the EXE yourself using Pyinstaller and running the build.bat file.

