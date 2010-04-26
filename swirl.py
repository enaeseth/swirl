# encoding: utf-8

"""
Provides some sugar to make Tornado's async stuff more palatable.
"""

import logging
import inspect
import functools
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, asynchronous as web_async

try:
    from inspect import isgeneratorfunction
except ImportError:
    # Python < 2.6
    def isgeneratorfunction(obj):
        return bool((inspect.isfunction(object) or inspect.ismethod(object)) and
                    obj.func_code.co_flags & CO_GENERATOR)

__version__ = '0.1.1'

class CoroutineRunner(object):
    def __init__(self, generator, web_handler=None, io_loop=None):
        self.gen = generator
        self.web_handler = web_handler
        self.io_loop = io_loop
        
        # start the ball rolling...
        self.callback_proxy()
    
    def execute_work(self):
        return self.work(self.callback_proxy)

    def callback_proxy(self, *args):
        try:
            if len(args) > 0:
                if isinstance(args[-1], Exception):
                    self.work = self.gen.throw(args[-1])
                elif (hasattr(args[0], 'error') and
                      isinstance(args[0].error, Exception)):
                    self.work = self.gen.throw(args[0].error)
                else:
                    if args[-1] is None:
                        args = args[:-1]
                    if len(args) == 1:
                        self.work = self.gen.send(args[0])
                    else:
                        self.work = self.gen.send(args)
            else:
                self.work = self.gen.next()
            
            if self.io_loop is None:
                self.io_loop = IOLoop.instance()
            
            self.io_loop.add_callback(self.execute_work)
        except StopIteration:
            if self.web_handler and not self.web_handler._finished:
                self.web_handler.finish()
        except Exception, e:
            if self.web_handler:
                if self.web_handler._headers_written:
                    logging.error('Exception after headers written',
                        exc_info=True)
                else:
                    self.web_handler._handle_request_exception(e)

def make_asynchronous_decorator(io_loop):
    """
    Creates an asynchronous decorator that uses the given I/O loop.
    
    If the `io_loop` argument is None, the default IOLoop instance will be
    used.
    
    For information on how to use such a decorator, see
    `swirl.asynchronous`.
    """
    
    def asynchronous(coroutine):
        """
        Allows a function to not use explicit callback functions to respond
        to asynchronous events.
        """

        if not isgeneratorfunction(coroutine):
            # the "coroutine" isn't actually a coroutine; just return
            # its result like tornado.web.asynchronous would do
            return coroutine
        
        web_async_coroutine = web_async(coroutine)
        
        @functools.wraps(coroutine)
        def run_async_routine(*args, **kwargs):
            # we check if we're an instancemethod of RequestHandler for better
            # intergration
            if len(args) > 0 and isinstance(args[0], RequestHandler):
                CoroutineRunner(web_async_coroutine(*args, **kwargs),
                    args[0], io_loop)
            else:
                CoroutineRunner(coroutine(*args, **kwargs), io_loop=io_loop)
        
        return run_async_routine    
    return asynchronous

asynchronous = make_asynchronous_decorator(None)
