resource "aws_security_group" "app_sg" {
    name        = "app_sg"
    description = "Security group for application server"
    vpc_id      = var.vpc_id
    
    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"  # Allows all traffic
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "app_server" {
  count = 2
  ami           = var.ami
  instance_type = var.instance_type
  subnet_id     = element(var.subnet_ids, count.index)
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  user_data = base64encode(file(var.userdata))
  tags = {
    Name = "AppServer-${count.index + 1}"
  }
}