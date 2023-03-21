import boto3

from utilities import log_output

@log_output
def describe_security_groups(region: str):
    
    # Create a boto3 client for EC2
    ec2 = boto3.client('ec2', region_name=region)

    # Get the security groups
    response = ec2.describe_security_groups()
    security_groups = response['SecurityGroups']
        
    return security_groups
        

def main():
    describe_security_groups('us-east-1')

if __name__ == '__main__':
    main()