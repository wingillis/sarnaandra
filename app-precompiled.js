$(document).foundation();

var Vue = require('vue');
var VueRouter = require('vue-router');
var request = require('superagent');
var Main = require('./templates/index.vue');

Vue.use(VueRouter);

var App = Vue.extend({});

var router = new VueRouter();

router.map({
  '/': {
    component: Main
  },
  '/exp/:expid': {
    component: {
      template: '<p> This is the id {{$route.params.expid}}</p>'
    }
  }
});


var addExp = function() {
  // console.log(this.api.name);
  // console.log(this.api.description);
  var ctx = this;
  request.post('/api/addExp').send(this.api)
  .end(function(err, res){
    ctx.experiments.push(res.body);
    // console.log(ctx.experiments);
    ctx.empty = false;
  });
};


router.start(App, '#app');
