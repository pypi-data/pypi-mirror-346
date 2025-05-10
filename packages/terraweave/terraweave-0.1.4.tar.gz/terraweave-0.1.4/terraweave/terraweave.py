import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TerraformWrapper:
    def __init__(self, working_dir):
        """
        Initialize the TerraformWrapper with a working directory.

        Args:
            working_dir (str): The path to the directory containing Terraform configuration files.
        """
        self.working_dir = working_dir

    def _run_command(self, command):
        try:
            result = subprocess.run(
                command,
                cwd=self.working_dir,
                text=True,
                capture_output=True,
                check=True
            )
            logger.info(f"Running command: {' '.join(command)}")
            logger.info(f"Command output: {result.stdout}")
            
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Command error: {e.stderr}")
            raise RuntimeError(f"Command '{' '.join(command)}' failed: {e.stderr}")

    def init(self):
        """
        Initialize the Terraform working directory.

        This runs the `terraform init` command to prepare the directory for Terraform operations.
        It downloads necessary provider plugins and sets up the backend.

        Returns:
            str: The output of the `terraform init` command.

        Raises:
            RuntimeError: If the command fails.
        """
        return self._run_command(["terraform", "init"])

    def plan(self, out_file=None):
        """
        Generate and show an execution plan.

        This runs the `terraform plan` command to create a plan for the changes Terraform will make.

        Args:
            out_file (str, optional): The path to save the plan file. If provided, the plan will be saved to this file.

        Returns:
            str: The output of the `terraform plan` command.

        Raises:
            RuntimeError: If the command fails.
        """
        command = ["terraform", "plan"]
        if out_file:
            command.extend(["-out", out_file])
        return self._run_command(command)

    def apply(self, plan_file=None):
        """
        Apply the changes required to reach the desired state.

        This runs the `terraform apply` command to execute the changes described in the plan.

        Args:
            plan_file (str, optional): The path to a saved plan file. If not provided, the changes will be applied directly.

        Returns:
            str: The output of the `terraform apply` command.

        Raises:
            RuntimeError: If the command fails.
        """
        command = ["terraform", "apply"]
        if plan_file:
            command.append(plan_file)
            command.append("-auto-approve")
        else:
            command.append("-auto-approve")
        return self._run_command(command)

    def destroy(self):
        """
        Destroy the Terraform-managed infrastructure.

        This runs the `terraform destroy` command to remove all resources defined in the configuration.

        Returns:
            str: The output of the `terraform destroy` command.

        Raises:
            RuntimeError: If the command fails.
        """
        return self._run_command(["terraform", "destroy", "-auto-approve"])

    def output(self, name=None):
        """
        Get the value of a Terraform output variable.

        This runs the `terraform output` command to retrieve the value of a specific output variable
        or all output variables if no name is provided.

        Args:
            name (str, optional): The name of the output variable to retrieve. If not provided, all outputs are returned.

        Returns:
            str: The value of the specified output variable or all outputs.

        Raises:
            RuntimeError: If the command fails.
        """
        command = ["terraform", "output", "-json"]
        if name:

            command.append(name)

        return self._run_command(command)
    
    def workspace_list(self):
        """
        List all Terraform workspaces.

        This runs the `terraform workspace list` command to display all available workspaces.

        Returns:
            str: A list of all Terraform workspaces.

        Raises:
            RuntimeError: If the command fails.
        """
        return self._run_command(["terraform", "workspace", "list"])

    def workspace_show(self):
        """
        Show the current Terraform workspace.

        This runs the `terraform workspace show` command to display the name of the currently selected workspace.

        Returns:
            str: The name of the current workspace.

        Raises:
            RuntimeError: If the command fails.
        """
        return self._run_command(["terraform", "workspace", "show"])

    def workspace_new(self, name):
        """
        Create a new Terraform workspace.

        This runs the `terraform workspace new` command to create a new workspace with the specified name.

        Args:
            name (str): The name of the new workspace to create.

        Returns:
            str: The output of the `terraform workspace new` command.

        Raises:
            RuntimeError: If the command fails.
        """
        return self._run_command(["terraform", "workspace", "new", name])

    def workspace_select(self, name):
        """
        Select a Terraform workspace.

        This runs the `terraform workspace select` command to switch to the specified workspace.

        Args:
            name (str): The name of the workspace to select.

        Returns:
            str: The output of the `terraform workspace select` command.

        Raises:
            RuntimeError: If the command fails.
        """
        return self._run_command(["terraform", "workspace", "select", name])

    def workspace_delete(self, name):
        """
        Delete a Terraform workspace.

        This runs the `terraform workspace delete` command to remove the specified workspace.

        Args:
            name (str): The name of the workspace to delete.

        Returns:
            str: The output of the `terraform workspace delete` command.

        Raises:
            RuntimeError: If the command fails.
        """
        return self._run_command(["terraform", "workspace", "delete", name])