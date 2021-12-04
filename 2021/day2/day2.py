from pathlib import Path
wrong_answers = [1947824]
input_path = Path(__file__).parent.absolute() / 'sub_commands.txt'
with input_path.open() as f:
    sub_commands_data = [i.split() for i in f.read().splitlines()]
command_with_depth_calc = []

up_sum = sum(-int(i[1]) for i in sub_commands_data if i[0] == "up")
down_sum = sum(int(i[1]) for i in sub_commands_data if i[0] == "down")
horizontal_position = sum(int(i[1]) for i in sub_commands_data if i[0] == "forward")
test_data = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
test_data = [x.split() for x in test_data.splitlines()]
def sub_1():
    depth = 0
    horizontal_position = 0
    for command, value in sub_commands_data:
        value = int(value)
        if command == "forward":
            print(f"Moving horizontal: {value} steps")
            horizontal_position += int(value)
        if command == "up":
            print(f"Moving up: {value} steps")
            depth -= int(value)
        if command == "down":
            print(f"Moving down: {value} steps")
            depth += int(value)

    print("Depth: ", depth)
    print("Horizontal position: ", horizontal_position)
    print("Total: ", depth * horizontal_position)

class Submarine:

    def __init__(self, commands, aim_sub=True) -> None:
        self.x = 0
        self.y = 0
        self.aim = 0
        self.commands = commands
        self.aim_sub = aim_sub
    
    def run_commands(self):
        for command, value in self.commands:
            self.command(command, value)
            print(self)
        return self.total()
    
    def command(self, command, value):
        value = int(value)
        print(f"--> {command} {value}")
        match command,value:
            case "forward",x:
                self.forward(x)
            case "up",x:
                # print(f"changing aim up {x} steps")
                self.depth(-x)
            case "down",x:
                print(f"changing aim down {x} steps")
                self.depth(x)

    def forward(self, value):
        print(f"moving forward {value} steps", end=" ")
        self.x += value
        if self.aim_sub:
            depth = value * self.aim
            print(f"changing depth by {value}x{self.aim}")
            self.depth(depth)
    
    def depth(self, value, forward=False):
        if self.aim_sub:
            self.change_aim(value)
            return
        elif self.aim_sub and forward:
            self.y += value
            print(f"changing depth by {value}")
            return
        elif not any(self.aim_sub,forward):
            self.y += value
            print(f"changing depth by {value}")
            return
        
    def change_aim(self, value):
        self.aim += value
    
    def total(self):
        return self.y*self.x
    
    def __str__(self) -> str:
        return f"(x:{self.x},y:{self.y},aim:{self.aim}, total:{self.total()})"

def sub_2():
    # horizontal_position = 0
    aim = 0
    submarine = Submarine(test_data)
    total = submarine.run_commands()
    # print(total)
    # depth = (up_sum + down_sum)
    # print("down_sum: ", down_sum)
    # print("up_sum: ", up_sum)
    # print("Depth: ", depth)
    # print("Horizontal position: ", horizontal_position)
    # print("Total: ", depth*horizontal_position)

def forward(value, horizontal_position, aim):
    print(f"Moving horizontal: {value} steps")
    horizontal_position += int(value)
    # return {horizontal_position, aim, depth+depth_move}

sub_2()