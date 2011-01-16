// Javascript for the entire project

$.extend({
  urlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++) {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = unescape(hash[1]);
    }
    return vars;
  },
  urlVar: function(name){
    return $.urlVars()[name];
  }
});