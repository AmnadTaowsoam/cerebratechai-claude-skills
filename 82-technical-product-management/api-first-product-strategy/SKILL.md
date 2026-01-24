---
name: API-First Product Strategy
description: Designing products with APIs as first-class citizens for better integration and developer experience
---

# API-First Product Strategy

## Current Level: Expert (Enterprise Scale)

## Domain: Technical Product Management
## Skill ID: 137

---

## Executive Summary

API-First Product Strategy treats APIs as first-class citizens in product design, enabling better integration, developer experience, and ecosystem growth. This approach is essential for modern SaaS products, platform businesses, and any product requiring third-party integration.

### Strategic Necessity

- **Developer Experience**: Improve DX for API consumers
- **Integration**: Enable seamless third-party integration
- **Ecosystem Growth**: Foster partner and developer ecosystem
- **Time-to-Market**: Accelerate development through parallel API and UI work
- **Flexibility**: Support multiple client types (web, mobile, IoT)

---

## Technical Deep Dive

### API-First Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    API-First Product Architecture                      │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   API Layer  │    │   Business  │    │   Data      │                  │
│  │   (Primary)  │───▶│   Logic     │───▶│   Access     │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Client Applications                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │   Web     │  │  Mobile    │  │  IoT       │  │  Third     │            │   │
│  │  │   App     │  │  App       │  │  Devices   │  │  Party     │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Developer Experience                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │   Docs    │  │   SDKs     │  │   Tools    │  │  Portal    │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### API Design Principles

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class APIType(Enum):
    """API types"""
    REST = "rest"
    GRAPHQL = "graphql"
    GRPC = "grpc"
    WEBSOCKET = "websocket"

class APIVersioningStrategy(Enum):
    """API versioning strategies"""
    URL_PATH = "url_path"  # /v1/users
    HEADER = "header"  # Accept: application/vnd.api.v1+json
    QUERY_PARAM = "query_param"  # ?version=1
    CONTENT_NEGOTIATION = "content_negotiation"

@dataclass
class APIEndpoint:
    """API endpoint definition"""
    path: str
    method: str  # GET, POST, PUT, DELETE, PATCH
    description: str
    request_schema: Dict[str, Any]
    response_schema: Dict[str, Any]
    authentication: Optional[str]
    rate_limiting: Optional[Dict[str, Any]]
    deprecated: bool = False
    deprecation_date: Optional[str] = None

class APIFirstDesigner:
    """API-first product designer"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_type = APIType(config.get('api_type', 'rest'))
        self.versioning_strategy = APIVersioningStrategy(
            config.get('versioning_strategy', 'url_path')
        )
        self.endpoints = []
        self.design_principles = self._initialize_principles()
        
    def _initialize_principles(self) -> Dict[str, Any]:
        """Initialize API design principles"""
        return {
            'consistency': {
                'naming_convention': 'snake_case',
                'resource_naming': 'plural',
                'field_naming': 'snake_case'
            },
            'error_handling': {
                'standard_errors': True,
                'error_codes': True,
                'error_messages': True
            },
            'pagination': {
                'strategy': 'cursor_based',
                'default_page_size': 20,
                'max_page_size': 100
            },
            'filtering': {
                'strategy': 'query_params',
                'supported_operators': ['eq', 'ne', 'gt', 'gte', 'like', 'in']
            },
            'sorting': {
                'strategy': 'query_param',
                'default_sort': 'created_at'
            },
            'versioning': {
                'strategy': self.versioning_strategy.value,
                'supported_versions': ['v1', 'v2']
            }
        }
    
    def design_api(
        self,
        product_requirements: Dict[str, Any]
    ) -> List[APIEndpoint]:
        """Design API based on product requirements"""
        logger.info("Designing API from product requirements...")
        
        # Extract resources from requirements
        resources = self._extract_resources(product_requirements)
        
        # Design endpoints for each resource
        for resource in resources:
            endpoints = self._design_resource_endpoints(resource)
            self.endpoints.extend(endpoints)
        
        # Apply design principles
        self._apply_design_principles()
        
        # Validate API design
        self._validate_api_design()
        
        logger.info(f"API design complete: {len(self.endpoints)} endpoints")
        
        return self.endpoints
    
    def _extract_resources(
        self,
        requirements: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract resources from product requirements"""
        resources = []
        
        # Extract entities from requirements
        entities = requirements.get('entities', [])
        
        for entity in entities:
            resource = {
                'name': entity['name'],
                'plural': entity.get('plural', f"{entity['name']}s"),
                'properties': entity.get('properties', []),
                'relationships': entity.get('relationships', []),
                'operations': entity.get('operations', ['create', 'read', 'update', 'delete'])
            }
            resources.append(resource)
        
        return resources
    
    def _design_resource_endpoints(
        self,
        resource: Dict[str, Any]
    ) -> List[APIEndpoint]:
        """Design endpoints for a resource"""
        endpoints = []
        resource_name = resource['name']
        resource_plural = resource['plural']
        
        # Design CRUD endpoints
        for operation in resource['operations']:
            endpoint = self._design_crud_endpoint(
                resource_name,
                resource_plural,
                operation
            )
            endpoints.append(endpoint)
        
        # Design relationship endpoints
        for relationship in resource.get('relationships', []):
            endpoint = self._design_relationship_endpoint(
                resource_name,
                relationship
            )
            endpoints.append(endpoint)
        
        # Design action endpoints
        for action in resource.get('actions', []):
            endpoint = self._design_action_endpoint(
                resource_name,
                action
            )
            endpoints.append(endpoint)
        
        return endpoints
    
    def _design_crud_endpoint(
        self,
        resource_name: str,
        resource_plural: str,
        operation: str
    ) -> APIEndpoint:
        """Design CRUD endpoint"""
        endpoints = {
            'create': {
                'path': f"/{resource_plural}",
                'method': 'POST',
                'description': f"Create new {resource_name}"
            },
            'read': {
                'path': f"/{resource_plural}/{{id}}",
                'method': 'GET',
                'description': f"Get {resource_name} by ID"
            },
            'update': {
                'path': f"/{resource_plural}/{{id}}",
                'method': 'PUT',
                'description': f"Update {resource_name}"
            },
            'delete': {
                'path': f"/{resource_plural}/{{id}}",
                'method': 'DELETE',
                'description': f"Delete {resource_name}"
            },
            'list': {
                'path': f"/{resource_plural}",
                'method': 'GET',
                'description': f"List all {resource_plural}"
            }
        }
        
        endpoint_config = endpoints.get(operation, {})
        
        return APIEndpoint(
            path=endpoint_config['path'],
            method=endpoint_config['method'],
            description=endpoint_config['description'],
            request_schema=self._get_request_schema(resource_name, operation),
            response_schema=self._get_response_schema(resource_name, operation),
            authentication='bearer_token',
            rate_limiting={'requests_per_minute': 100}
        )
    
    def _design_relationship_endpoint(
        self,
        resource_name: str,
        relationship: Dict[str, Any]
    ) -> APIEndpoint:
        """Design relationship endpoint"""
        relationship_name = relationship['name']
        target_resource = relationship['target_resource']
        cardinality = relationship.get('cardinality', 'many')
        
        return APIEndpoint(
            path=f"/{resource_name}/{{id}}/{relationship_name}",
            method='GET',
            description=f"Get {cardinality} {target_resource} for {resource_name}",
            request_schema={},
            response_schema={'data': {'type': 'array', 'items': {'$ref': target_resource}}},
            authentication='bearer_token',
            rate_limiting={'requests_per_minute': 60}
        )
    
    def _design_action_endpoint(
        self,
        resource_name: str,
        action: Dict[str, Any]
    ) -> APIEndpoint:
        """Design action endpoint"""
        action_name = action['name']
        action_path = action.get('path', f"/{resource_name}/{{id}}/{action_name}")
        
        return APIEndpoint(
            path=action_path,
            method=action.get('method', 'POST'),
            description=action.get('description', f"Perform {action_name} action"),
            request_schema=action.get('request_schema', {}),
            response_schema=action.get('response_schema', {}),
            authentication=action.get('authentication', 'bearer_token'),
            rate_limiting=action.get('rate_limiting', {'requests_per_minute': 30})
        )
    
    def _get_request_schema(
        self,
        resource_name: str,
        operation: str
    ) -> Dict[str, Any]:
        """Get request schema for endpoint"""
        if operation == 'create':
            return {
                'type': 'object',
                'required': ['data'],
                'properties': {
                    'data': {
                        'type': 'object',
                        'required': self._get_required_fields(resource_name, 'create'),
                        'properties': self._get_field_properties(resource_name)
                    }
                }
            }
        elif operation == 'update':
            return {
                'type': 'object',
                'required': ['data'],
                'properties': {
                    'data': {
                        'type': 'object',
                        'required': self._get_required_fields(resource_name, 'update'),
                        'properties': self._get_field_properties(resource_name)
                    }
                }
            }
        elif operation == 'list':
            return {
                'type': 'object',
                'properties': {
                    'page': {'type': 'integer', 'minimum': 1},
                    'per_page': {'type': 'integer', 'minimum': 1, 'maximum': 100},
                    'filter': {'type': 'object'},
                    'sort': {'type': 'string'}
                }
            }
        else:
            return {}
    
    def _get_response_schema(
        self,
        resource_name: str,
        operation: str
    ) -> Dict[str, Any]:
        """Get response schema for endpoint"""
        if operation in ['create', 'read', 'update']:
            return {
                'type': 'object',
                'properties': {
                    'data': {'$ref': resource_name},
                    'meta': {
                        'type': 'object',
                        'properties': {
                            'page': {'type': 'integer'},
                            'per_page': {'type': 'integer'},
                            'total': {'type': 'integer'}
                        }
                    }
                }
            }
        elif operation == 'list':
            return {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {'$ref': resource_name}
                    },
                    'meta': {
                        'type': 'object',
                        'properties': {
                            'page': {'type': 'integer'},
                            'per_page': {'type': 'integer'},
                            'total': {'type': 'integer'}
                        }
                    }
                }
            }
        elif operation == 'delete':
            return {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        else:
            return {}
    
    def _get_required_fields(
        self,
        resource_name: str,
        operation: str
    ) -> List[str]:
        """Get required fields for operation"""
        # Implementation would return required fields
        # based on resource configuration
        return []
    
    def _get_field_properties(self, resource_name: str) -> Dict[str, Any]:
        """Get field properties for resource"""
        # Implementation would return field definitions
        # with types, constraints, etc.
        return {}
    
    def _apply_design_principles(self):
        """Apply design principles to all endpoints"""
        # Apply naming conventions
        self._apply_naming_conventions()
        
        # Apply error handling
        self._apply_error_handling()
        
        # Apply pagination
        self._apply_pagination()
        
        # Apply filtering
        self._apply_filtering()
        
        # Apply sorting
        self._apply_sorting()
        
        # Apply versioning
        self._apply_versioning()
    
    def _apply_naming_conventions(self):
        """Apply naming conventions to endpoints"""
        naming = self.design_principles['consistency']
        
        for endpoint in self.endpoints:
            # Apply naming convention to path
            endpoint.path = endpoint.path.lower()
            
            # Apply naming convention to fields
            # This would be done in schema definitions
            pass
    
    def _apply_error_handling(self):
        """Apply standard error handling"""
        error_handling = self.design_principles['error_handling']
        
        # Define standard error codes
        self.standard_errors = {
            'validation_error': {'code': 400, 'message': 'Validation error'},
            'unauthorized': {'code': 401, 'message': 'Unauthorized'},
            'forbidden': {'code': 403, 'message': 'Forbidden'},
            'not_found': {'code': 404, 'message': 'Resource not found'},
            'conflict': {'code': 409, 'message': 'Resource conflict'},
            'server_error': {'code': 500, 'message': 'Internal server error'}
        }
    
    def _apply_pagination(self):
        """Apply pagination to list endpoints"""
        pagination = self.design_principles['pagination']
        
        for endpoint in self.endpoints:
            if endpoint.method == 'GET' and not endpoint.path.endswith('/{id}'):
                # Add pagination parameters
                pass
    
    def _apply_filtering(self):
        """Apply filtering to list endpoints"""
        filtering = self.design_principles['filtering']
        
        for endpoint in self.endpoints:
            if endpoint.method == 'GET' and not endpoint.path.endswith('/{id}'):
                # Add filtering parameters
                pass
    
    def _apply_sorting(self):
        """Apply sorting to list endpoints"""
        sorting = self.design_principles['sorting']
        
        for endpoint in self.endpoints:
            if endpoint.method == 'GET' and not endpoint.path.endswith('/{id}'):
                # Add sorting parameters
                pass
    
    def _apply_versioning(self):
        """Apply versioning to all endpoints"""
        versioning = self.design_principles['versioning']
        
        if versioning['strategy'] == 'url_path':
            for endpoint in self.endpoints:
                # Add version prefix to path
                endpoint.path = f"/{versioning['supported_versions'][0]}{endpoint.path}"
    
    def _validate_api_design(self):
        """Validate API design against best practices"""
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check for duplicate endpoints
        duplicates = self._check_duplicate_endpoints()
        validation_results['errors'].extend(duplicates)
        
        # Check for inconsistent naming
        naming_issues = self._check_naming_consistency()
        validation_results['warnings'].extend(naming_issues)
        
        # Check for missing documentation
        doc_issues = self._check_documentation_completeness()
        validation_results['warnings'].extend(doc_issues)
        
        # Check for security issues
        security_issues = self._check_security()
        validation_results['errors'].extend(security_issues)
        
        if validation_results['errors']:
            validation_results['valid'] = False
        
        return validation_results
    
    def _check_duplicate_endpoints(self) -> List[str]:
        """Check for duplicate endpoints"""
        duplicates = []
        endpoint_signatures = {}
        
        for endpoint in self.endpoints:
            signature = f"{endpoint.method}:{endpoint.path}"
            
            if signature in endpoint_signatures:
                duplicates.append(
                    f"Duplicate endpoint: {endpoint.method} {endpoint.path}"
                )
            else:
                endpoint_signatures[signature] = endpoint
        
        return duplicates
    
    def _check_naming_consistency(self) -> List[str]:
        """Check for naming consistency"""
        issues = []
        naming = self.design_principles['consistency']
        
        # Check resource naming
        resource_names = set()
        for endpoint in self.endpoints:
            resource = endpoint.path.split('/')[1]
            
            if resource in resource_names:
                issues.append(f"Inconsistent resource naming: {resource}")
            else:
                resource_names.add(resource)
        
        return issues
    
    def _check_documentation_completeness(self) -> List[str]:
        """Check for documentation completeness"""
        issues = []
        
        for endpoint in self.endpoints:
            if not endpoint.description:
                issues.append(
                    f"Missing description: {endpoint.method} {endpoint.path}"
                )
        
        return issues
    
    def _check_security(self) -> List[str]:
        """Check for security issues"""
        issues = []
        
        for endpoint in self.endpoints:
            # Check for authentication
            if not endpoint.authentication:
                issues.append(
                    f"Missing authentication: {endpoint.method} {endpoint.path}"
                )
            
            # Check for rate limiting
            if not endpoint.rate_limiting:
                issues.append(
                    f"Missing rate limiting: {endpoint.method} {endpoint.path}"
                )
        
        return issues
```

### API Documentation

```python
class APIDocumentationGenerator:
    """API documentation generator"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.endpoints = []
        
    def generate_openapi_spec(
        self,
        endpoints: List[APIEndpoint]
    ) -> Dict[str, Any]:
        """Generate OpenAPI specification"""
        logger.info("Generating OpenAPI specification...")
        
        spec = {
            'openapi': '3.0.0',
            'info': self._get_api_info(),
            'servers': self._get_servers(),
            'security': self._get_security_schemes(),
            'paths': self._get_paths(endpoints),
            'components': self._get_components(),
            'tags': self._get_tags()
        }
        
        logger.info("OpenAPI specification generated")
        
        return spec
    
    def _get_api_info(self) -> Dict[str, Any]:
        """Get API information"""
        return {
            'title': self.config.get('title', 'My API'),
            'description': self.config.get('description', 'API Description'),
            'version': self.config.get('version', '1.0.0'),
            'contact': {
                'name': self.config.get('contact_name', 'API Team'),
                'email': self.config.get('contact_email', 'api@example.com')
            },
            'license': {
                'name': self.config.get('license_name', 'MIT'),
                'url': self.config.get('license_url', 'https://opensource.org/licenses/MIT')
            }
        }
    
    def _get_servers(self) -> List[Dict[str, Any]]:
        """Get API servers"""
        servers = []
        
        for env in ['development', 'staging', 'production']:
            servers.append({
                'url': self.config.get(f'{env}_url', f'https://api.{env}.example.com'),
                'description': f'{env.capitalize()} environment'
            })
        
        return servers
    
    def _get_security_schemes(self) -> Dict[str, Any]:
        """Get security schemes"""
        return {
            'bearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'JWT authentication'
            }
        }
    
    def _get_paths(
        self,
        endpoints: List[APIEndpoint]
    ) -> Dict[str, Any]:
        """Get API paths"""
        paths = {}
        
        for endpoint in endpoints:
            path_key = endpoint.path.replace('{id}', '{id}')
            
            if path_key not in paths:
                paths[path_key] = {}
            
            paths[path_key][endpoint.method.lower()] = {
                'summary': endpoint.description,
                'description': endpoint.description,
                'operationId': f"{endpoint.method.lower()}_{endpoint.path.replace('/', '_')}",
                'tags': self._get_endpoint_tags(endpoint),
                'security': [endpoint.authentication] if endpoint.authentication else [],
                'requestBody': self._get_request_body(endpoint),
                'responses': self._get_responses(endpoint)
            }
        
        return paths
    
    def _get_endpoint_tags(self, endpoint: APIEndpoint) -> List[str]:
        """Get tags for endpoint"""
        # Extract resource name from path
        resource = endpoint.path.split('/')[1]
        return [resource]
    
    def _get_request_body(self, endpoint: APIEndpoint) -> Dict[str, Any]:
        """Get request body for endpoint"""
        if endpoint.method in ['POST', 'PUT', 'PATCH']:
            return {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': endpoint.request_schema
                    }
                }
            }
        return {}
    
    def _get_responses(self, endpoint: APIEndpoint) -> Dict[str, Any]:
        """Get responses for endpoint"""
        responses = {
            '200': {
                'description': 'Successful response',
                'content': {
                    'application/json': {
                        'schema': endpoint.response_schema
                    }
                }
            }
        }
        
        # Add error responses
        for error_code, error_info in self.standard_errors.items():
            responses[str(error_info['code'])] = {
                'description': error_info['message'],
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'error': {
                                    'type': 'object',
                                    'properties': {
                                        'code': {'type': 'integer'},
                                        'message': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        
        return responses
    
    def _get_components(self) -> Dict[str, Any]:
        """Get reusable components"""
        return {
            'schemas': self._get_schemas(),
            'securitySchemes': self._get_security_schemes()
        }
    
    def _get_schemas(self) -> Dict[str, Any]:
        """Get reusable schemas"""
        schemas = {}
        
        # Add common schemas
        schemas['Error'] = {
            'type': 'object',
            'properties': {
                'code': {'type': 'integer'},
                'message': {'type': 'string'}
            }
        }
        
        schemas['Pagination'] = {
            'type': 'object',
            'properties': {
                'page': {'type': 'integer', 'minimum': 1},
                'per_page': {'type': 'integer', 'minimum': 1, 'maximum': 100},
                'total': {'type': 'integer'}
            }
        }
        
        return schemas
    
    def _get_tags(self) -> List[Dict[str, Any]]:
        """Get API tags"""
        tags = []
        resources = set()
        
        for endpoint in self.endpoints:
            resource = endpoint.path.split('/')[1]
            if resource not in resources:
                tags.append({
                    'name': resource.capitalize(),
                    'description': f"{resource.capitalize()} operations"
                })
                resources.add(resource)
        
        return tags
```

---

## Tooling & Tech Stack

### API Design Tools
- **OpenAPI/Swagger**: API specification
- **Postman**: API testing and documentation
- **Stoplight**: API design platform
- **Insomnia**: API client

### Documentation Tools
- **Swagger UI**: Interactive API documentation
- **Redoc**: Beautiful API documentation
- **Docusaurus**: Static site generator
- **GitBook**: Documentation platform

### Testing Tools
- **Postman Collections**: API test suites
- **Newman**: CLI for Postman
- **REST Assured**: API testing framework
- **Karate**: API testing framework

### Developer Tools
- **OpenAPI Generator**: Generate client SDKs
- **Swagger Codegen**: Generate server stubs
- **AutoRest**: Generate REST clients
- **NSwag**: Generate Swagger from .NET

---

## Configuration Essentials

### API Configuration

```yaml
# config/api_config.yaml
api:
  name: "My Product API"
  version: "1.0.0"
  description: "API for My Product"
  contact:
    name: "API Team"
    email: "api@example.com"
  
  type: "rest"
  versioning:
    strategy: "url_path"
    supported_versions:
      - "v1"
      - "v2"
  
  servers:
    development:
      url: "https://api-dev.example.com"
      description: "Development environment"
    staging:
      url: "https://api-staging.example.com"
      description: "Staging environment"
    production:
      url: "https://api.example.com"
      description: "Production environment"

design:
  principles:
    consistency:
      naming_convention: "snake_case"
      resource_naming: "plural"
      field_naming: "snake_case"
    
    error_handling:
      standard_errors: true
      error_codes: true
      error_messages: true
    
    pagination:
      strategy: "cursor_based"
      default_page_size: 20
      max_page_size: 100
    
    filtering:
      strategy: "query_params"
      supported_operators:
        - "eq"
        - "ne"
        - "gt"
        - "gte"
        - "like"
        - "in"
    
    sorting:
      strategy: "query_param"
      default_sort: "created_at"

security:
  authentication:
    type: "bearer"
    scheme: "JWT"
    token_expiry: 3600  # seconds
  
  rate_limiting:
    default_limit: 1000  # requests per hour
    burst_limit: 100  # requests per minute

documentation:
  format: "openapi"
  tools:
    - "swagger_ui"
    - "redoc"
  
  output:
    format: "yaml"
    location: "docs/api"
    auto_generate: true
```

---

## Code Examples

### Good: Complete API-First Implementation

```python
# api/design.py
import asyncio
import logging
from typing import Dict, Any, List

from api.designer import APIFirstDesigner
from api.documentation import APIDocumentationGenerator
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def design_api_first_product():
    """Design API-first product"""
    logger.info("=" * 60)
    logger.info("API-First Product Design")
    logger.info("=" * 60)
    
    # Load product requirements
    product_requirements = load_requirements('docs/product_requirements.md')
    
    # Step 1: Design API
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Designing API")
    logger.info("=" * 60)
    
    designer = APIFirstDesigner(settings.api_config)
    endpoints = designer.design_api(product_requirements)
    
    logger.info(f"Designed {len(endpoints)} endpoints")
    
    # Step 2: Validate API design
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Validating API Design")
    logger.info("=" * 60)
    
    validation = designer._validate_api_design()
    
    if not validation['valid']:
        logger.warning("API design validation failed")
        logger.warning(f"Errors: {validation['errors']}")
        logger.warning(f"Warnings: {validation['warnings']}")
        
        # Fix issues
        await fix_design_issues(validation['errors'])
        
        # Re-validate
        validation = designer._validate_api_design()
    
    logger.info("API design validated successfully")
    
    # Step 3: Generate documentation
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Generating API Documentation")
    logger.info("=" * 60)
    
    doc_generator = APIDocumentationGenerator(settings.api_config)
    openapi_spec = doc_generator.generate_openapi_spec(endpoints)
    
    # Save OpenAPI spec
    save_openapi_spec('docs/api/openapi.yaml', openapi_spec)
    
    logger.info("API documentation generated")
    
    # Step 4: Generate SDKs
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Generating SDKs")
    logger.info("=" * 60)
    
    await generate_sdks(endpoints)
    
    logger.info("SDKs generated")
    
    # Step 5: Setup developer portal
    logger.info("\n" + "=" * 60)
    logger.info("Step 5: Setting Up Developer Portal")
    logger.info("=" * 60)
    
    await setup_developer_portal(openapi_spec)
    
    logger.info("Developer portal setup complete")
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("API-First Design Summary")
    logger.info("=" * 60)
    logger.info(f"Endpoints: {len(endpoints)}")
    logger.info(f"Documentation: docs/api/openapi.yaml")
    logger.info(f"SDKs: Generated for multiple languages")
    logger.info(f"Developer Portal: https://developers.example.com")

def load_requirements(filename: str) -> Dict[str, Any]:
    """Load product requirements"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

def save_openapi_spec(filename: str, spec: Dict[str, Any]):
    """Save OpenAPI specification"""
    import yaml
    with open(filename, 'w') as f:
        yaml.dump(spec, f, default_flow_style=False)

async def generate_sdks(endpoints: List[APIEndpoint]):
    """Generate SDKs for multiple languages"""
    # Generate JavaScript SDK
    await generate_javascript_sdk(endpoints)
    
    # Generate Python SDK
    await generate_python_sdk(endpoints)
    
    # Generate Java SDK
    await generate_java_sdk(endpoints)

async def generate_javascript_sdk(endpoints: List[APIEndpoint]):
    """Generate JavaScript SDK"""
    logger.info("Generating JavaScript SDK...")
    # Implementation would use OpenAPI generator
    pass

async def generate_python_sdk(endpoints: List[APIEndpoint]):
    """Generate Python SDK"""
    logger.info("Generating Python SDK...")
    # Implementation would use OpenAPI generator
    pass

async def generate_java_sdk(endpoints: List[APIEndpoint]):
    """Generate Java SDK"""
    logger.info("Generating Java SDK...")
    # Implementation would use OpenAPI generator
    pass

async def setup_developer_portal(spec: Dict[str, Any]):
    """Setup developer portal"""
    logger.info("Setting up developer portal...")
    # Implementation would deploy Swagger UI and Redoc
    pass

async def fix_design_issues(issues: List[str]):
    """Fix API design issues"""
    logger.info("Fixing design issues...")
    # Implementation would fix identified issues
    pass

async def main():
    """Main entry point"""
    await design_api_first_product()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No API design
def bad_product():
    # Skip API design
    build_ui_first()

# BAD: UI-first design
def bad_product():
    # Build UI first, then API
    ui = build_ui()
    api = adapt_to_ui(ui)

# BAD: No documentation
def bad_product():
    # Build API without documentation
    build_api()

# BAD: No SDKs
def bad_product():
    # No developer tools
    build_api_only()

# BAD: No versioning
def bad_product():
    # No version control
    single_version_api()
```

---

## Standards, Compliance & Security

### Industry Standards
- **OpenAPI Specification**: API specification standard
- **REST**: Architectural style for APIs
- **GraphQL**: Query language for APIs
- **OAuth 2.0**: Authorization framework

### Security Best Practices
- **Authentication**: JWT/OAuth2
- **Authorization**: RBAC
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Validate all inputs

### Compliance Requirements
- **Documentation**: Complete API docs
- **Versioning**: Clear version strategy
- **Deprecation**: Proper deprecation policy
- **Privacy**: Data protection compliance

---

## Quick Start

### 1. Install Tools

```bash
pip install pyyaml
pip install openapi-generator
```

### 2. Configure API

```bash
# Copy example config
cp config/api_config.yaml.example config/api_config.yaml

# Edit configuration
vim config/api_config.yaml
```

### 3. Design API

```bash
python api/design.py
```

### 4. View Documentation

```bash
# Open Swagger UI
open http://localhost:8080/swagger-ui

# View OpenAPI spec
cat docs/api/openapi.yaml
```

---

## Production Checklist

### API Design
- [ ] API endpoints designed
- [ ] Naming conventions applied
- [ ] Error handling defined
- [ ] Pagination strategy defined
- [ ] Filtering strategy defined

### Documentation
- [ ] OpenAPI spec generated
- [ ] Swagger UI deployed
- [ ] Redoc deployed
- [ ] Examples provided
- [ ] Tutorials written

### SDKs
- [ ] JavaScript SDK generated
- [ ] Python SDK generated
- [ ] Java SDK generated
- [ ] SDKs tested
- [ ] SDKs documented

### Developer Portal
- [ ] Developer portal deployed
- [ ] API keys management
- [ ] Usage analytics
- [ ] Support documentation
- [ ] Community forum

### Security
- [ ] Authentication implemented
- [ ] Authorization implemented
- [ ] Rate limiting configured
- [ ] Input validation added
- [ ] Security audit passed

---

## Anti-patterns

### ❌ Avoid These Practices

1. **UI-First Design**
   ```python
   # BAD: UI first
   build_ui()
   adapt_api_to_ui()
   ```

2. **No Documentation**
   ```python
   # BAD: No documentation
   build_api()
   ```

3. **No SDKs**
   ```python
   # BAD: No developer tools
   build_api_only()
   ```

4. **No Versioning**
   ```python
   # BAD: No version control
   single_version_api()
   ```

5. **No Validation**
   ```python
   # BAD: No input validation
   @app.route('/users', methods=['POST'])
   def create_user():
       return create_user(request.json)  # No validation
   ```

### ✅ Follow These Practices

1. **API-First Design**
   ```python
   # GOOD: API first
   design_api()
   build_ui_from_api()
   ```

2. **Complete Documentation**
   ```python
   # GOOD: Complete documentation
   generate_openapi_spec()
   deploy_swagger_ui()
   ```

3. **SDKs**
   ```python
   # GOOD: Developer tools
   generate_sdks()
   ```

4. **Versioning**
   ```python
   # GOOD: Version control
   @app.route('/v1/users', methods=['GET'])
   def get_users_v1():
       pass
   
   @app.route('/v2/users', methods=['GET'])
   def get_users_v2():
       pass
   ```

5. **Input Validation**
   ```python
   # GOOD: Input validation
   @app.route('/users', methods=['POST'])
   @validate_request(UserSchema)
   def create_user(data):
       return create_user(data)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 40-80 hours
- **API Design**: 40-60 hours
- **Documentation**: 20-40 hours
- **SDK Development**: 60-100 hours
- **Total**: 160-280 hours

### Operational Costs
- **Documentation Platform**: $50-200/month
- **Developer Portal**: $100-500/month
- **API Gateway**: $200-1000/month
- **Support**: 10-20 hours/month

### ROI Metrics
- **Developer Adoption**: 50-80% increase
- **Integration Time**: 70-90% reduction
- **Support Tickets**: 60-80% reduction
- **Ecosystem Growth**: 2-5x increase

### KPI Targets
- **API Coverage**: 100%
- **Documentation Completeness**: > 95%
- **SDK Quality**: > 90% test coverage
- **Developer Satisfaction**: > 4.5/5.0
- **Time to First Integration**: < 1 hour

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **18. Project Management**: Project planning
- **19. Requirement Analysis**: Requirements gathering

### Parallel Skills
- **138. Platform Product Design**: Platform design
- **139. Product Discovery Validation**: Validation
- **140. Product Analytics Implementation**: Analytics

### Downstream Skills
- **141. Feature Prioritization**: Prioritization
- **142. Technical Debt Prioritization**: Debt management
- **143. Competitive Intelligence**: Competitive analysis
- **144. Product Roadmap Communication**: Roadmap

### Cross-Domain Skills
- **59. Architecture Decision**: Architecture decisions
- **64. Meta Standards**: Coding standards
- **84. Compliance AI Governance**: Compliance
- **14. Monitoring and Observability**: API monitoring

---

## References & Resources

### Documentation
- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API Design Best Practices](https://restfulapi.net/)
- [GraphQL Specification](https://graphql.org/learn/)
- [OAuth 2.0](https://oauth.net/2/)

### Best Practices
- [API Design Best Practices](https://apihandbook.com/)
- [REST API Tutorial](https://restfulapi.net/)
- [API Security Best Practices](https://owasp.org/www-project-api-security)

### Tools & Libraries
- [Swagger/OpenAPI](https://swagger.io/)
- [Postman](https://www.postman.com/)
- [Stoplight](https://stoplight.io/)
- [Redoc](https://github.com/Redocly/redoc)
