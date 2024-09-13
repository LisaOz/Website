const siteUrl = '//127.0.0.1:8000/'; // the base Url for the website 
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWidth = 250; // min width of the images that the bookmarklet will collect from the site
const minHeight = 250;

// Load css
var head = document.getElementsByTagName('head')[0];
var link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
head.appendChild(link);

// load HTML
var body = document.getElementsByTagName('body')[0];

// Define the HTML content as a string
boxHtml = `
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a> 
        <h1>Select an image to bookmark:</h1>
        <div class="images"></div>
    </div>
`;

// Append the HTML to the body
body.innerHTML += boxHtml;

// The bookmarklet launcher function
function bookmarkletLaunch() {  
    bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');

    // clear images found
    imagesFound.innerHTML = '';
    // display bookmarklet
    bookmarklet.style.display = 'block';
    // close event
    bookmarklet.querySelector('#close')
                .addEventListener('click', function(){
                    bookmarklet.style.display = 'none'
                });


    // Find images in the DOM (document object model) with the minimum dimensions
    images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
    images.forEach(image => {
        if(image.naturalWidth >= minWidth
            && image.naturalHeight >= minHeight)
            {
                var imageFound = document.createElement('img');
                imageFound.src = image.src;
                imagesFound.append(imageFound);
            }        
    })

/*
Function that allows user to click on the desired image to bookmark it.
*/

// Select image event
imagesFound.querySelectorAll('img').forEach(image => {
    image.addEventListener('click', function(event){ // click event is attached to each element within the ImageFound container
        imageSelected = event.target; // every clicked image is stored in the imageSelected variable
        bookmarklet.style.display = 'none'; // the bookmarklet is hidden by setting display property to 'none'
        window.open(siteUrl + 'images/create/?url=' // a new browser window is opened with the URL to bookmark a new image on the site
            + encodeURIComponent(imageSelected.src)
            + '&title='
            + encodeURIComponent(document.title),
            '_blank');
        })
    })
}
// Launch the bookmarklet
bookmarkletLaunch();

