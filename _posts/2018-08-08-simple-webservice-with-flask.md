---
layout: post
title: "A simple webservice with flask"
tags: python web
summary: Write a simple webservice with python and flask
date: 2018-08-08 08:08:08:00
---

This morning, a friend of mine asked me how to write a simple webservice with python. His aim was to use it with fastai models but I will keep it simple here. For such topics, I usually use django but for a single simple webservice, it is a bit too complicated. So I give it a try with flask and here is the result.

# The structure

Let's start by defining our URL and create a simple flask app. Put the following code in `app.py`:

{% highlight python %}
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
		# if POST method, return json response
		return jonify({
			"some_key": "some_value",
			})
    # if method == GET, render the html form
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

{% endhighlight %}

Here we are. If you run `flask run` from this file, you'll see an error because the `index.html` template is missing.

Let's fix this error right now! We will be starting with a simple HTML form, with only two inputs:

- File selector `type=file`
- Submit button `type=submit`

You can put this HTML code in your `templates/index.html` file:

{% highlight html %}
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
		<meta charset="UTF-8">
		<title>Image statistics</title>
		<meta name="viewport" content="width=device-width">
		<meta name="description" content="Image statistics">
	</head>
    <body>

	<h1>Image statistics</h1>
	<h2>with flask</h2>

	<form method="POST" enctype="multipart/form-data" action="{{ url_for('classify') }}" > 
		<div class="input-file-container">
			<label for="my-file" class="label-file">Select a file...</label>		
			<input class="input-file" id="my-file" type="file" name="image" multiple>
	    </div>
	    <p class="selected-file-name"></p>
	    <input type="submit">
	    <p><a href="" onclick="resetFile()">Reset files</a></p>
	</form>
    </body>
</html>
{% endhighlight %}


The submit button posts data to `/classify` URL, which will execute by our `classifiy` function thanks to the special `route` decorator.

Now, you can run `flask` and visit `http://127.0.0.1:5000`. You can also select some image and submit the form, you'll see our fixed JSON response.

Starting from now, you can adapt the form and view to your needs. 


# Read submitted images in python

In my case, I want to get some statistics about the image. So let's improve the view. First, we'll have to tell flask where to download the images. For that, you'll need to `pip install Flask-Uploads` and then:

{% highlight python %}
from flask_uploads import UploadSet, configure_uploads, IMAGES

images_upload_set = UploadSet('images', IMAGES)
app.config['UPLOADED_IMAGES_DEST'] = 'tmp_files'
configure_uploads(app, images_upload_set)
{% endhighlight %}

to download image in `tmp_dir` in your server.

To get some statistics about the image, we will use `numpy` and `PIL`:

{% highlight python %}
import os
import numpy as np

from PIL import Image

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        f = request.files["image"] # form input name
		# save image on disk in tmp location
		filename = images_upload_set.save(f)
		# get full image path on local disk
		file_path = images_upload_set.path(filename)
		# do things with image...
		# e.g. here, transform to numpy array through PIL
		im = Image.open(file_path)
		array_of_image = np.array(im) # array_of_image.shape: height x width x channel
		# remove temporary file
		os.remove(file_path)
		# return json response
		return jonify({
			"file": file_path,
			"shape": array_of_image.shape,
			# you can add more informations here if you want to
			})
    # if method == GET
    # render the html form
    return render_template('index.html')
{% endhighlight %}

Here we go! You can test this code with several images.


# Multiiple image selection

A nice feature is to be able to select and analyse multiple files. It is quite simple, firstly add `multiple` option to the file input. Then in the python view, replace :

    uploaded_files = request.files["image"]
    
with:

    uploaded_files = request.files.getlist("image")

and then you have to perform the analysis on each file with a loop:

     for f in uploaded_files:


# Error handling

When no images are selected, you can return an empty json, or display an error in the form. For the second solution, here is a way of doing it:

{% highlight python %}
def classify():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error="Please select at least one image")
{% endhighlight %}

And the error message can be displayed on the form:
{% highlight html %}
	<form method="POST" enctype="multipart/form-data" action="{{ url_for('classify') }}" > 
	    {% if error %}
	    <p class="error" >{{ error }}</p>
	    {% endif %}
{% endhighlight %}

# Style

Finally, I added some CSS style:

{% highlight css%}
body {
    background: #FCFDFD;
}
h1, h2 {
    margin-bottom: 5px;
    font-weight: bold;
    text-align: center;
    color: #205e94;
}
h2 {
    color: #4192d3;
}
form {
    width: 30%;
    margin: 4em auto 0;
    text-align:center;
}
h2 + P {
    text-align: center;
}
.input-file-container {  
}  
.input-file {
    display: none;
}
.label-file {
    display: block;
    width: 50%;
    margin: auto;
    line-height: 3.5em;
    background: #205e94;
    color: #fff;
    cursor: pointer;
}
.label-file:hover {
    background-color: #4192d3;
}
.selected-file-name {  
    font-style: italic;
    font-size: .8em;
}
a {
    color: #205e94;
    cursor: pointer;
}
a:hover {
    color: #4192d3;
}
.error {
    color: red;
}
{% endhighlight %}

 and a small JS code to show the name of the selected file to the user before submiting the form:

{% highlight javascript %}
var fileInput = document.querySelector( ".input-file" );
var label = document.querySelector(".label-file");
var selected_file_name_ul = document.querySelector(".selected-file-name");
var error = document.querySelector(".error");

// print file name when selected
fileInput.addEventListener( "change", function( event ) {
    label.innerHTML = "Change selected file";
    var files = this.files;
    for (var i = 0; i < files.length; i++) {
	 var li = document.createElement("li");
	 li.appendChild(document.createTextNode(files[i].name));
	 selected_file_name_ul.appendChild(li);
    }
    if (error) {
	 error.style.display = "none"; 
    };
});
{% endhighlight %}

# Reset selected files

You'll notice that once the multiple file selection is enabled, if you hit the select files button again, the first selected files will not be deleted but the new files are appended to them. You can add a reset button in your form, e.g. with:

{% highlight html %}
<p><a href="" onclick="resetFile()">Reset files</a></p>
{% endhighlight %}

and the corresponding JS:

{% highlight javascript %}
	function resetFile() {
	    const file = document.querySelector('.input-file');
	    file.value = '';
	}
{% endhighlight %}


# Conclusion

You'll notice we have done more than the initial requirement. If you just need the webservice, only the `app.py` file is needed, together with the `tmp_dir` directory. Final code in available here:

If you want to post image with the command line, you can use for example:

    curl -X POST -H "Content-Type: multipart/form-data" \
	    -F "image=@my_image.jpg" http://127.0.0.1:5000/classify
	
	
or using [httpie](https://httpie.org/):

    http -f POST http://127.0.0.1:5000/classify image@my_image.jpg

Finally, you can download a tarball with the final files [here](/downloads/simple_webservice_v2.tar.gz). Have fun!
