#!/usr/bin/env node
var express = require('express')
 
var app = express()
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');


app.get('/', function(req, res) {
  res.sendFile('index');
})
 
// app.listen(3237);
app.listen(3237, 'localhost', function() {
  console.log("Running");
});