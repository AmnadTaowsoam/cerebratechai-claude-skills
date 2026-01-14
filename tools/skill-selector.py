#!/usr/bin/env python3
"""
Cerebrate Chai - Skill Selection CLI Tool

Interactive tool to help users select relevant skills based on their project type.
"""

import sys
import json
from typing import List, Dict, Set
from pathlib import Path
import textwrap

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Project type definitions
PROJECT_TYPES = {
    "1": {
        "name": "SaaS Application",
        "description": "B2B/B2C Software as a Service",
        "essential": [
            "01-foundations/typescript-standards",
            "01-foundations/python-standards",
            "02-frontend/nextjs-patterns",
            "03-backend-api/nodejs-api",
            "04-database/prisma-guide",
            "10-authentication-authorization/jwt-authentication",
            "18-project-management/agile-scrum",
            "19-seo-optimization/technical-seo",
            "21-documentation/technical-writing",
        ],
        "important": [
            "11-billing-subscription/stripe-integration",
            "11-billing-subscription/usage-metering",
            "12-compliance-governance/pdpa-compliance",
            "14-monitoring-observability/prometheus-metrics",
            "15-devops-infrastructure/docker-patterns",
            "28-marketing-integration/email-marketing",
            "29-customer-support/helpdesk-integration",
        ],
        "optional": [
            "17-domain-specific/multi-tenancy",
            "20-ai-integration/chatbot-integration",
            "34-real-time-features/websocket-patterns",
        ]
    },
    "2": {
        "name": "E-commerce Platform",
        "description": "Online store with payments and inventory",
        "essential": [
            "01-foundations/typescript-standards",
            "02-frontend/nextjs-patterns",
            "03-backend-api/nodejs-api",
            "04-database/prisma-guide",
            "10-authentication-authorization/jwt-authentication",
            "11-billing-subscription/stripe-integration",
            "13-file-storage/s3-integration",
            "30-ecommerce/shopping-cart",
            "30-ecommerce/payment-gateways",
            "30-ecommerce/order-management",
        ],
        "important": [
            "12-compliance-governance/pdpa-compliance",
            "15-devops-infrastructure/kubernetes-deployment",
            "19-seo-optimization/nextjs-seo",
            "28-marketing-integration/email-marketing",
            "30-ecommerce/inventory-management",
            "30-ecommerce/shipping-integration",
        ],
        "optional": [
            "14-monitoring-observability/grafana-dashboards",
            "29-customer-support/live-chat",
        ]
    },
    "3": {
        "name": "Mobile Application",
        "description": "iOS/Android mobile app",
        "essential": [
            "01-foundations/typescript-standards",
            "03-backend-api/fastapi-patterns",
            "04-database/mongodb-patterns",
            "10-authentication-authorization/jwt-authentication",
            "31-mobile-development/react-native-patterns",
            "31-mobile-development/push-notifications",
        ],
        "important": [
            "13-file-storage/s3-integration",
            "14-monitoring-observability/error-tracking",
            "15-devops-infrastructure/ci-cd-github-actions",
            "31-mobile-development/offline-mode",
            "31-mobile-development/deep-linking",
        ],
        "optional": [
            "11-billing-subscription/stripe-integration",
            "20-ai-integration/chatbot-integration",
            "34-real-time-features/presence-detection",
        ]
    },
    "4": {
        "name": "AI/ML Product",
        "description": "Machine learning powered application",
        "essential": [
            "01-foundations/python-standards",
            "03-backend-api/fastapi-patterns",
            "04-database/vector-database",
            "05-ai-ml-core/pytorch-deployment",
            "06-ai-ml-production/llm-integration",
            "06-ai-ml-production/rag-implementation",
        ],
        "important": [
            "05-ai-ml-core/model-training",
            "05-ai-ml-core/data-preprocessing",
            "13-file-storage/s3-integration",
            "14-monitoring-observability/prometheus-metrics",
            "15-devops-infrastructure/kubernetes-deployment",
            "20-ai-integration/ai-agents",
            "39-data-science-ml/ml-serving",
        ],
        "optional": [
            "07-document-processing/ocr-paddleocr",
            "19-seo-optimization/technical-seo",
            "21-documentation/api-documentation",
        ]
    },
    "5": {
        "name": "IoT Platform",
        "description": "Internet of Things device management",
        "essential": [
            "01-foundations/python-standards",
            "03-backend-api/nodejs-api",
            "04-database/timescaledb",
            "08-messaging-queue/mqtt-integration",
            "36-iot-integration/iot-protocols",
            "36-iot-integration/device-management",
        ],
        "important": [
            "14-monitoring-observability/grafana-dashboards",
            "15-devops-infrastructure/docker-patterns",
            "34-real-time-features/real-time-dashboard",
            "36-iot-integration/sensor-data-processing",
            "36-iot-integration/iot-security",
        ],
        "optional": [
            "06-ai-ml-production/llm-integration",
            "36-iot-integration/edge-computing",
            "39-data-science-ml/data-pipeline",
        ]
    },
    "6": {
        "name": "Gaming Platform",
        "description": "Multiplayer gaming or game platform",
        "essential": [
            "01-foundations/typescript-standards",
            "03-backend-api/nodejs-api",
            "04-database/redis-caching",
            "08-messaging-queue/redis-queue",
            "34-real-time-features/websocket-patterns",
            "38-gaming-features/leaderboards",
            "38-gaming-features/real-time-multiplayer",
        ],
        "important": [
            "10-authentication-authorization/jwt-authentication",
            "11-billing-subscription/stripe-integration",
            "14-monitoring-observability/prometheus-metrics",
            "15-devops-infrastructure/kubernetes-deployment",
            "38-gaming-features/achievements",
            "38-gaming-features/matchmaking",
        ],
        "optional": [
            "13-file-storage/cdn-integration",
            "37-video-streaming/live-streaming",
            "38-gaming-features/in-game-purchases",
        ]
    },
    "7": {
        "name": "Video Platform",
        "description": "Video hosting and streaming service",
        "essential": [
            "01-foundations/typescript-standards",
            "03-backend-api/nodejs-api",
            "04-database/prisma-guide",
            "13-file-storage/s3-integration",
            "37-video-streaming/video-upload-processing",
            "37-video-streaming/adaptive-bitrate",
        ],
        "important": [
            "10-authentication-authorization/jwt-authentication",
            "14-monitoring-observability/prometheus-metrics",
            "15-devops-infrastructure/kubernetes-deployment",
            "34-real-time-features/websocket-patterns",
            "37-video-streaming/video-transcoding",
            "37-video-streaming/cdn-delivery",
        ],
        "optional": [
            "11-billing-subscription/subscription-plans",
            "20-ai-integration/ai-search",
            "37-video-streaming/live-streaming",
        ]
    },
    "8": {
        "name": "Web3/Blockchain Application",
        "description": "Decentralized application (dApp)",
        "essential": [
            "01-foundations/typescript-standards",
            "02-frontend/nextjs-patterns",
            "03-backend-api/nodejs-api",
            "35-blockchain-web3/web3-integration",
            "35-blockchain-web3/wallet-connection",
            "35-blockchain-web3/smart-contracts",
        ],
        "important": [
            "10-authentication-authorization/jwt-authentication",
            "13-file-storage/s3-integration",
            "14-monitoring-observability/error-tracking",
            "15-devops-infrastructure/docker-patterns",
            "35-blockchain-web3/blockchain-authentication",
        ],
        "optional": [
            "11-billing-subscription/stripe-integration",
            "34-real-time-features/websocket-patterns",
            "35-blockchain-web3/nft-integration",
            "35-blockchain-web3/cryptocurrency-payment",
        ]
    },
    "9": {
        "name": "Content Management System",
        "description": "Headless CMS or publishing platform",
        "essential": [
            "01-foundations/typescript-standards",
            "02-frontend/nextjs-patterns",
            "03-backend-api/nodejs-api",
            "04-database/prisma-guide",
            "33-content-management/headless-cms",
            "33-content-management/media-library",
        ],
        "important": [
            "10-authentication-authorization/rbac-patterns",
            "13-file-storage/cdn-integration",
            "19-seo-optimization/nextjs-seo",
            "21-documentation/user-guides",
            "33-content-management/content-versioning",
        ],
        "optional": [
            "20-ai-integration/ai-search",
            "22-ux-ui-design/design-systems",
            "34-real-time-features/collaborative-editing",
        ]
    },
    "10": {
        "name": "Custom/Other",
        "description": "Browse all categories",
        "essential": [],
        "important": [],
        "optional": []
    }
}

# All available skills by category
SKILL_CATEGORIES = {
    "01": "Foundations",
    "02": "Frontend Development",
    "03": "Backend API",
    "04": "Database",
    "05": "AI/ML Core",
    "06": "AI/ML Production",
    "07": "Document Processing",
    "08": "Messaging & Queue",
    "09": "Microservices",
    "10": "Authentication & Authorization",
    "11": "Billing & Subscription",
    "12": "Compliance & Governance",
    "13": "File Storage",
    "14": "Monitoring & Observability",
    "15": "DevOps & Infrastructure",
    "16": "Testing",
    "17": "Domain-Specific",
    "18": "Project Management",
    "19": "SEO Optimization",
    "20": "AI Integration",
    "21": "Documentation",
    "22": "UX/UI Design",
    "28": "Marketing Integration",
    "29": "Customer Support",
    "30": "E-commerce",
    "31": "Mobile Development",
    "32": "CRM Integration",
    "33": "Content Management",
    "34": "Real-time Features",
    "35": "Blockchain/Web3",
    "36": "IoT Integration",
    "37": "Video Streaming",
    "38": "Gaming Features",
    "39": "Data Science/ML",
}


def print_header():
    """Print the tool header."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}  🧠 Cerebrate Chai - Claude Skills Selector{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")


def print_section(title: str, color: str = Colors.OKBLUE):
    """Print a section header."""
    print(f"\n{color}{Colors.BOLD}{title}{Colors.ENDC}")
    print(f"{color}{'─'*len(title)}{Colors.ENDC}")


def print_skills(skills: List[str], priority: str):
    """Print a list of skills with their priority."""
    priority_colors = {
        "essential": Colors.OKGREEN,
        "important": Colors.WARNING,
        "optional": Colors.OKCYAN
    }
    
    color = priority_colors.get(priority, Colors.ENDC)
    
    for skill in skills:
        skill_name = skill.split('/')[-1].replace('-', ' ').title()
        category = skill.split('/')[0]
        print(f"  {color}•{Colors.ENDC} {skill_name} {Colors.BOLD}[{category}]{Colors.ENDC}")


def select_project_type() -> Dict:
    """Interactive project type selection."""
    print_section("📋 Select Your Project Type", Colors.OKBLUE)
    
    for key, project in PROJECT_TYPES.items():
        print(f"\n{Colors.BOLD}{key}.{Colors.ENDC} {Colors.OKGREEN}{project['name']}{Colors.ENDC}")
        print(f"   {project['description']}")
    
    while True:
        choice = input(f"\n{Colors.BOLD}Enter your choice (1-10): {Colors.ENDC}").strip()
        if choice in PROJECT_TYPES:
            return PROJECT_TYPES[choice]
        print(f"{Colors.FAIL}Invalid choice. Please enter a number between 1-10.{Colors.ENDC}")


def display_recommended_skills(project: Dict):
    """Display recommended skills for the selected project type."""
    print_header()
    print(f"{Colors.BOLD}{Colors.OKGREEN}Project: {project['name']}{Colors.ENDC}")
    print(f"{project['description']}\n")
    
    if project['essential']:
        print_section("🔥 Essential Skills (Start Here)", Colors.OKGREEN)
        print("These skills are critical for your project:\n")
        print_skills(project['essential'], "essential")
    
    if project['important']:
        print_section("⚡ Important Skills (High Priority)", Colors.WARNING)
        print("These skills will significantly improve your project:\n")
        print_skills(project['important'], "important")
    
    if project['optional']:
        print_section("💡 Optional Skills (Nice to Have)", Colors.OKCYAN)
        print("Consider these based on specific requirements:\n")
        print_skills(project['optional'], "optional")


def browse_all_categories():
    """Browse all skill categories."""
    print_section("📚 All Skill Categories", Colors.OKBLUE)
    
    for code, name in sorted(SKILL_CATEGORIES.items()):
        print(f"  {Colors.BOLD}{code}.{Colors.ENDC} {name}")


def generate_skill_list_file(project: Dict, output_path: str):
    """Generate a text file with the skill list."""
    with open(output_path, 'w') as f:
        f.write(f"# Skills for {project['name']}\n")
        f.write(f"# {project['description']}\n\n")
        
        if project['essential']:
            f.write("## Essential Skills\n\n")
            for skill in project['essential']:
                f.write(f"- {skill}\n")
            f.write("\n")
        
        if project['important']:
            f.write("## Important Skills\n\n")
            for skill in project['important']:
                f.write(f"- {skill}\n")
            f.write("\n")
        
        if project['optional']:
            f.write("## Optional Skills\n\n")
            for skill in project['optional']:
                f.write(f"- {skill}\n")
    
    print(f"\n{Colors.OKGREEN}✓ Skill list saved to: {output_path}{Colors.ENDC}")


def generate_claude_prompt(project: Dict):
    """Generate a Claude prompt with the selected skills."""
    print_section("🤖 Generated Claude Prompt", Colors.OKBLUE)
    
    all_skills = project['essential'] + project['important']
    skill_list = "\n".join([f"- {skill}" for skill in all_skills])
    
    prompt = f"""I'm building a {project['name']} ({project['description']}).

Please help me implement this following these skills:

{skill_list}

Requirements:
1. Follow all best practices from these skills
2. Include proper error handling
3. Add security considerations
4. Ensure production-ready code
5. Include testing strategies

Let's start with [describe what you want to build].
"""
    
    print(f"\n{Colors.OKCYAN}{prompt}{Colors.ENDC}")
    
    # Save to file
    with open("claude_prompt.txt", 'w') as f:
        f.write(prompt)
    
    print(f"\n{Colors.OKGREEN}✓ Prompt saved to: claude_prompt.txt{Colors.ENDC}")


def interactive_skill_filter():
    """Interactive filtering of skills by keywords."""
    print_section("🔍 Search Skills by Keyword", Colors.OKBLUE)
    
    keyword = input(f"\n{Colors.BOLD}Enter keyword (e.g., 'docker', 'auth', 'payment'): {Colors.ENDC}").strip().lower()
    
    matching_skills = []
    for category_code, category_name in SKILL_CATEGORIES.items():
        # This is simplified - in real implementation, would scan actual skill files
        if keyword in category_name.lower():
            matching_skills.append(f"{category_code} - {category_name}")
    
    if matching_skills:
        print(f"\n{Colors.OKGREEN}Found {len(matching_skills)} matching categories:{Colors.ENDC}\n")
        for skill in matching_skills:
            print(f"  • {skill}")
    else:
        print(f"\n{Colors.WARNING}No matches found for '{keyword}'{Colors.ENDC}")


def main_menu():
    """Display the main menu and handle user interaction."""
    while True:
        print_header()
        print_section("🎯 Main Menu", Colors.OKBLUE)
        
        print(f"""
{Colors.BOLD}1.{Colors.ENDC} Select project type (recommended)
{Colors.BOLD}2.{Colors.ENDC} Browse all skill categories
{Colors.BOLD}3.{Colors.ENDC} Search skills by keyword
{Colors.BOLD}4.{Colors.ENDC} Generate Claude prompt
{Colors.BOLD}5.{Colors.ENDC} Exit
        """)
        
        choice = input(f"{Colors.BOLD}Enter your choice (1-5): {Colors.ENDC}").strip()
        
        if choice == "1":
            project = select_project_type()
            display_recommended_skills(project)
            
            # Ask if user wants to save or generate prompt
            print(f"\n{Colors.BOLD}What would you like to do?{Colors.ENDC}")
            print("1. Save skill list to file")
            print("2. Generate Claude prompt")
            print("3. Back to main menu")
            
            action = input(f"\n{Colors.BOLD}Enter choice: {Colors.ENDC}").strip()
            
            if action == "1":
                output_path = f"skills_{project['name'].lower().replace(' ', '_')}.txt"
                generate_skill_list_file(project, output_path)
            elif action == "2":
                generate_claude_prompt(project)
            
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            
        elif choice == "2":
            browse_all_categories()
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            
        elif choice == "3":
            interactive_skill_filter()
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            
        elif choice == "4":
            project = select_project_type()
            generate_claude_prompt(project)
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            
        elif choice == "5":
            print(f"\n{Colors.OKGREEN}Thank you for using Claude Skills Selector! 🚀{Colors.ENDC}\n")
            sys.exit(0)
        else:
            print(f"\n{Colors.FAIL}Invalid choice. Please try again.{Colors.ENDC}")


def main():
    """Main entry point."""
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Interrupted by user. Goodbye! 👋{Colors.ENDC}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {str(e)}{Colors.ENDC}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()