output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_ids" {
  value = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.vpc.private_subnet_ids
}
output "ece_instance_ids" {
  description = "List of EC2 instance IDs"
  value       = module.ec2.ec2_instance_ids
}