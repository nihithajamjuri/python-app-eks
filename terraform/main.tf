module "vpc" {
  source = "./modules/vpc"

  vpc_cidr       = var.vpc_cidr
  vpc_name      = var.vpc_name
  public_subnets = var.public_subnets
  private_subnets = var.private_subnets
}
module "ec2" {
  source = "./modules/ec2"

  vpc_id        = module.vpc.vpc_id
  ami           = var.ami
  instance_type = var.instance_type
  subnet_ids    = module.vpc.public_subnet_ids
  userdata      = var.userdata
}
