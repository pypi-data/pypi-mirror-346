import json
import os
import sys
import traceback
import click
import requests

from ftf_cli.utils import is_logged_in


@click.command()  # Add this decorator to register the function as a Click command
@click.option(
    "-p",
    "--profile",
    default=lambda: os.getenv("FACETS_PROFILE", "default"),
    help="The profile name to use or defaults to environment variable FACETS_PROFILE if set.",
)
@click.option(
    "-o",
    "--output",
    prompt="Name of the output type to get details for",
    type=str,
    help="The profile name to use or defaults to environment variable FACETS_PROFILE if set.",
)
def get_output_lookup_tree(profile, output):
    """Get the lookup tree of a registered output type from the control plane"""
    try:
        # Check if profile is set
        click.echo(f"Profile selected: {profile}")
        credentials = is_logged_in(profile)
        if not credentials:
            click.echo(f"❌ Not logged in under profile {profile}. Please login first.")
            sys.exit(1)

        # Extract credentials
        control_plane_url = credentials["control_plane_url"]
        username = credentials["username"]
        token = credentials["token"]

        # Make a request to fetch output types
        response = requests.get(
            f"{control_plane_url}/cc-ui/v1/tf-outputs", auth=(username, token)
        )

        if response.status_code == 200:
            registered_output_types = {}
            for registered_output_type in response.json():
                registered_output_types[registered_output_type["name"]] = (
                    registered_output_type
                )

            required_output_type = registered_output_types.get(output)

            if not required_output_type:
                click.echo(f"❌ Output type {output} not found.")
                sys.exit(1)

            if "lookupTree" not in required_output_type:
                lookup_tree = {"out": {"attributes": {}, "interfaces": {}}}
            else:
                lookup_tree = json.loads(required_output_type["lookupTree"])
            click.echo(
                f"Output type lookup tree for {output}:\n{json.dumps(lookup_tree, indent=2, sort_keys=True)}"
            )

        else:
            click.echo(
                f"❌ Failed to fetch output types. Status code: {response.status_code}"
            )
            sys.exit(1)
    except Exception as e:
        click.echo(f"❌ An error occurred: {e}")
        traceback.print_exc()
        sys.exit(1)
