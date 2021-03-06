#gems group and objects group
# * is 42
# box is 169
import random
from game.casting.actor import Actor
from game.casting.artifact import Artifact

from game.shared.point import Point
from game.shared.color import Color


class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """


    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._score = 0
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()
        

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)        

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")

        banner.set_text(f"Score : {self._score}")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)

        gems = cast.get_actors("Gems")
        obs = cast.get_actors("Obstacles")
        
        for artifact in gems:
            artifact.move_next(max_x, max_y)
        for artifact in obs:
            artifact.move_next(max_x, max_y)
        
        for n in range(len(gems)):
            if gems[n].get_position().equals(robot.get_position()):
                cast.remove_actor("Gems", gems[n])
                self._score += 1
                message = 'o'

                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                color = Color(r, g, b)

                x = random.randint(1, 60 - 1)
                y = 1
                position = Point(x, y)
                position = position.scale(15)
                velocity = Point(0, 1)

                artifact = Artifact()
                artifact.set_text(chr(42))
                artifact.set_font_size(15)
                artifact.set_color(color)
                artifact.set_position(position)
                artifact.set_message(message)
                artifact.set_velocity(velocity)
                cast.add_actor("Gems", artifact)

        for n in range(len(obs)):
            if obs[n].get_position().equals(robot.get_position()):
                cast.remove_actor("Obstacles", obs[n])
                self._score -= 1 #5  
                message = 'o'

                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                color = Color(r, g, b)

                x = random.randint(1, 60 - 1)
                y = 1
                position = Point(x, y)
                position = position.scale(15)
                velocity = Point(0, 1)

                artifact = Artifact()
                artifact.set_text(chr(42))
                artifact.set_font_size(15)
                artifact.set_color(color)
                artifact.set_position(position)
                artifact.set_message(message)
                artifact.set_velocity(velocity)
                cast.add_actor("Obstacles", artifact)                 


    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()