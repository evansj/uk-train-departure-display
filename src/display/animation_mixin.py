
class AnimationMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._running     = True
        self._should_stop = False

    @property
    def running(self):
        """Returns True while the animation is running"""
        return self._running

    @property
    def stopped(self):
        """The opposite of running"""
        return not self._running

    def run(self):
        """The main coordinator method calls this when animations should start again"""
        self._should_stop = False
        self._running = True

    def stop(self):
        """The main coordinator method calls this when it wants to stop all animations"""
        self._should_stop = True

    @property
    def should_stop(self):
        """The class calls this to see if it can start another animation"""
        return self._should_stop

    @property
    def can_start(self):
        """The opposite of should_stop"""
        return not self._should_stop

    def start(self):
        """
            The class calls this when it is starting an animation.
            It returns True if animation is permitted.
        """
        self._running = self.can_start
        return self._running

    def end(self):
        """
            The class calls this when it has ended an animation.
        """
        self._running = False
