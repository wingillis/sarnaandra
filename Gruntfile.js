module.exports = function(grunt) {
  grunt.initConfig({
    watch: {
      files: ['*.js'],
      tasks: 'browserify'
    },
    browserify: {
      dist: {
        files: {
        'static/app.js': ['app-precompiled.js'],
        'static/exp.js': ['exp-precompiled.js']
        }
      }
    }
  });
  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.registerTask('default', 'watch');
};
