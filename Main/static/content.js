

chrome.storage.sync.get(['keywords'], function(result) {
  console.log('Keywords are:'+result.keywords);
  var word = 'Joey';
  var queue = [document.body], curr;
  while (curr = queue.pop()) {
      if (!curr.textContent.match(word)) continue;
      for (var i = 0; i < curr.childNodes.length; ++i) {
          switch (curr.childNodes[i].nodeType) {
              case Node.TEXT_NODE :
                  if (curr.childNodes[i].textContent.match(word)) {
                      console.log("Found!");
                      var cl = curr.className;
                      var idd = curr.id;
                      if(idd)
                      {
                        console.log("ID is "+id)
                        document.getElementById(idd).style.color = "transparent";
                        document.getElementById(idd).style.textShadow = "0 0 10px rgba(0,0,0,0.5)";
                      }
                      else if (cl) {
                        console.log("Class Name is "+cl)
                        var cl_array = document.getElementsByClassName(cl);
                        for(var i=0; i<cl_array.length; i++)
                        {
                          if(cl_array[i].textContent.match(word))
                          {
                            cl_array[i].style.color = "transparent";
                            cl_array[i].style.textShadow = "0 0 10px rgba(0,0,0,0.5)";
                            break;
                          }
                        }

                      }
                  }
                  break;
              case Node.ELEMENT_NODE :
                  queue.push(curr.childNodes[i]);
                  break;
          }
      }
  }

})
