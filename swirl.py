# encoding: utf-8

"""
Provides some sugar to make Tornado's async stuff more palatable.
"""

import inspect
import logging
import functools
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, asynchronous as web_async

__version__ = '0.1.0'

def make_asynchronous_decorator(io_loop):
    """
    Creates an asynchronous decorator that uses the given I/O loop.
    
    For information on how to use such a decorator, see
    `swirl.asynchronous`.
    """
    
    
    def asynchronous(coroutine):
        """
        Allows a function to not use explicit callback functions to respond
        to asynchronous events.
        """
        
        @functools.wraps(coroutine)
        def run_async_routine(*args, **kwargs):
            if len(args) > 0 and isinstance(args[0], RequestHandler):
                routine = web_async(coroutine)
                web_handler = args[0]
            else:
                routine = coroutine
                web_handler = None
            
            gen = routine(*args, **kwargs)
            if not inspect.isgenerator(gen):
                # the "coroutine" isn't actually a coroutine; just return
                # its result like tornado.web.asynchronous would do
                return gen
            
            work = None
            def execute_work():
                return work(callback_proxy)
            
            def callback_proxy(*args):
                is_err = lambda val: isinstance(val, Exception)
                try:
                    if len(args) > 0:
                        if is_err(args[-1]):
                            work = gen.throw(args[-1])
                        elif (hasattr(args[0], 'error') and
                              is_err(args[0].error)):
                            work = gen.throw(args[0].error)
                        else:
                            if args[-1] is None:
                                args = args[:-1]
                            if len(args) == 1:
                                work = gen.send(args[0])
                            else:
                                work = gen.send(args)
                    else:
                        work = gen.next()
                    io_loop.add_callback(execute_work)
                except StopIteration:
                    if web_handler:
                        web_handler.finish()
                except Exception, e:
                    if web_handler:
                        if web_handler._headers_written:
                            logging.error('Exception after headers written',
                                exc_info=True)
                        else:
                            web_handler._handle_request_exception(e)
            
            try:
                work = gen.next()
            except StopIteration:
                return None
            
            io_loop.add_callback(execute_work)
        return run_async_routine
    
    return asynchronous

asynchronous = make_asynchronous_decorator(IOLoop.instance())
