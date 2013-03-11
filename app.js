
/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , user = require('./routes/user')
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

  var wiki_link = request.body.link;
  console.log(wiki_link);
  console.log(__dirname);

  test = spawn('python', [__dirname + '/python/test.py']);
  test.stdout.on('data', function(data) {
    console.log('Stdout: ' + data);
    response.render('index', {
      title: 'Wikiometer',
      score: wiki_link
    });
  });
  test.stderr.on('data', function(data) {
    console.log('Stderr: ' + data);
  });
});

http.createServer(app).listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});
