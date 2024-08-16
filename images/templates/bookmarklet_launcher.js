/* 
This is a launcher script. It checks whether the bookmarklet has already been loaded
by checking the value of the bookmarklet window variable with if(!window.bookmarklet).
This prevents the bookmarklet from being loaded more than once if the user clicks on the 
bookmarklet repeatedly.
Using the launcher code allows to update the bookmarklet code at any time without requiring users
to change the previously added to the browser bookmark.
*/

(function(){
    if(!window.bookmarklet) {
        bookmarklet_js = document.body.appendChild(document.createElement('script'));

        // The scr attr is used to load the URL of the bookmarklet.js script with a random 16-digit integer parameter generated with Math.random()
        // Using the random number prevents the browser from loading the file from the browser's cache.
        bookmarklet_js.src = '//127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*9999999999999999);
        window.bookmarklet = true;
    }
    else {
        bookmarkletLaunch(); // if window.bookmarklet is defined and has a truthy value, the launch is executed
    }
})();