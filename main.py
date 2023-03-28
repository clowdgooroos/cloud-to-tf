import boto3
import argparse

from pathlib import Path

from utilities import log_output, render_template

@log_output
def describe_security_groups(region: str):
    """ Describe all security groups for a given AWS region """
    
    # Create a boto3 client for EC2
    ec2 = boto3.client('ec2', region_name=region)

    # Get the security groups
    response = ec2.describe_security_groups()
    security_groups = response['SecurityGroups']
        
    return security_groups


def security_group_to_terraform(security_group):
    """ Convert a security group to Terraform code """
    
    # Load the Security Group Terraform file
    security_group_template = Path('terraform/security-group.tf')
    
    rendered_tf = render_template(security_group_template, security_group)
    
    return rendered_tf


def main():
    """ A tool for reversing AWS resources into Terraform code """
    
    # Set up the parser
    parser = argparse.ArgumentParser(description='A tool for reversing AWS resources into Terraform code')
    parser.add_argument('-r', '--region', type=str, help='Region to pull data from')
    parser.add_argument('-o', '--output', type=str, help='Output file for TF code')
    args = parser.parse_args()
    
    # Parse the args
    region = args.region
    output_file = Path(args.output)
    
    # Get the security groups
    security_groups = describe_security_groups(region)
    
    # Create the string to hold the entire rendered TF
    rendered_tf = ""
    
    if security_groups:
        for group in security_groups:
            rendered_tf += security_group_to_terraform(group)
    
    output_file.write_text(rendered_tf)
    

if __name__ == '__main__':
    main()