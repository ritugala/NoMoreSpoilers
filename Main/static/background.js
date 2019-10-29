chrome.runtime.onInstalled.addListener(function() {
   chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
     chrome.declarativeContent.onPageChanged.addRules([{
       conditions: [new chrome.declarativeContent.PageStateMatcher({
         pageUrl: {hostEquals: 'developer.chrome.com'},
       })
       ],
           actions: [new chrome.declarativeContent.ShowPageAction()]
     }]);
   });
 });

 chrome.storage.onChanged.addListener(function(changes, namespace) {
         for (var key in changes) {
           var storageChange = changes[key];
           console.log('Storage key "%s" in namespace "%s" changed. ' +
                       'Old value was "%s", new value is "%s".',
                       key,
                       namespace,
                       storageChange.oldValue,
                       storageChange.newValue);
         }
       });
