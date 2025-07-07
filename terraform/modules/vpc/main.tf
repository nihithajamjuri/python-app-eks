data aws_availability_zones "available" {
  state = "available"
}

resource aws_vpc "main" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = var.vpc_name
  }
}

resource aws_subnet "public" {
  count = length(var.public_subnets)
  vpc_id = aws_vpc.main.id
  cidr_block = element(var.public_subnets, count.index)
  availability_zone = element(aws_availability_zones.available.names, count.index)
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.vpc_name}-public-${count.index + 1}"
  }
}

resource aws_subnet "private" {
  count = length(var.private_subnets)
  vpc_id = aws_vpc.main.id
  cidr_block = element(var.private_subnets, count.index)
  availability_zone = element(aws_availability_zones.available.names, count.index)
  tags = {
    Name = "${var.vpc_name}-private-${count.index + 1}"
  }
}

resource aws_internet_gateway "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.vpc_name}-igw"
  }
}

resource aws_route_table "public" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.vpc_name}-public-rt"
  }
}

resource aws_route_table_association "public" {
  count = length(var.public_subnets)
  subnet_id = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}