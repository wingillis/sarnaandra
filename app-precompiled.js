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
      var ctx = this;
      request.post('/api/addExp').send(this.api)
      .end(function(err, res){
        ctx.experiments.push(res.body);
        // console.log(ctx.experiments);
        ctx.empty = false;
      });
      // console.log('Sent experiment modal');
    }
  }
});

function getEpxeriments() {
  request.get('/api/exp')
    .query('all=true').end(function(err, res) {
      if (res.body.res.length > 0) {
        data.empty = false;
      }
      data.experiments = res.body.res;
      // console.log(res.body.res);
    });
}

getEpxeriments();
