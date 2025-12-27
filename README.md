# how to use
First, ensure you have pillow ``python -m pip install Pillow``<br>
THEN, run the following<br>
```python grokblok.py <FILENAME>```

<br><br>Might eventually make a UI version.
# how this works
It just makes a gif, first frame is the image in the repo (or whatever you swap it to)<br>
The argument then, is used for frame 2, and frame 1024, the gif uses additive mode, so it just looks like one image.<br>It also saves up on storage, since my old method just did 256 images with replace mode.<br>
I tried to make it look decent, having 16 colors for the initial image, and 240 for the user's image.<br><br>If you know how to make this less crap, pull requests are open.
