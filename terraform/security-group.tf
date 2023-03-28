resource "aws_security_group" "{{ GroupName }}" {

  name        = "{{ GroupName }}"
  description = "{{ Description }}"
  vpc_id      = "{{ VpcId }}"

  {% if IpPermissionsIngress %}
  {% for rule in IpPermissionsIngress %}
  ingress {
    description      = "{{ rule.Description }}"
    from_port        = 0
    to_port          = 0
    protocol         = "{{ rule.IpProtocol }}"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  {% endfor %}
  {% endif %} 

  {% if IpPermissionsEgress %}
  {% for rule in IpPermissionsEgress %}
  egress {
    description      = "{{ rule.Description }}"
    from_port        = 0
    to_port          = 0
    protocol         = "{{ rule.IpProtocol }}"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  {% endfor %}
  {% endif %}


  {% if Tags %}
  tags = {
    {% for tag in Tags %}
    {{ tag.name }} = "{{ tag.value }}"
    {% endfor %}
  }
  {% endif %} 
  
}

