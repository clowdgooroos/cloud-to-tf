import boto3

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


def security_group_to_terraform(security_group, output_file: Path):
    """ Convert a security group to Terraform code """
    
    # Load the Security Group Terraform file
    security_group_template = Path('terraform/security-group.tf')
    
    rendered_tf = render_template(security_group_template, security_group)
    
    return rendered_tf


def main():
    """ A tool for reversing AWS resources into Terraform code """
    
    # Parse the args
    region = 'us-east-1'
    output_file = Path('/tmp/security_groups.tf')
    
    # Get the security groups
    security_groups = describe_security_groups(region)
    
    # Create the string to hold the entire rendered TF
    rendered_tf = ""
    
    for group in security_groups:
        rendered_tf += security_group_to_terraform(group)
    
    output_file.write_text(rendered_tf)
    

if __name__ == '__main__':
    main()