//Provider Block
provider "aws" {
    profile = "anddhen"
    region = "us-east-1"
}

//Resource Block
resource "aws_instance" "app_server" {
    ami = "ami-007868005aea67c54"
    instance_type = "t2.micro"

    tags = {
        Name = "NewMyTerraformInstance"
    }
}