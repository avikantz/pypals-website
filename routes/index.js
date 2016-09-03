var express = require('express');
var router = express.Router();


router.get('/MU3.14159', function(req, res, next) {
    res.render('mu_py')
})


router.get('/', function(req, res, next) {
  res.redirect('MU3.14159');
});

router.get('/repo', function(req, res, next) {
    res.redirect('https://github.com/pypals');
});

router.get('/jiteshjha', function(req, res, next) {
    res.redirect('https://www.github.com/jiteshjha');
});

router.get('/website-repo', function(req, res, next) {
    res.redirect('https://github.com/pypals/pypals-website')
});

router.get('/LUGM', function(req, res, next) {
	res.redirect('http://www.lugm.xyz')
});

router.get('/404', function(req, res, next) {
    res.send('not found');
})

module.exports = router;