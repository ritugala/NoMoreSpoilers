

chrome.storage.sync.get(['keywords'], function(result) {
  console.log('Keywords are:'+result.keywords);

  for(var j=0; j<result.keywords.length; j++)
  {
    var word = result.keywords[j];
    console.log('This is word:'+word);
    var queue = [document.body], curr;
    while (curr = queue.pop()) {
        if (!curr.textContent.match(word)) continue;
        for (var i = 0; i < curr.childNodes.length; ++i) {
            switch (curr.childNodes[i].nodeType) {
                case Node.TEXT_NODE :
                    var temp = curr.childNodes[i].textContent.toLowerCase()
                    if (temp.match(word)) { ////This needs to be refined
                        console.log("Found!");
                        console.log(curr.childNodes[i].textContent)
                        var cl = curr.className;
                        var idd = curr.id;
                        var tag  = curr.tagName;
                        // if(idd)
                        // {
                        //   console.log("ID is "+id)
                        //   document.getElementById(idd).style.color = "transparent";
                        //   document.getElementById(idd).style.textShadow = "0 0 10px rgba(0,0,0,0.5)";
                        //   break;
                        // }
                        // else if (cl) {
                        //   console.log("Class Name is "+cl)
                        //   var cl_array = document.getElementsByClassName(cl);
                        //   for(var z=0; z<cl_array.length; z++)
                        //   {
                        //     if(cl_array[z].textContent.match(word))
                        //     {
                        //       cl_array[z].style.color = "transparent";
                        //       cl_array[z].style.textShadow = "0 0 10px rgba(0,0,0,0.5)";
                        //       break;
                        //     }
                        //   }
                        console.log("Tag Name is "+tag)
                        var tag_array = document.getElementsByTagName(tag);
                        for(var z=0; z<tag_array.length; z++)
                        {
                          if(tag_array[z].textContent.match(word))
                          {
                            //tag_array[z].style.color = "transparent";
                            tag_array[z].style.textShadow = "0 0 10px rgba(255,0,0,1)";
                            break;
                            console.log('Style applied!')
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
  }
});
