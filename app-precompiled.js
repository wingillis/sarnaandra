$(document).foundation();

var Vue = require('vue');
var request = require('superagent');

var data = {
  experiments:[],
  empty: true,
  api: {}
};

var app = new Vue({
  el:'#app',
  data: data,
  methods: {
    addExp: function() {
      // console.log(this.api.name);
      // console.log(this.api.description);
      request.post('/api/addExp').send(this.api).end();
      console.log('Sent experiment modal');
    }
  }
});

console.log('New vue instance formed');

// app.start();
