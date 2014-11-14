## Morepath implementation of the TodoMVC-API for Google App Engine

An implementation of the [TodoMVC-API](https://github.com/tastejs/todomvc-api) for Google
App Engine using the [Morepath framework](http://morepath.readthedocs.org/).


## Run Locally
1. Install the [App Engine Python SDK](https://developers.google.com/appengine/downloads).
See the README file for directions. You'll need python 2.7 and [pip 1.4 or later](http://www.pip-installer.org/en/latest/installing.html) installed too.

2. Clone this repo with

   ```
   git clone https://github.com/webmaven/appengine-todos-morepath.git
   ```
3. Install dependencies in the project's lib directory.
   Note: App Engine can only import libraries from inside your project directory.

   ```
   cd appengine-python-morepath-skeleton
   pip install -r requirements.txt -t lib
   ```
4. Run this project locally from the command line:

   ```
   dev_appserver.py .
   ```

See [the development server documentation](https://developers.google.com/appengine/docs/python/tools/devserver)
for options when running dev_appserver.

## Deploy
To deploy the application:

1. Use the [Admin Console](https://appengine.google.com) to create a
   project/app id. (App id and project id are identical)
1. [Deploy the
   application](https://developers.google.com/appengine/docs/python/tools/uploadinganapp) with

   ```
   appcfg.py -A <your-project-id> --oauth2 update .
   ```
1. Congratulations!  Your API is now live at your-app-id.appspot.com

## Next Steps
You should be able to point a TodoMVC front end at this backend.

### Feedback
Star this repo if you found it useful. Use the github issue tracker to give
feedback on this repo.


## Licensing
See [LICENSE](LICENSE)

## Author
[Michael R. Bernstein](http://www.michaelbernstein.com)


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/webmaven/appengine-todos-morepath/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

