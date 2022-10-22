from game.casting.actor import Actor

# Implemet class Artifact, it will manage the points to earn or lose 

class Artifact(Actor): 

    def __init__(self):
        '''
        Atributes:
            _earnings: This attribute assigns points to earn or lose according to the value assigned to the artifact.
        '''
        self._earnings = ""


    def calculate_earnings(self, artifact):
        """Calculate how many points this artifact will add or subtract to the general score.

        Args:
            artifact (Artifact): An instance of a child class of actor.
        """
        earn = 0
        if artifact == "o\no\no\no":
            earn = 1
        else:
            earn = -1
        
        self._earnings = earn 

    def get_earnings(self):
        """Returns the points assigned to this artifact.

        Args:
            none
        """

        return self._earnings
