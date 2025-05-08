import argparse
import os
import subprocess
import sys
import uuid
import time
from typing import Optional, List


def build_docker_image(path: str, name: Optional[str] = None, tag: Optional[str] = None, verbose: bool = False, context: Optional[str] = None) -> str:
    """
    Build a Docker image from a Dockerfile in the specified path.

    Args:
        path: Path to the directory containing the Dockerfile or path to a specific Dockerfile
        name: Optional name for the image
        tag: Optional tag for the image
        verbose: Whether to show detailed build logs
        context: Optional path to use as build context (defaults to current directory)

    Returns:
        The ID of the built image
    """
    # Check if path is a file (specific Dockerfile) or directory
    if os.path.isfile(path):
        dockerfile = path
    elif os.path.isdir(path):
        # Use the directory as build context and look for Dockerfile
        dockerfile = os.path.join(path, "Dockerfile")
        if not os.path.isfile(dockerfile):
            raise ValueError(f"No Dockerfile found in {path}")
    else:
        raise ValueError(f"Path {path} does not exist or is not accessible")

    # Generate random name if not provided
    if not name:
        name = f"neodynamics-{uuid.uuid4().hex[:8]}"

    # Use 'latest' as default tag if not provided
    if not tag:
        tag = "latest"

    # Create full image name with tag
    image_name = f"{name}:{tag}"

    # Use provided context or default to current directory
    build_context = os.path.abspath(context) if context else "."

    cmd = ["docker", "build", "-f", dockerfile, "-t", image_name, build_context]

    print(f"Building Docker image with command: {' '.join(cmd)}")

    try:
        if verbose:
            # Use Popen to stream output in real-time when verbose is enabled
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Stream the build logs
            for line in process.stdout:
                print(line, end='')

            process.wait()
            if process.returncode != 0:
                print(f"Error building Docker image. Process exited with code {process.returncode}", file=sys.stderr)
                sys.exit(1)
        else:
            # Use run with minimal output when not verbose
            print("Building Docker image... (use --verbose for detailed logs)")
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error building Docker image: {result.stderr}", file=sys.stderr)
                sys.exit(1)

        print(f"Successfully built image: {image_name}")
        return image_name
    except Exception as e:
        print(f"Error building Docker image: {str(e)}", file=sys.stderr)
        sys.exit(1)


def run_docker_container(image: str, port_mapping: bool = True, interactive_bash: bool = False,
                         additional_args: List[str] = None, attach: bool = False, host_port: int = 50051,
                         volumes: List[str] = None, entrypoint_args: List[str] = None) -> None:
    """
    Run a Docker container with the specified image.

    Args:
        image: The image ID or name to run
        port_mapping: Whether to map port 50051 to the host
        interactive_bash: Whether to run in interactive mode with bash shell
        additional_args: Additional arguments to pass to docker run
        attach: Whether to attach to the container's STDOUT (default is detached mode)
        host_port: The port on the host to map to container's port 50051 (default: 50051)
        volumes: List of volume mappings in format "host_path:container_path"
        entrypoint_args: List of arguments to pass to the container's entrypoint
    """
    cmd = ["docker", "run", "--rm"]

    # Add -it for interactive mode
    if interactive_bash:
        cmd.append("-it")
        # Override entrypoint for interactive mode to ensure we get a shell
        cmd.extend(["--entrypoint", "bash"])
    elif attach:
        # For non-interactive but attached mode, we want to attach to STDOUT
        cmd.extend(["-a", "STDOUT"])
    else:
        # For detached mode (default)
        cmd.append("-d")

    # Add port mapping if enabled
    if port_mapping:
        cmd.extend(["-p", f"{host_port}:50051"])

    # Add volume mappings if provided
    if volumes:
        for volume in volumes:
            cmd.extend(["-v", volume])

    if additional_args:
        cmd.extend(additional_args)

    cmd.append(image)

    # Add entrypoint arguments if provided
    if entrypoint_args:
        cmd.extend(entrypoint_args)

    try:
        if interactive_bash:
            # For interactive mode, we use subprocess.call to directly connect
            # the terminal to the container
            print(f"Starting interactive bash session in container from image: {image}")
            subprocess.call(cmd)
        elif attach:
            # Using subprocess.Popen with stdout/stderr streaming to console
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      universal_newlines=True, bufsize=1)

            print(f"Running container from image: {image}")
            print(f"Command: {' '.join(cmd)}")
            print("Container logs:")

            # Stream the output
            for line in process.stdout:
                print(line, end='')

            process.wait()
            if process.returncode != 0:
                print(f"Container exited with code {process.returncode}", file=sys.stderr)
                sys.exit(process.returncode)
        else:
            # Detached mode
            print(f"Starting container in detached mode from image: {image}")
            print(f"Command: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error starting container: {result.stderr}", file=sys.stderr)
                print(f"Error: {result.stderr}")
                sys.exit(1)
            print(f"Container started successfully")

    except KeyboardInterrupt:
        print("\nStopping container...")
        sys.exit(0)
    except Exception as e:
        print(f"Error running Docker container: {str(e)}", file=sys.stderr)
        sys.exit(1)

def test_connection(server_address: str, num_steps: int = 5, agent_mode: bool = False) -> None:
    """
    Test the connection to a NeoDynamics environment or agent server by calling the appropriate client's main function.

    Args:
        server_address: The address of the server (e.g., "localhost:50051")
        num_steps: Number of steps to run in the test
        agent_mode: Whether to test an agent connection instead of an environment connection
    """
    try:
        if agent_mode:
            # Import the agent client module's main function
            from neodynamics.interface.agent.client import main as client_main
            print(f"Testing agent connection to {server_address}...")
        else:
            # Import the environment client module's main function
            from neodynamics.interface.environment.client import main as client_main
            print(f"Testing environment connection to {server_address}...")

        # Call the client's main function
        client_main(server_address, num_steps)

        print(f"Successfully connected to the {'agent' if agent_mode else 'environment'} server at {server_address}")

    except Exception as e:
        print(f"\nError: {str(e)}")
        print(f"Failed to connect to or interact with the {'agent' if agent_mode else 'environment'} server.")
        sys.exit(1)

def stop_container(image: str) -> None:
    """
    Stop all Docker containers running the specified image.

    Args:
        image: The image name of the containers to stop
    """
    try:
        # Get all container IDs running the specified image
        container_ids = subprocess.run(
            ["docker", "ps", "-q", "--filter", f"ancestor={image}"],
            capture_output=True, text=True, check=True
        ).stdout.strip().split('\n')

        # Filter out empty strings
        container_ids = [cid for cid in container_ids if cid]

        if not container_ids:
            print(f"No running containers found for image {image}")
            return

        print(f"Found {len(container_ids)} container(s) running image {image}")
        for container_id in container_ids:
            try:
                subprocess.run(["docker", "rm", "-f", container_id], check=True)
                print(f"Container {container_id} stopped successfully")
            except subprocess.CalledProcessError as e:
                print(f"Failed to stop container {container_id}: {e}", file=sys.stderr)

    except Exception as e:
        print(f"Error stopping containers: {str(e)}", file=sys.stderr)
        sys.exit(1)


def build_run(
    path: str,
    name: Optional[str] = None,
    tag: Optional[str] = None,
    port_mapping: bool = True,
    verbose: bool = False,
    context: Optional[str] = None,
    host_port: int = 50051,
    volumes: List[str] = None,
    entrypoint_args: List[str] = None
) -> None:
    """
    Build a Docker image, run it as a container, and test the connection.

    Args:
        path: Path to the directory containing the Dockerfile or path to a specific Dockerfile
        name: Optional name for the image
        tag: Optional tag for the image
        port_mapping: Whether to map port 50051 to the host
        verbose: Whether to show detailed logs
        context: Optional path to use as build context (defaults to current directory)
        host_port: The port on the host to map to container's port 50051 (default: 50051)
        volumes: List of volume mappings in format "host_path:container_path"
        entrypoint_args: List of arguments to pass to the container's entrypoint
    """
    try:
        # Step 1: Build the Docker image
        print("=== STEP 1: Building Docker Image ===")
        image = build_docker_image(path, name, tag, verbose, context)

        # Step 2: Run the Docker container
        print("\n=== STEP 2: Running Docker Container ===")
        run_docker_container(
            image,
            port_mapping,
            False,
            additional_args=None,
            attach=False,
            host_port=host_port,
            volumes=volumes,
            entrypoint_args=entrypoint_args
        )

        # Give the container a moment to start up
        print("Waiting for container to initialize...")
        time.sleep(3)  # Wait 3 seconds for the container to start

        return image

    except Exception as e:
        print(f"Error during build-run-test sequence: {str(e)}", file=sys.stderr)
        sys.exit(1)

def build_run_test(
    path: str,
    name: Optional[str] = None,
    tag: Optional[str] = None,
    port_mapping: bool = True,
    server_address: str = "localhost:50051",
    num_steps: int = 5,
    verbose: bool = False,
    context: Optional[str] = None,
    host_port: int = 50051,
    volumes: List[str] = None,
    entrypoint_args: List[str] = None,
    agent_mode: bool = False
) -> None:
    """
    Build a Docker image, run it as a container, and test the connection.

    Args:
        path: Path to the directory containing the Dockerfile or path to a specific Dockerfile
        name: Optional name for the image
        tag: Optional tag for the image
        port_mapping: Whether to map port 50051 to the host
        server_address: The address of the server (e.g., "localhost:50051")
        num_steps: Number of steps to run in the test
        verbose: Whether to show detailed logs
        context: Optional path to use as build context (defaults to current directory)
        host_port: The port on the host to map to container's port 50051 (default: 50051)
        volumes: List of volume mappings in format "host_path:container_path"
        entrypoint_args: List of arguments to pass to the container's entrypoint
        agent_mode: Whether to test an agent connection instead of an environment connection
    """
    try:
        image = build_run(
            path,
            name,
            tag,
            port_mapping,
            verbose,
            context,
            host_port,
            volumes,
            entrypoint_args
        )

        # Step 3: Test the connection
        print("\n=== STEP 3: Testing Connection ===")

        # Test the connection
        test_connection(server_address, num_steps, agent_mode)

        # Stop the container after testing
        print("\n=== Cleaning up: Stopping container ===")
        try:
            container_id = subprocess.run(
                ["docker", "ps", "-q", "--filter", f"ancestor={image}"],
                capture_output=True, text=True, check=True
            ).stdout.strip()

            if container_id:
                subprocess.run(["docker", "stop", container_id], check=True)
                print(f"Container {container_id} stopped successfully")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to stop container: {e}")

    except Exception as e:
        print(f"Error during build-run-test sequence: {str(e)}", file=sys.stderr)
        sys.exit(1)

def remove_neodynamics_images() -> None:
    """
    Remove all Docker images that start with 'neodynamics-'.
    """
    try:
        # List all images that start with 'neodynamics-'
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}", "neodynamics-*"],
            capture_output=True, text=True, check=True
        )

        images = result.stdout.strip().split('\n')
        if not images or (len(images) == 1 and not images[0]):
            print("No neodynamics images found.")
            return

        # Remove each image
        print(f"Found {len(images)} neodynamics images. Removing...")
        for image in images:
            try:
                subprocess.run(["docker", "rmi", "-f", image], check=True)
                print(f"Successfully removed image: {image}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to remove image {image}: {e}", file=sys.stderr)

        print("Finished removing neodynamics images.")
    except Exception as e:
        print(f"Error removing neodynamics images: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="NeoDynamics Docker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build a Docker image")
    build_parser.add_argument("path", help="Path to the directory containing the Dockerfile or path to a specific Dockerfile")
    build_parser.add_argument("-n", "--name", help="Name for the Docker image (random if not provided)")
    build_parser.add_argument("-t", "--tag", help="Tag for the Docker image (defaults to 'latest')")
    build_parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed build logs")
    build_parser.add_argument("-c", "--context", help="Path to use as build context (defaults to current directory)")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a Docker container")
    run_parser.add_argument("image", help="Docker image to run")
    run_parser.add_argument("--no-port-mapping", action="store_true",
                           help="Disable mapping port 50051 to the host")
    run_parser.add_argument("--host-port", type=int, default=50051,
                           help="Port on the host to map to container's port 50051 (default: 50051)")
    run_parser.add_argument("-i", "--interactive", action="store_true",
                           help="Run in interactive mode with bash shell")
    run_parser.add_argument("-a", "--attach", action="store_true",
                           help="Attach to container's STDOUT (default is detached mode)")
    run_parser.add_argument("-v", "--volume", action="append", dest="volumes",
                           help="Mount a volume (format: host_path:container_path). Can be used multiple times.")
    run_parser.add_argument("--entrypoint-args", nargs=argparse.REMAINDER,
                           help="Arguments to pass to the container's entrypoint")
    run_parser.add_argument("--docker-args", nargs=argparse.REMAINDER,
                           help="Additional arguments to pass to docker run")

    # Test command
    test_parser = subparsers.add_parser("test", help="Test connection to a NeoDynamics environment or agent server")
    test_parser.add_argument("--address", default="localhost:50051",
                            help="Server address (default: localhost:50051)")
    test_parser.add_argument("--steps", type=int, default=5,
                            help="Number of steps to run in the test (default: 5)")
    test_parser.add_argument("--agent", action="store_true",
                            help="Test agent connection instead of environment connection")

    # Build-Run command
    br_parser = subparsers.add_parser("build-run",
                                     help="Build a Docker image and run it")
    br_parser.add_argument("path", help="Path to the directory containing the Dockerfile or path to a specific Dockerfile")
    br_parser.add_argument("-n", "--name", help="Name for the Docker image (random if not provided)")
    br_parser.add_argument("-t", "--tag", help="Tag for the Docker image (defaults to 'latest')")
    br_parser.add_argument("--no-port-mapping", action="store_true",
                          help="Disable mapping port 50051 to the host")
    br_parser.add_argument("--host-port", type=int, default=50051,
                          help="Port on the host to map to container's port 50051 (default: 50051)")
    br_parser.add_argument("-v", "--verbose", action="store_true",
                          help="Show detailed logs")
    br_parser.add_argument("-c", "--context", help="Path to use as build context (defaults to current directory)")
    br_parser.add_argument("--volume", action="append", dest="volumes",
                          help="Mount a volume (format: host_path:container_path). Can be used multiple times.")
    br_parser.add_argument("--entrypoint-args", nargs=argparse.REMAINDER,
                          help="Arguments to pass to the container's entrypoint")

    # Build-Run-Test command
    brt_parser = subparsers.add_parser("build-run-test",
                                      help="Build a Docker image, run it, and test the connection")
    brt_parser.add_argument("path", help="Path to the directory containing the Dockerfile or path to a specific Dockerfile")
    brt_parser.add_argument("-n", "--name", help="Name for the Docker image (random if not provided)")
    brt_parser.add_argument("-t", "--tag", help="Tag for the Docker image (defaults to 'latest')")
    brt_parser.add_argument("--no-port-mapping", action="store_true",
                           help="Disable mapping port 50051 to the host")
    brt_parser.add_argument("--address", default="localhost:50051",
                           help="Server address (default: localhost:50051)")
    brt_parser.add_argument("--steps", type=int, default=5,
                           help="Number of steps to run in the test (default: 5)")
    brt_parser.add_argument("-v", "--verbose", action="store_true",
                           help="Show detailed logs")
    brt_parser.add_argument("-c", "--context", help="Path to use as build context (defaults to current directory)")
    brt_parser.add_argument("--host-port", type=int, default=50051,
                           help="Port on the host to map to container's port 50051 (default: 50051)")
    brt_parser.add_argument("--volume", action="append", dest="volumes",
                           help="Mount a volume (format: host_path:container_path). Can be used multiple times.")
    brt_parser.add_argument("--entrypoint-args", nargs=argparse.REMAINDER,
                           help="Arguments to pass to the container's entrypoint")
    brt_parser.add_argument("--agent", action="store_true",
                           help="Test agent connection instead of environment connection")

    # Add remove-images command
    subparsers.add_parser("remove-images",
                         help="Remove all Docker images that start with 'neodynamics-'")

    args = parser.parse_args()

    if args.command == "build":
        build_docker_image(args.path, args.name, args.tag, args.verbose, args.context)
    elif args.command == "run":
        run_docker_container(
            args.image,
            port_mapping=not args.no_port_mapping,
            interactive_bash=args.interactive,
            additional_args=args.docker_args,
            attach=args.attach,
            host_port=args.host_port,
            volumes=args.volumes,
            entrypoint_args=args.entrypoint_args
        )
    elif args.command == "test":
        test_connection(args.address, args.steps, args.agent)
    elif args.command == "stop":
        stop_container(args.image)
    elif args.command == "build-run":
        build_run(
            args.path,
            args.name,
            args.tag,
            not args.no_port_mapping,
            args.verbose,
            args.context,
            args.host_port,
            args.volumes,
            args.entrypoint_args
        )
    elif args.command == "build-run-test":
        build_run_test(
            args.path,
            args.name,
            args.tag,
            not args.no_port_mapping,
            args.address,
            args.steps,
            args.verbose,
            args.context,
            args.host_port,
            args.volumes,
            args.entrypoint_args,
            args.agent
        )
    elif args.command == "remove-images":
        remove_neodynamics_images()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()