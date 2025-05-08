import msgpack
import grpc
import requests

from gymnasium import Env, spaces
from gymnasium.core import ActType, ObsType
import gymnasium as gym

# Add the interface directory to the path to import the generated gRPC code
from neodynamics.interface import Empty, ObservationRequest, AgentServiceStub
from neodynamics.interface.utils import native_to_numpy, numpy_to_native, native_to_numpy_space, generate_gym_space_from_spaces_info

class AgentClient(Env):
    """
    A Gym environment compatible agent that connects to a remote environment via gRPC.

    This class implements the Gym interface and forwards all calls to a remote
    agent server.
    """

    def __init__(self, server_address: str, timeout: float = 60.0):
        # Connect to the gRPC server with timeout
        self.channel = grpc.insecure_channel(server_address)
        try:
            # Wait for the channel to be ready
            grpc.channel_ready_future(self.channel).result(timeout=timeout)
        except grpc.FutureTimeoutError:
            self.channel.close()
            raise TimeoutError(f"Could not connect to server at {server_address} within {timeout} seconds")

        self.stub = AgentServiceStub(self.channel)

        # Initialize the remote environment
        init_request = Empty()

        # Call the Init method and get space information
        spaces_response = self.stub.GetSpaces(init_request)

        # Set up observation space
        space_dict = {}
        for name, proto_space in spaces_response.observation_space.items():
            space_dict[name] = native_to_numpy_space(proto_space)
        self.observation_space = spaces.Dict(space_dict)

        # Set up action space
        self.action_space = native_to_numpy_space(spaces_response.action_space)

    def get_action(self, observation: ObsType) -> ActType:
        """Get an action from the agent."""
        # Convert numpy arrays to lists for serialization
        serializable_observation = {}
        for key, value in observation.items():
            serializable_observation[key] = numpy_to_native(value, self.observation_space[key])
        observation_request = ObservationRequest(observation=msgpack.packb(serializable_observation, use_bin_type=True))

        # Call the GetAction method
        action_response = self.stub.GetAction(observation_request)

        # Deserialize the action
        action = msgpack.unpackb(action_response.action, raw=False)
        numpy_action = native_to_numpy(action, self.action_space)

        return numpy_action

    def get_action_serve(self, observation: ObsType) -> ActType:
        """Get an action from the agent."""
        # Convert numpy arrays to lists for serialization
        observation_request = ObservationRequest(observation=msgpack.packb(observation, use_bin_type=True))

        # Call the GetAction method
        action_response = self.stub.GetAction(observation_request)

        # Deserialize the action
        action = msgpack.unpackb(action_response.action, raw=False)
        return action

class DeployedAgentClient(AgentClient):
    def __init__(self, url, api_key=None):
        self.url = url
        self.api_key = api_key
        self.headers = None
        if api_key is not None:
            self.headers = {
                'Content-Type': 'application/json',
                'X-Neo-API-Key': self.api_key
            }

        self._get_spaces()

    def get_action(self, obs):
        # Convert numpy arrays to lists for serialization
        serializable_observation = {}
        for key, value in obs.items():
            serializable_observation[key] = numpy_to_native(value, self.observation_space[key])

        url = self.url.rstrip('/') + '/get_action'
        response = requests.post(url, json={"observation": serializable_observation}, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error in DeployedAgentClient.get_action: {response.status_code} {response.text}")

        action = response.json().get("action")
        numpy_action = native_to_numpy(action, self.action_space)

        return numpy_action

    def _get_spaces(self):
        url = self.url.rstrip('/') + '/get_spaces'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Error in DeployedAgentClient._get_spaces: {response.status_code} {response.text}")

        spaces_config = response.json().get("spaces_config")
        observation_space = {}
        for key in spaces_config['observationSpaceInfo'].keys():
            observation_space[key] = generate_gym_space_from_spaces_info(spaces_config['observationSpaceInfo'][key])
        self.observation_space = gym.spaces.Dict(observation_space)
        self.action_space = generate_gym_space_from_spaces_info(spaces_config['actionSpaceInfo'])


def main(server_address: str = "localhost:50051", num_steps: int = 5):
    """
    Run a simple test of the EnvironmentClient.

    Args:
        server_address: The address of the server (e.g., "localhost:50051")
        num_steps: Number of steps to run in the test
    """
    try:
        # Create a remote agent
        agent = AgentClient(server_address)

        # Run a few steps
        for i in range(num_steps):
            obs = agent.observation_space.sample()
            action = agent.get_action(obs)
            assert agent.action_space.contains(action), f"Action {action} not in action space {agent.action_space}"

            print(f"Observation: {obs}")
            print(f"Action: {action}")

        # Print success message if no errors occurred
        print("\nSuccess! The agent client is working correctly.")

    except Exception as e:
        print(f"\nError: {e}")
        print("Failed to connect to or interact with the agent server.")
        raise


# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test the AgentClient")
    parser.add_argument("--address", default="localhost:50051",
                        help="AServer address (default: localhost:50051)")
    parser.add_argument("--steps", type=int, default=5,
                        help="Number of steps to run in the test (default: 5)")

    args = parser.parse_args()

    try:
        main(args.address, args.steps)
    except Exception:
        import sys
        sys.exit(1)