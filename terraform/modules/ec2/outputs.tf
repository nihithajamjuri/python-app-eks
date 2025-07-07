output "ece_instance_ids" {
  description = "List of EC2 instance IDs"
  value       = aws_instance.app_server[*].id
}

output "public_ips" {
  description = "List of public IP addresses of the EC2 instances"
  value       = aws_instance.app_server[*].public_ip
}

output "sg_ids" {
  description = "Security group IDs associated with the EC2 instances"
  value       = aws_security_group.app_sg.id
}