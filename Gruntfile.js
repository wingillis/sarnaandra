module.exports = function(grunt) {
  grunt.initConfig({
    watch: {
      files: 'app-precompiled.js',
      tasks: 'browserify'
    },
    browserify: {
      dist: {
        files: {
        'static/app.js': ['app-precompiled.js']
        }
      }
    }
  });
  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.registerTask('default', 'watch');
};
