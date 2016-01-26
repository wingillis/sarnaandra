<template lang="jade">
.row
  .columns.medium-3.small-3.button(style='margin: 5px;', data-open="newExpModal")
    div New Experiment
  .columns.medium-6
    h1.text-center Experiments
.row
  .columns.medium-12(v-if="empty")
    p Sorry, but there have been no produced Experiments. Please make one to start the process.
  .columns.medium-3(v-else, v-for="(index, exp) in experiments")
    div Name: {{exp.name}}
    div Description: {{exp.description}}
    div Id: {{exp.id}}
    a(v-link="{ path: '/exp/'+exp.id}") Go
    br
    br

.small.reveal#newExpModal(data-reveal)
  h3 Name:
  input(type='text', v-model="api.name")
  h3 Tags:
  input(type='text', placeholder='comma separated words', v-model="api.tags")
  h3 Description:
  textarea(v-model="api.description")
  input.button(type='submit', value='submit', @click="addExp", data-close)
</template>

<script>
import * as request from 'superagent';
export default {
  created: function(){
    this.getExperiments();
  },
  data: function () {
    var data = {
      empty: true,
      experiments: []
    };
    return data;
  },
  methods: {
    getExperiments: function() {
      var ctx = this;
      request.get('/api/exp')
        .query('all=true').end(function(err, res) {
          if (res.body.res.length > 0) {
            ctx.empty = false;
          }
          ctx.experiments = res.body.res;
        });
    }
  }
}
</script>
