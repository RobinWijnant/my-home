import asyncio


class Executor:
    def __init__(self, logger):
        self.current_task = None
        self.logger = logger
        pass

    async def run(self, coroutine, success_message):
        self.stop()

        current_task = asyncio.create_task(coroutine)
        current_task.add_done_callback(lambda task: self.logger.info(success_message))
        await current_task

    def stop(self):
        print("try stop")
        if self.current_task is not None and not self.current_task.cancelled():
            print("raise error")
            self.current_task.cancel()
