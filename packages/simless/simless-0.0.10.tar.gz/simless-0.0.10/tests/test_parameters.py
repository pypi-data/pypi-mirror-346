from simless.sections import *
from simless.parameters import *


def test_speed_rate_parameters():

    section = ConfigSection("SpeedRateSection")
    section.add(
        [       
            BitsPerSecSpeedRateParameter("**.rate", 10),
        ]
    )
    
    print(section.export())
    

test_speed_rate_parameters()