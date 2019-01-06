ElmalzmaDechiper
=======
ElmalzmaDechiper is a python script that removes the annoying watermark that is typically found at your studying sheets using OpenCV

## Running the script (basic instructions)
* you need to install python 3 
* run pip install -r requirements.txt to install required python packages

## Usage
```
python filterwm.py -p | -f | -s target -t threshold -i iterations
```
```
Options:
     -p              Process images in pdf file named `target`
     -f              Process images in folder named `target`
     -s              Process single image file named `target`
     -t threshold    Thershold level [0-255] to apply binarization on at the watermark area
     -i iterations   Number of iterations in the watermark detection using Opening/Closing  Morphological process
```

## Examples
```bash
python filterwm.py -s 1.jpg -t 53 -i 9
```

<img src="https://github.com/KarimAshraf1995/ElmalzmaDechiper/blob/master/examples/1.jpg?raw=true" width="25%" />


<img src="https://github.com/KarimAshraf1995/ElmalzmaDechiper/blob/master/examples/output_20190106184915/1.jpg?raw=true" width="25%" />


```bash 
python filterwm.py -s 2.jpg -t 53 -i 15
```

<img src="https://github.com/KarimAshraf1995/ElmalzmaDechiper/blob/master/examples/2.jpg?raw=true" width="25%" />


<img src="https://github.com/KarimAshraf1995/ElmalzmaDechiper/blob/master/examples/output_20190106184915/2.jpg?raw=true" width="25%" />

## Limitions 
* Thershold level and number of iterations must be entered and they depend on the condition of the scanning. The best way to find the best values is trial and error. Typical values for thershold is in range 45 - 75 and 5 - 15 for number of iterations for good quality images

* The script does not detect the edges of the paper. Please crop the images to include the paper only

* The script will not work if the page is already copied, or the image is in grayscale or taken by a mobile phone in low light


