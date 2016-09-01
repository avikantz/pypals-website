#!/usr/bin/env node
var express = require('express')
var routes = require('./routes/index');
var path = require('path');
var app = express()
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.use('/public', express.static(__dirname + '/public'));
app.set('view engine', 'ejs');



var routes = require('./routes/index');
app.use('/', routes);
// app.get('/', function(req, res) {
//   res.send('index.html');
// })

app.use(function(req, res, next) {
    res.redirect(404, '/404');
  // var err = new Error('Not Found');
  // err.status = 404;
  // next(err);
});




app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});

// app.listen(3000);
app.listen(3000, /*'localhost',*/ function() {
  console.log("Running");
});


module.exports = app;
