
def orientation_string_to_int(orientation_string):
    if orientation_string == "N":
        return 0
    elif orientation_string == "E":
        return 1
    elif orientation_string == "S":
        return 2
    elif orientation_string == "W":
        return 3


def orientation_int_to_string(orientation_int):
    if orientation_int == 0:
        return "N"
    elif orientation_int == 1:
        return "E"
    elif orientation_int == 2:
        return "S"
    elif orientation_int == 3:
        return "W"


class Robot:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation  # (N, E, S, W)
        self.isLost = False  # LOST or not

    def describe(self):
        return "(" + str(self.position[0]) + ", " + str(self.position[1]) + ", " + orientation_int_to_string(self.orientation) + ")" + " " + ("LOST" if self.isLost else "")


class RobotController:
    def __init__(self, grid_size, initial_robot_state, commands):
        self.grid_size = grid_size
        self.robot = Robot(position=tuple(
            initial_robot_state[:2]), orientation=initial_robot_state[2])
        self.commands = commands

    def execute_command(self, command):
        if self.robot.isLost:
            # Robot is lost, do nothing.
            return

        if command == "L":
            # Turn left command.
            self.robot.orientation = (self.robot.orientation - 1) % 4
        elif command == "R":
            # Turn right command.
            self.robot.orientation = (self.robot.orientation + 1) % 4
        elif command == "F":
            # Move command.
            if self.robot.orientation == 0:  # North
                if self.robot.position[1] + 1 >= self.grid_size[1]:
                    self.robot.isLost = True
                else:
                    self.robot.position = (
                        self.robot.position[0], self.robot.position[1] + 1)
            elif self.robot.orientation == 1:  # East
                if self.robot.position[0] + 1 >= self.grid_size[0]:
                    self.robot.isLost = True
                else:
                    self.robot.position = (
                        self.robot.position[0] + 1, self.robot.position[1])
            elif self.robot.orientation == 2:  # South
                if self.robot.position[1] - 1 < 0:
                    self.robot.isLost = True
                else:
                    self.robot.position = (
                        self.robot.position[0], self.robot.position[1] - 1)
            elif self.robot.orientation == 3:  # West
                if self.robot.position[0] - 1 < 0:
                    self.robot.isLost = True
                else:
                    self.robot.position = (
                        self.robot.position[0] - 1, self.robot.position[1])


class MarsController:
    def __init__(self, grid_size):
        self.robots = []
        self.grid_size = grid_size

    def add_robot(self, initial_robot_state, commands):
        self.robots.append(RobotController(
            self.grid_size, initial_robot_state, commands))

    def execute_commands(self):
        for robot in self.robots:
            for command in robot.commands:
                robot.execute_command(command)

    def print_state(self):
        for robot in self.robots:
            print(robot.robot.describe())


def main():
    # Parse input
    # Grid size: 4 8
    grid_size = tuple(map(int, input("Enter grid size: ").split()))

    controller = MarsController(grid_size)

    while True:
        initial_robot_state_and_commands = input(
            "Enter initial robot state and commands: ")

        if len(initial_robot_state_and_commands) == 0:
            break
        # Get last word after space.
        commands = initial_robot_state_and_commands.split()[-1]
        # Parse robot state and commands: (2, 3, E) LFRFF
        initial_state_string = initial_robot_state_and_commands[:-len(
            commands)]
        initial_state_split = initial_state_string.strip().strip("()").split(",")
        initial_robot_state = (int(initial_state_split[0].strip()), int(
            initial_state_split[1].strip()), orientation_string_to_int(initial_state_split[2].strip()))

        controller.add_robot(initial_robot_state, commands)

    controller.execute_commands()
    controller.print_state()


if __name__ == "__main__":
    main()
