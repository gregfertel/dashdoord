var directions = {L11N: "Manhattan", L11S: "Rockaway Parkway"}

var fillCryptos = function() {
    $.get('crypto', function(data) {
        cryptoData = JSON.parse(data)
        $("#bitcoin_price").html(cryptoData['Bitcoin']['price'] + ' (' + cryptoData['Bitcoin']['change'] + '%)')
        $("#ethereum_price").html(cryptoData['Ethereum']['price'] + ' (' + cryptoData['Ethereum']['change'] + '%)')
    })
}
fillCryptos()

var replaceCitibike = function() {
    $.get( "citibike?latitude=" + latitude + "&longitude=" + longitude, function( data ) {
        citibikeData = JSON.parse(data)
        var content = ''
        for (var i = 0; i < citibikeData.length; i++) {
            var row = citibikeData[i]
            content += '<tr>'
            content += '<td>' + row['stationName'] + '</td>'
            content += '<td>' + row['availableBikes'] + '</td>'
            content += '<td>' + row['availableDocks'] + '</td>' 
            content += '<td>' + row['distance'] + '</td>'
            content += '</tr>'
        $("#citibike_body").html(content)
    }
    });
}

var replaceSubway = function () {
    $.get("subway", function (data) {
        subwayData = JSON.parse(data)
        for (var subway in subwayData) {
            var content = ''
            var directionData = subwayData[subway].slice(0, 4)
            for (var i = 0; i < directionData.length; i++) {
                content += '<tr><td><img height="40" src="static/ltrain.png" alt="L Train Logo"></td>'
                content += '<td>' + directions[subway] + '</td>'
                content += '<td>' + directionData[i] + " Minutes</td></tr>"
            }
            $("#" + subway + "_body").html(content)
        }
    })
}

var updateTime = function() {
    var time = new Date();
    var currentTime = time.toLocaleString('en-US', 
        { hour: 'numeric', hour12: true, 'minute': 'numeric', 'second': 'numeric' });
    $("#current_time").html(currentTime)
}


var cssInject = function () { 
// the css we are going to inject
var css = 'html {-webkit-filter: invert(100%);' +
    '-moz-filter: invert(100%);' + 
    '-o-filter: invert(100%);' + 
    '-ms-filter: invert(100%); }',

head = document.getElementsByTagName('head')[0],
style = document.createElement('style');

// a hack, so you can "invert back" clicking the bookmarklet again
if (!window.counter) { window.counter = 1;} else  { window.counter ++;
if (window.counter % 2 == 0) { var css ='html {-webkit-filter: invert(0%); -moz-filter:    invert(0%); -o-filter: invert(0%); -ms-filter: invert(0%); }'}
 };

style.type = 'text/css';
if (style.styleSheet){
style.styleSheet.cssText = css;
} else {
style.appendChild(document.createTextNode(css));
}

//injecting the css to the head
head.appendChild(style);
}
//cssInject()
function hideAddressBar(){
  if(document.documentElement.scrollHeight<window.outerHeight/window.devicePixelRatio)
    document.documentElement.style.height=(window.outerHeight/window.devicePixelRatio)+'px';
  setTimeout(window.scrollTo(1,1),0);
}
window.addEventListener("load",function(){hideAddressBar();});
window.addEventListener("orientationchange",function(){hideAddressBar();});

// Setting Subways to update every minute
window.setInterval(function(){
    updateTime()
    replaceSubway()
}, 60000);

// Setting Citibike to Update every 5 minutes
window.setInterval(function(){
    replaceCitibike()
}, 300000);

// Setting weather and cryptos to update every 15 minutes
window.setInterval(function(){
    document.getElementById("forecast_embed").src += ''
    fillCryptos()
}, 900000);