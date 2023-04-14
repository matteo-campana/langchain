import json
from langchain.tools.base import BaseTool


class PromptGenerator:
    """
    A class for generating custom prompt strings based on constraints, commands, resources, and performance evaluations.
    """

    def __init__(self):
        """
        Initialize the PromptGenerator object with empty lists of constraints, commands, resources, and performance evaluations.
        """
        self.constraints = []
        self.commands = []
        self.resources = []
        self.performance_evaluation = []
        self.response_format = {
            "thoughts": {
                "text": "thought",
                "reasoning": "reasoning",
                "plan": "- short bulleted\n- list that conveys\n- long-term plan",
                "criticism": "constructive self-criticism",
                "speak": "thoughts summary to say to user"
            },
            "command": {
                "name": "tool name",
                "input": "input to the tool"
            }
        }

    def add_constraint(self, constraint):
        """
        Add a constraint to the constraints list.

        Args:
            constraint (str): The constraint to be added.
        """
        self.constraints.append(constraint)

    def add_tool(self, tool: BaseTool):
        self.commands.append(tool)

    def _generate_command_string(self, tool):
        return f'{tool.name}: {tool.description}'

    def add_resource(self, resource):
        """
        Add a resource to the resources list.

        Args:
            resource (str): The resource to be added.
        """
        self.resources.append(resource)

    def add_performance_evaluation(self, evaluation):
        """
        Add a performance evaluation item to the performance_evaluation list.

        Args:
            evaluation (str): The evaluation item to be added.
        """
        self.performance_evaluation.append(evaluation)

    def _generate_numbered_list(self, items, item_type='list'):
        """
        Generate a numbered list from given items based on the item_type.

        Args:
            items (list): A list of items to be numbered.
            item_type (str, optional): The type of items in the list. Defaults to 'list'.

        Returns:
            str: The formatted numbered list.
        """
        if item_type == 'command':
            return "\n".join(f"{i+1}. {self._generate_command_string(item)}" for i, item in enumerate(items))
        else:
            return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))

    def generate_prompt_string(self):
        """
        Generate a prompt string based on the constraints, commands, resources, and performance evaluations.

        Returns:
            str: The generated prompt string.
        """
        formatted_response_format = json.dumps(self.response_format, indent=4)
        prompt_string = (
            f"Constraints:\n{self._generate_numbered_list(self.constraints)}\n\n"
            f"Commands:\n{self._generate_numbered_list(self.commands, item_type='command')}\n\n"
            f"Resources:\n{self._generate_numbered_list(self.resources)}\n\n"
            f"Performance Evaluation:\n{self._generate_numbered_list(self.performance_evaluation)}\n\n"
            f"You should only respond in JSON format as described below \nResponse Format: \n{formatted_response_format} \nEnsure the response can be parsed by Python json.loads"
        )

        return prompt_string

def get_prompt(tools):
    """
    This function generates a prompt string that includes various constraints, commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint("~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.")
    prompt_generator.add_constraint("If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.")
    prompt_generator.add_constraint("No user assistance")
    prompt_generator.add_constraint('Exclusively use the commands listed in double quotes e.g. "command name"')

    # Add commands to the PromptGenerator object
    for tool in tools:
        prompt_generator.add_tool(tool)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource("Internet access for searches and information gathering.")
    prompt_generator.add_resource("Long Term memory management.")
    prompt_generator.add_resource("GPT-3.5 powered Agents for delegation of simple tasks.")
    prompt_generator.add_resource("File output.")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation("Continuously review and analyze your actions to ensure you are performing to the best of your abilities.")
    prompt_generator.add_performance_evaluation("Constructively self-criticize your big-picture behavior constantly.")
    prompt_generator.add_performance_evaluation("Reflect on past decisions and strategies to refine your approach.")
    prompt_generator.add_performance_evaluation("Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.")

    # Generate the prompt string
    prompt_string = prompt_generator.generate_prompt_string()

    return prompt_string
