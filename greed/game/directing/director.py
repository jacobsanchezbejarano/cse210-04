import random
from game.shared.color import Color
from game.shared.point import Point
from game.casting.artifact import Artifact

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
        self._score = 600
        self.CELL_SIZE = 15
        self.FONT_SIZE = 15
        self.COLS = 60
        self.ROWS = 40
    
    def set_score(self, earnings):
        self._score += earnings

    def get_score(self):
        return self._score
        
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
            Creates new artifacts when one disappears
            Updates score
            
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")

        banner.set_text("")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)
        
        for artifact in artifacts:
            
            artifact.countdown()
            if robot.get_position().equals(artifact.get_position()):
                
                artifact.calculate_earnings(artifact.get_text())
                earnings = artifact.get_earnings()

                self.set_score(earnings)

                cast.remove_actor('artifacts',artifact) 
                gems = "*"
                rocks = "o"

                list_artifacts = [gems, rocks]


                
                text = list_artifacts[random.randint(0, 1)]

                x = random.randint(1, self.COLS - 1)
                y = random.randint(1, self.ROWS - 20)
                position = Point(x, y)
                position = position.scale(self.CELL_SIZE)

                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                color = Color(r, g, b)
                
                artifact = Artifact()
                artifact.set_text(text)
                artifact.set_font_size(self.FONT_SIZE)
                artifact.set_color(color)
                artifact.set_position(position)
                cast.add_actor("artifacts", artifact)
            
            y_pos = artifact._position.get_y()
            
            if y_pos > 588:
                    cast.remove_actor('artifacts',artifact) 
                    gems = "*"
                    rocks = "o"

                    list_artifacts = [gems, rocks]


                    
                    text = list_artifacts[random.randint(0, 1)]

                    x = random.randint(1, self.COLS - 1)
                    y = random.randint(1, self.ROWS - 20)
                    position = Point(x, y)
                    position = position.scale(self.CELL_SIZE)

                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    color = Color(r, g, b)
                    
                    artifact = Artifact()
                    artifact.set_text(text)
                    artifact.set_font_size(self.FONT_SIZE)
                    artifact.set_color(color)
                    artifact.set_position(position)
                    cast.add_actor("artifacts", artifact)

        

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_score(self._score)
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()