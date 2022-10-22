import random
from game.shared.color import Color
from game.shared.point import Point
from game.casting.artifact import Artifact
CAR = "[]----[]\n  OO\n  OO\n[]----[]"

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
            
            for i in robot.get_body_range():
                
                x_a = artifact.get_body_range()[2].get_x()
                y_a = artifact.get_body_range()[3].get_y()
                x_r = i.get_x()
                y_r = i.get_y()+4

                x_robot_range = []
                x_artifact_range = []
                y_robot_range = []
                y_artifact_range = []

                condition = False

                for x in range(0,32):
                    x_artifact_range.append(x_a-16+x) 
                for x in range(0,32):
                    x_robot_range.append(x_r-11+x) 
                for x in range(0,5):
                    y_artifact_range.append(y_a-5+x)
                for x in range(0,5):
                    y_robot_range.append(y_a-x)
                
                for z in x_artifact_range:

                        if z in x_robot_range and (440 in y_artifact_range or 460 in y_artifact_range or 480 in y_artifact_range or 500 in y_artifact_range):
                            condition = True
                            
                            
                if condition:
                    
                    
                
                    artifact.calculate_earnings(artifact.get_text())
                    earnings = artifact.get_earnings()

                    self.set_score(earnings)

                    cast.remove_actor('artifacts',artifact) 

                    gems = CAR
                    rocks = "o\no\no\no"

                    list_artifacts = [gems, rocks]


                    
                    text = list_artifacts[random.randint(0, 1)]

                    reduced_cols = (self.COLS - 1) / 8
                    reduced_rows = (self.ROWS - 30) / 8

                    x = random.randint(1, int(reduced_cols))*8
                    y = random.randint(1, int(reduced_rows))*8
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
                    gems = CAR
                    rocks = "o\no\no\no"

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