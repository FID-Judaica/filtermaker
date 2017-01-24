filtermaker
===========
``filtermaker`` is a tiny framework for creating string-property testing
suites. I will forego an explanation of how it works because it's one of
those sausage factory things.

So to start, you get your filtering namespace:

.. code:: python

  >>> import filtermaker
  >>> fs = filtermaker.get_filterspace()

Let's say I'm trying to determine if a certain string is part of a
transliteration standard I'm working with (which is why this exists),
first I will define a ``set`` which contains all the characters in that
standard. It could be a sequence type as well, but a set will be faster
for lookups, so it is recommended to use them. Set arithmetic is also
helpful for defining subsets and supersets of things you've already
defined so... use sets.

Once you have your set, you can register a couple of tests with it.

.. code:: python

  >>> all_chars = set('ʾʿăaāâbdĕeēêfghḥiîkḵlmnŏoōôpqrsṣśštṭuûvwyz')
  >>> special_chars = all_chars - set(string.ascii_lowercase)
  >>> fs.haschars(special_chars, 'trans chars')
  >>> fs.onlycharset(all_chars, 'only trans chars')

- create a set with all characters in the transliteration standard.
- create a subset that contains only the non-ascii characters.
- register a test called ``trans chars`` that checks to see if a string
  contains any of the non-ascii characters in the standard.
- register a test that only returns true if all letter-characters in the
  string are part of the transliteration standard. Characters like
  punctuation and so forth will be skipped.

From there, we will want to create an instance of Filter:

.. code:: python

  >>> line = fs.Filter('Šel-lô be-derek ham-melek')
  >>> line.has('trans chars')
  True
  >>> line.has('only trans chars')
  True

One can also combine the tests:

.. code:: python

  >>> line.has('trans chars', 'only trans chars')
  True

Note that this will return false as soon as the first test returns
false.

.. code:: python

  >>> line = fs.Filter('Ḳef u-Śimḥah') # ḳ isn't part of the standard!
  >>> line.has('trans chars')
  True
  >>> line.has('only trans_chars')
  False
  >>> line.has('only trans chars', 'trans chars')
  False

There are a couple of other built-in test generators:

.. code:: python

  >>> # some characters in our transliteration are expressed as digraphs.
  >>> fs.hascluster({'kh', 'sh', 'ts'}, 'digraphs')
  >>> fs.Filter('Ani Okhel Shoḳolad be-Śimḥah').has('digraphs')
  True

as you see, ``.hascluster()`` creates a test that will check in the
string contains certain clusters.

.. code:: python

  >>> fs.hasregex(re.compile('(\W|^)al-[^p]'), 'arabic article')
  >>> # Some of the arabic transliteration is almost impossible to
  >>> # distinguish from Hebrew. This at least checks for the presence
  >>> # of the Arabic article.

This is basically the same as testing with ``re.search()``. It just
makes it easier to integrate regex searches into the rest of the
framework.

So, those are the four built-in test types. What if you want to do a
test that doesn't fit into any of those models? You can create your own
tests with a decorator:

.. code:: python

  >>> @fs.register
  ... def only_western(line):
  ...    return all(ord(c) < 256 for c in line.data)
  ...
  >>> fs.Filter('Šel-lô be-derek ham-melek').has('only_western')
  False

The wrapped function should take one argument as input, which is going
to be the ``Filter`` instance itself, which is a subclass of
``collections.UserString``, so you access the real string with the
``.data`` attribute. The return value should be a bool.

If you want to get very fancy, you can create an entire class of tests
with the ``.registrar`` decorator. Here is the internal implementation
of the ``.haschars`` decorator to show how it works:

.. code:: python

  @registrar
  def haschars(charset):
      return lambda line: any(c for c in line.data if c in charset)

The wrapped function to take one object as input (of any type), and it
should return a closure that takes the string to be checked as input and
returns a bool. The returned function will take the object to be passed
to the wrapped function as the first argument and the name of the test
as the second argument.

.. .. code:: python
