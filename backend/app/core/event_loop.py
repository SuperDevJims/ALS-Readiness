import asyncio


def selector_event_loop_factory() -> asyncio.AbstractEventLoop:
    """Uvicorn --loop factory.

    On Windows, uvicorn's built-in "asyncio" loop option hardcodes
    ProactorEventLoop, which async psycopg cannot run under. Point uvicorn
    at this factory (via --loop) to get a SelectorEventLoop instead, which
    works on every platform. Setting asyncio's event loop policy from
    application code does not work here: uvicorn calls this factory
    directly (asyncio.run(..., loop_factory=...)), bypassing the policy
    entirely.
    """
    return asyncio.SelectorEventLoop()
