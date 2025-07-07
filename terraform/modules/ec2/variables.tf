variable "instance_type" {
  description = "The type of EC2 instance to launch"
  type        = string
  default     = "t2.micro"
}

variable "ami" {
  description = "The AMI ID to use for the EC2 instances"
  type        = string
}

variable "vpc_id" {
  description = "The VPC ID where the EC2 instances will be launched"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs where the EC2 instances will be launched"
  type        = list(string)
}

variable "userdata" {
  description = "Path to the user data script for the EC2 instances"
  type        = string
  default     = "userdata.sh"
}