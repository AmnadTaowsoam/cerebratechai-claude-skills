#!/bin/bash
# Development environment setup script

set -e

echo "🚀 Setting up development environment..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo -e "${BLUE}Building Docker containers...${NC}"
docker-compose build

echo -e "${BLUE}Installing Python dependencies...${NC}"
docker-compose run --rm dev pip install -r requirements-dev.txt

echo -e "${BLUE}Installing Node.js dependencies...${NC}"
docker-compose run --rm dev npm install

echo -e "${BLUE}Setting up Git hooks...${NC}"
docker-compose run --rm dev python scripts/setup-git-hooks.py

echo -e "${GREEN}✓ Development environment ready!${NC}"
echo ""
echo "Available commands:"
echo "  docker-compose up dev        # Start development shell"
echo "  docker-compose run validator # Validate all skills"
echo "  docker-compose up docs       # Start documentation server"
echo "  docker-compose up search     # Start search service"