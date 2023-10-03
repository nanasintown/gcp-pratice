#!/usr/bin/env python

import os

from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_google.provider import GoogleProvider
from cdktf_cdktf_provider_google.compute_instance import ComputeInstance, ComputeInstanceBootDisk, ComputeInstanceBootDiskInitializeParams, ComputeInstanceNetworkInterfaceAccessConfig, ComputeInstanceNetworkInterfaceAliasIpRange, ComputeInstanceNetworkInterface
from cdktf_cdktf_provider_google.compute_network import ComputeNetwork
from cdktf_cdktf_provider_google.compute_firewall import ComputeFirewall, ComputeFirewallAllow

project_id = "css-nhutcao-2023"

scope = App()
stack = TerraformStack(scope, "tf_python")

with open("credentials.json", "r") as credentials:
    GoogleProvider(
        stack,
        "cdktf",
        region="europe-central2",
        project=project_id,
        credentials=credentials.read())

# The VPC network with automatic subnets (enabled by default)
network = ComputeNetwork(
    stack,
    "cdktf-network",
    name="cdktf-network")

ssh_firewall_rule = ComputeFirewall(
    stack,
    "cdktf-ssh",
    name="cdktf-ssh",
    network=network.id,
    source_ranges=["0.0.0.0/0"],
    target_tags=["ssh"],
    allow=[
        ComputeFirewallAllow(protocol="tcp", ports=["22"])
    ])

http_firewall_rule = ComputeFirewall(
    stack,
    "cdktf-http",
    name="cdktf-http",
    network=network.id,
    source_ranges=["0.0.0.0/0"],
    target_tags=["http"],
    allow=[
        ComputeFirewallAllow(protocol="tcp", ports=["80"]),
    ])

instance = ComputeInstance(
    stack,
    "css-cdktf-vm",
    name="css-cdktf-vm",
    machine_type="f1-micro",
    zone="europe-central2-a",
    boot_disk=ComputeInstanceBootDisk(
        initialize_params=ComputeInstanceBootDiskInitializeParams(
            image="debian-cloud/debian-11"
        )
    ),
    tags=["ssh", "http"],
    network_interface=[ComputeInstanceNetworkInterface(
        network=network.name,
        # An empty access configuration enables public internet access to the server
        access_config=[ComputeInstanceNetworkInterfaceAccessConfig()]
    )],
    allow_stopping_for_update=True)

# Ignore external SSH access changes that happen when clicking the SSH button in the console
instance.add_override("lifecycle.ignore_changes", ["metadata"])

TerraformOutput(stack, "project ID", value=project_id)
TerraformOutput(stack, "vm name", value=instance.name)
TerraformOutput(stack, "vm public IPv4",
                value=instance.network_interface.get(0).access_config.get(0).nat_ip)
TerraformOutput(stack, "vm instance id", value=instance.instance_id)

scope.synth()
