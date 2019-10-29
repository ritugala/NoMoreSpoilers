//document.addEventListener('DOMContentLoaded', documentEvents , false);



// function documentEvents() {
//   document.getElementById('sub').addEventListener('click', function()
//     {
//     var series = document.getElementById('Series').value;
//     console.log(series);
//     series = series.split(' ').join('_');
//     var season = document.getElementById('Season').value;
//     var url = '';
//     url = url.concat('https://en.wikipedia.org/wiki/',series,'_(season_',season,')');
//     console.log(url);
//
//   });
// }


$(document).ready(function()
{
     $('form').on('submit', function(event)
      {
        console.log('sending data');
         $.ajax({
            data : {
               Series : $('#Series').val(),
               Season: $('#Season').val(),
                   },
               type : 'POST',
               url : 'http://127.0.0.1:5000/index'
              })
          .done(function(data)
          {
            chrome.storage.sync.set({keywords:data.keywords}, function()
            {
              console.log('Data is set');
              console.log('Data is: '+data.keywords);
            })
          });
        event.preventDefault();
      });
    });
