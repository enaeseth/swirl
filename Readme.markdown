Swirl
=====

Swirl makes it easier to use the asynchronous features of the
[Tornado][tornado] framework. Tornado methods that require callbacks force you
to write a separate function to capture the result of the method, disrupting
the flow of your program. Swirl exploits Python's
[support for coroutines][pep342] to remove the need for you to write explicit
callback functions.

[tornado]: http://www.tornadoweb.org/
[pep342]: http://www.python.org/dev/peps/pep-0342/

License
-------

Swirl is made available under the terms of the MIT License.

Copyright © 2009 [Eric Naeseth][copyright_holder]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

[copyright_holder]: http://github.com/enaeseth/
