var Vue = require('vue');
var request = require('superagent');

var data = {
  experiments:['wowee', 'wwww'],
  empty: false
};

var app = new Vue({
  el:'#app',
  data: data
});

console.log('New vue instance formed');

app.start();
