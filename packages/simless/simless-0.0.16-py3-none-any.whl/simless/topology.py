


from simless.sections import NetworkSection


class Topology:
    
    """
    Represents the topology configuration.

    The `Topology` class is responsible for creating all topology-related input files, 
    such as the NED file and routing tables. It also generates the configuration 
    section required to import these inputs into the simulations.

    The primary focus of this class is the topology itself, including nodes, 
    switches, links, and other network components necessary for defining the 
    network structure used in the simulation.
    """

    # This is the section model that will be used to build the section
    # The user can override this to use a custom section model. 
    SECTION_MODEL = NetworkSection 

    def __init__(self):
        self.section: NetworkSection = self.SECTION_MODEL()

    def build_files(self, sim_dir):
        """
        Build the topology files.
        """
        pass

    def build_section(self):
        """
        Build the topology configuration.
        """
        pass

    def build(self, sim_dir):
        self.build_files(sim_dir)
        self.build_section()
        return self.section