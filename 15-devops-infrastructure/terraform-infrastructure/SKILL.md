# Terraform Infrastructure

## Overview

Terraform is an Infrastructure as Code (IaC) tool that allows you to define and provision cloud infrastructure. This skill covers Terraform basics, providers, resources, and best practices.

## Table of Contents

1. [Terraform Basics](#terraform-basics)
2. [Provider Configuration](#provider-configuration)
3. [Resource Definitions](#resource-definitions)
4. [Variables and Outputs](#variables-and-outputs)
5. [Modules](#modules)
6. [State Management](#state-management)
7. [Remote State](#remote-state)
8. [Workspaces](#workspaces)
9. [Common Patterns](#common-patterns)
10. [Best Practices](#best-practices)
11. [Security](#security)

---

## Terraform Basics

### Basic Structure

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main-vpc"
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
}
```

### Terraform Commands

```bash
# Initialize Terraform
terraform init

# Format configuration
terraform fmt

# Validate configuration
terraform validate

# Plan changes
terraform plan

# Apply changes
terraform apply

# Destroy infrastructure
terraform destroy

# Show state
terraform show

# Import existing resources
terraform import aws_vpc.main vpc-12345678
```

---

## Provider Configuration

### AWS Provider

```hcl
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    Environment = "production"
    ManagedBy = "Terraform"
  }

  assume_role {
    role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
  }
}
```

### Azure Provider

```hcl
# providers.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}
```

### GCP Provider

```hcl
# providers.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}
```

### Multiple Providers

```hcl
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    aws.west = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
      configuration_aliases = [west]
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
}
```

---

## Resource Definitions

### VPC Setup

```hcl
# vpc.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.project_name}-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet-${count.index}"
  }
}

resource "aws_subnet" "private" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 3)
  availability_zone       = var.availability_zones[count.index]

  tags = {
    Name = "${var.project_name}-private-subnet-${count.index}"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
```

### ECS/EKS Cluster

```hcl
# ecs.tf
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name        = "${var.project_name}-cluster"
    Environment = var.environment
  }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn           = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = var.container_image
      cpu       = var.task_cpu
      memory    = var.task_memory
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          protocol      = "tcp"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/${var.project_name}"
          "awslogs-region"        = var.region
          "awslogs-stream-prefix"   = "ecs"
          "awslogs-create-group"   = "true"
        }
      }

      environment = [
        {
          name  = "DATABASE_URL"
          value = var.database_url
        },
        {
          name  = "REDIS_URL"
          value = var.redis_url
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "app" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.service_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.app.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = var.container_port
  }

  tags = {
    Name        = "${var.project_name}-service"
    Environment = var.environment
  }
}
```

### RDS Database

```hcl
# rds.tf
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

resource "aws_security_group" "db" {
  name_prefix = "${var.project_name}-db-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-db-sg"
  }
}

resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-db"
  engine     = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class
  allocated_storage = var.db_allocated_storage
  storage_type      = "gp2"
  storage_encrypted = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  backup_retention_period = var.db_backup_retention_period
  backup_window          = "03:00-04:00"

  skip_final_snapshot  = var.db_skip_final_snapshot

  performance_insights_enabled = true

  tags = {
    Name        = "${var.project_name}-db"
    Environment = var.environment
  }
}
```

---

## Variables and Outputs

### Variables

```hcl
# variables.tf
variable "project_name" {
  description = "Project name"
  type        = string
  default     = "myapp"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "container_image" {
  description = "Docker image for the application"
  type        = string
}

variable "container_port" {
  description = "Container port"
  type        = number
  default     = 3000
}

variable "task_cpu" {
  description = "Task CPU units"
  type        = number
  default     = 256
}

variable "task_memory" {
  description = "Task memory in MB"
  type        = number
  default     = 512
}

variable "database_url" {
  description = "Database connection URL"
  type        = string
  sensitive   = true
}

variable "redis_url" {
  description = "Redis connection URL"
  type        = string
  sensitive   = true
}
```

### Outputs

```hcl
# outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "ecs_cluster_id" {
  description = "ID of the ECS cluster"
  value       = aws_ecs_cluster.main.id
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.app.name
}

output "rds_instance_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}
```

---

## Modules

### Module Structure

```
modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── ecs/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── rds/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

### VPC Module

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block = var.cidr_block

  tags = {
    Name = var.name
  }
}

resource "aws_subnet" "public" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name}-public-subnet-${count.index}"
  }
}

resource "aws_subnet" "private" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 3)
  availability_zone       = var.availability_zones[count.index]

  tags = {
    Name = "${var.name}-private-subnet-${count.index}"
  }
}
```

```hcl
# modules/vpc/variables.tf
variable "name" {
  description = "Name of the VPC"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}
```

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}
```

### Using Module

```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"

  name               = "myapp"
  cidr_block        = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "ecs" {
  source = "./modules/ecs"

  vpc_id           = module.vpc.vpc_id
  subnet_ids       = module.vpc.private_subnet_ids
  container_image  = var.container_image
}
```

---

## State Management

### Local State

```hcl
# terraform.tf
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
```

### S3 Backend

```hcl
# terraform.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Azure Storage Backend

```hcl
# terraform.tf
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "terraformstate12345"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

### GCS Backend

```hcl
# terraform.tf
terraform {
  backend "gcs" {
    bucket  = "my-terraform-state"
    prefix  = "prod/terraform"
  }
}
```

---

## Remote State

### Configure Remote State

```hcl
# terraform.tf
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "network/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### Reference Remote State

```hcl
# main.tf
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "network/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_subnet" "app" {
  vpc_id     = data.terraform_remote_state.network.outputs.vpc_id
  cidr_block = "10.0.1.0/24"
}
```

### Terraform Cloud

```hcl
# terraform.tf
terraform {
  cloud {
    organization = "my-org"
    workspaces {
      name = "prod"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

---

## Workspaces

### Workspaces Configuration

```hcl
# terraform.tf
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "workspaces/${terraform.workspace}/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### Use Workspace Variables

```hcl
# variables.tf
variable "environment" {
  default = terraform.workspace
}
```

### Multiple Workspaces

```bash
# Create workspace
terraform workspace new dev

# List workspaces
terraform workspace list

# Select workspace
terraform workspace select dev

# Show current workspace
terraform workspace show
```

---

## Common Patterns

### VPC Setup

```hcl
# vpc.tf
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.main.id
  subnet_id     = aws_subnet.public[0].id

  depends_on = [aws_internet_gateway.main]
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }
}
```

### EKS Cluster

```hcl
# eks.tf
resource "aws_eks_cluster" "main" {
  name     = "${var.project_name}-cluster"
  role_arn = aws_iam_role.cluster.arn
  version = var.kubernetes_version

  vpc_config {
    subnet_ids = concat(aws_subnet.public[*].id, aws_subnet.private[*].id)
  }

  enabled_cluster_log_types = ["api", "audit"]

  tags = {
    Name = "${var.project_name}-cluster"
  }
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.project_name}-node-group"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = aws_subnet.private[*].id

  scaling_config {
    desired_size = var.node_desired_size
    max_size     = var.node_max_size
    min_size     = var.node_min_size
  }

  instance_types = [var.node_instance_type]

  labels = {
    Environment = var.environment
  }
}
```

### RDS Database

```hcl
# rds.tf
resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-db"
  engine     = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class
  allocated_storage = var.db_allocated_storage
  storage_encrypted = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  backup_retention_period = var.db_backup_retention_period
  backup_window          = "03:00-04:00"
  multi_az                = true

  performance_insights_enabled = true

  tags = {
    Name = "${var.project_name}-db"
  }
}
```

---

## Best Practices

### 1. Use Modules

```hcl
# Good: Use modules
module "vpc" {
  source = "./modules/vpc"
  name   = "myapp"
}

# Bad: Duplicate code
resource "aws_vpc" "main" { ... }
resource "aws_subnet" "public" { ... }
```

### 2. Use Variables

```hcl
# Good: Use variables
variable "project_name" {
  type = string
}

# Bad: Hardcode values
resource "aws_vpc" "main" {
  tags = {
    Name = "myapp-vpc"
  }
}
```

### 3. Use Outputs

```hcl
# Good: Use outputs
output "vpc_id" {
  value = aws_vpc.main.id
}

# Bad: Hardcode references
resource "aws_subnet" "app" {
  vpc_id = "vpc-12345678"
}
```

### 4. Use Remote State

```hcl
# Good: Use remote state
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "network/terraform.tfstate"
  }
}

# Bad: Duplicate resources
resource "aws_vpc" "main" { ... }
```

### 5. Use Workspaces

```hcl
# Good: Use workspaces
terraform {
  backend "s3" {
    key = "workspaces/${terraform.workspace}/terraform.tfstate"
  }
}

# Bad: Separate state files
```

---

## Security

### 1. Encrypt State

```hcl
terraform {
  backend "s3" {
    bucket  = "my-terraform-state"
    key     = "terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}
```

### 2. Use State Locking

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
  }
}
```

### 3. Use Sensitive Variables

```hcl
variable "database_password" {
  type      = string
  sensitive = true
}

resource "aws_db_instance" "main" {
  password = var.database_password
}

output "database_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}
```

### 4. Use IAM Roles

```hcl
resource "aws_iam_role" "terraform" {
  name = "terraform-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Condition = {
          StringEquals = {
            "aws:SourceOwner" = var.aws_account_id
          }
        }
      }
    ]
  })
}
```

---

## Summary

This skill covers comprehensive Terraform infrastructure implementation including:

- **Terraform Basics**: Basic structure, Terraform commands
- **Provider Configuration**: AWS, Azure, GCP, multiple providers
- **Resource Definitions**: VPC setup, ECS/EKS cluster, RDS database
- **Variables and Outputs**: Variables definition and outputs
- **Modules**: Module structure and usage
- **State Management**: Local, S3, Azure Storage, GCS backends
- **Remote State**: Configure and reference remote state
- **Workspaces**: Workspace configuration and usage
- **Common Patterns**: VPC setup, EKS cluster, RDS database
- **Best Practices**: Use modules, variables, outputs, remote state, workspaces
- **Security**: Encrypt state, state locking, sensitive variables, IAM roles
