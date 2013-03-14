
/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , http = require('http')
  , path = require('path')
  , spawn = require('child_process').spawn;

var app = express();

app.configure(function(){
  app.set('port', process.env.PORT || 3000);
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use(express.favicon());
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(express.static(path.join(__dirname, 'public')));
});

app.configure('development', function(){
  app.use(express.errorHandler());
});

app.get('/', routes.index);
app.post('/', function(request, response) {

  var wiki_link = request.body.link
    , python_script = __dirname + '/python/classifier/classifier.py';

  console.log(wiki_link);
  console.log(python_script);

  python = spawn(python_script, [wiki_link]);

  python.stdout.on('data', function(data) {;
    score = data.toString().split("\n");
    console.log('Stdout: ' + data);
    response.render('index', {
      title: 'Wikiometer',
      score: score,
      error: null
    });
  });

  python.stderr.on('data', function(data) {
    console.log('Stderr: ' + data);
    response.render('index', {
      title: 'Wikiometer',
      score: null,
      error: 'error'
    });
  });
});

http.createServer(app).listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});
