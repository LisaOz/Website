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
var body = docuement.getElementsByTagName('body')[0];
boxHtml =
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a> 
        <h1>Select an image to bookmark:</h1>
        <div class="images"></div>
    </div>;
body.innerHTML += boxHtml;

function bookmarkletLaunch() {  
    bookmarklet = document.getElementById('bookmarklet');
    var ImagesFound = bookmarklet.querySelector('.images');

    // clear images found
    ImagesFound.innerHTML = '';
    // display bookmarklet
    bookmarklet.style.display = 'block';
    // close element
    bookmarklet.querySelector('#close')
                .addEventListener('click', function(){
                    bookmarklet.style.display = 'none'
                });
}
// Launch the bookmarklet
bookmarkletLaunch();