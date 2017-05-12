Changelog
---------

1.0.0 (2017-05-17)
++++++++++++++++++

* Fix handling of utf-encoded values when using ``auth`` (#3). Thanks @biern for the catch and patch.
* Drop support for Python 2.6.
* Test against Python 3.6.

0.3.3 (2015-03-17)
++++++++++++++++++

* Implement ``TestApp.head``.

0.3.2 (2014-06-04)
++++++++++++++++++

* Bug fix that caused an ``UnboundLocalError``.

0.3.1 (2014-05-31)
++++++++++++++++++

* Fix string encoding bug on Python 2.

0.3.0 (2014-05-31)
++++++++++++++++++

* Add support for JSON web token authentication.

0.2.1 (2013-11-24)
++++++++++++++++++

* Add authentication to ``TestResponse.click`` and ``TestResponse.clickbutton``.

0.2.0 (2013-10-15)
++++++++++++++++++

* Add support for JSON methods (e.g. ``app.post_json``, etc.)

0.1.0 (2013-10-06)
++++++++++++++++++

* First release.
* HTTP Basic Authentication working.
