variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
    default     = "ca-central-1"
}
variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vpc_name" {
  description = "The name of the VPC"
  type        = string
  default     = "my-vpc"
}

variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
  default     =  ["172.16.1.0/24", "172.16.2.0/24"]
}

variable "private_subnets" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
  default     =  ["172.16.3.0/24", "172.16.4.0/24"]
}
variable "ami" {
  description = "The AMI ID to use for the EC2 instances"
  type        = string
  default = "ami-0f9cb75652314425a"
}

variable "instance_type" {
  description = "The type of EC2 instance to launch"
  type        = string
  default     = "t2.micro"
}

variable "userdata" {
  description = "Path to the user data script for the EC2 instances"
  type        = string
  default     = "userdata.sh"
}