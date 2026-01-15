# Test Data Factory

## Overview

Test data factories provide a clean, reusable way to create test data. This skill covers factory patterns, libraries (Factory Boy, Fishery), fixture factories, Faker integration, database seeding, realistic test data, data relationships, performance considerations, reusability, and best practices.

## Table of Contents

1. [Factory Pattern for Tests](#factory-pattern-for-tests)
2. [Libraries](#libraries)
   - [Factory Boy (Python)](#factory-boy-python)
   - [Fishery (TypeScript)](#fishery-typescript)
3. [Fixture Factories](#fixture-factories)
4. [Faker Integration](#faker-integration)
5. [Database Seeding](#database-seeding)
6. [Realistic Test Data](#realistic-test-data)
7. [Data Relationships](#data-relationships)
8. [Performance Considerations](#performance-considerations)
9. [Reusability](#reusability)
10. [Best Practices](#best-practices)

---

## Factory Pattern for Tests

### Basic Factory Pattern

```python
# test/factories/base_factory.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseFactory(ABC):
    """Base factory class for creating test data."""
    
    @classmethod
    @abstractmethod
    def create(cls, **kwargs) -> Any:
        """Create a single instance."""
        pass
    
    @classmethod
    @abstractmethod
    def create_batch(cls, count: int, **kwargs) -> list:
        """Create multiple instances."""
        pass
```

### Simple Factory Implementation

```python
# test/factories/user_factory.py
from typing import Dict, Optional
from test.factories.base_factory import BaseFactory

class UserFactory(BaseFactory):
    """Factory for creating test users."""
    
    _counter = 0
    
    @classmethod
    def create(cls, **kwargs) -> Dict:
        """Create a single user."""
        cls._counter += 1
        
        defaults = {
            'id': cls._counter,
            'name': f'Test User {cls._counter}',
            'email': f'user{cls._counter}@example.com',
            'age': 30,
            'active': True,
        }
        
        defaults.update(kwargs)
        return defaults
    
    @classmethod
    def create_batch(cls, count: int, **kwargs) -> list:
        """Create multiple users."""
        return [cls.create(**kwargs) for _ in range(count)]
    
    @classmethod
    def reset_counter(cls):
        """Reset the counter."""
        cls._counter = 0
```

### Using the Factory

```python
# test/test_user.py
import pytest
from test.factories.user_factory import UserFactory

def test_create_user():
    """Test creating a user."""
    user = UserFactory.create()
    
    assert user['id'] == 1
    assert user['name'] == 'Test User 1'
    assert user['email'] == 'user1@example.com'

def test_create_user_with_overrides():
    """Test creating a user with overrides."""
    user = UserFactory.create(
        name='Custom Name',
        email='custom@example.com',
    )
    
    assert user['name'] == 'Custom Name'
    assert user['email'] == 'custom@example.com'

def test_create_batch_users():
    """Test creating multiple users."""
    users = UserFactory.create_batch(5)
    
    assert len(users) == 5
    assert users[0]['id'] == 1
    assert users[4]['id'] == 5
```

---

## Libraries

### Factory Boy (Python)

#### Installation

```bash
pip install factory-boy
```

#### Basic Usage

```python
# test/factories/user_factory.py
import factory
from datetime import datetime, timedelta
from src.models import User

class UserFactory(factory.Factory):
    """Factory for User model."""
    
    class Meta:
        model = User
    
    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    email = factory.Faker('email')
    age = factory.Faker('random_int', min=18, max=80)
    active = True
    created_at = factory.LazyFunction(datetime.now)
```

#### Using Factory Boy

```python
# test/test_user.py
import pytest
from test.factories.user_factory import UserFactory

def test_create_user():
    """Test creating a user."""
    user = UserFactory()
    
    assert user.id is not None
    assert user.name is not None
    assert user.email is not None
    assert user.age >= 18
    assert user.active is True

def test_create_user_with_overrides():
    """Test creating a user with overrides."""
    user = UserFactory(
        name='Custom Name',
        email='custom@example.com',
        age=25,
    )
    
    assert user.name == 'Custom Name'
    assert user.email == 'custom@example.com'
    assert user.age == 25

def test_create_batch_users():
    """Test creating multiple users."""
    users = UserFactory.create_batch(5)
    
    assert len(users) == 5
    assert all(u.id is not None for u in users)
```

#### Related Factories

```python
# test/factories/post_factory.py
import factory
from src.models import Post
from test.factories.user_factory import UserFactory

class PostFactory(factory.Factory):
    """Factory for Post model."""
    
    class Meta:
        model = Post
    
    id = factory.Sequence(lambda n: n)
    title = factory.Faker('sentence', nb_words=5)
    content = factory.Faker('text')
    published = False
    created_at = factory.LazyFunction(datetime.now)
    
    # Foreign key relationship
    author = factory.SubFactory(UserFactory)
```

```python
# test/test_post.py
import pytest
from test.factories.post_factory import PostFactory

def test_create_post():
    """Test creating a post."""
    post = PostFactory()
    
    assert post.id is not None
    assert post.title is not None
    assert post.content is not None
    assert post.author is not None

def test_create_post_with_custom_author():
    """Test creating a post with a custom author."""
    custom_author = UserFactory(name='Custom Author')
    post = PostFactory(author=custom_author)
    
    assert post.author.name == 'Custom Author'
```

#### Lazy Attributes

```python
# test/factories/order_factory.py
import factory
from src.models import Order
from test.factories.user_factory import UserFactory

class OrderFactory(factory.Factory):
    """Factory for Order model."""
    
    class Meta:
        model = Order
    
    id = factory.Sequence(lambda n: n)
    status = 'pending'
    total = factory.LazyAttribute(lambda o: sum(item.price * item.quantity for item in o.items))
    created_at = factory.LazyFunction(datetime.now)
    
    author = factory.SubFactory(UserFactory)
    items = factory.List([
        factory.SubFactory('test.factories.order_item_factory.OrderItemFactory'),
    ])
```

---

### Fishery (TypeScript)

#### Installation

```bash
npm install fishery
```

#### Basic Usage

```typescript
// test/factories/user.factory.ts
import { Factory } from 'fishery';
import { faker } from '@faker-js/faker';

interface User {
  id: number;
  name: string;
  email: string;
  age: number;
  active: boolean;
  createdAt: Date;
}

const userFactory = Factory.define<User>(({ sequence }) => ({
  id: sequence,
  name: faker.person.fullName(),
  email: faker.internet.email(),
  age: faker.number.int({ min: 18, max: 80 }),
  active: true,
  createdAt: new Date(),
}));

export default userFactory;
```

#### Using Fishery

```typescript
// test/user.test.ts
import { describe, it, expect } from '@jest/globals';
import userFactory from '../factories/user.factory';

describe('User Factory', () => {
  it('should create a user', () => {
    const user = userFactory.build();
    
    expect(user.id).toBeDefined();
    expect(user.name).toBeDefined();
    expect(user.email).toBeDefined();
    expect(user.age).toBeGreaterThanOrEqual(18);
    expect(user.active).toBe(true);
  });

  it('should create a user with overrides', () => {
    const user = userFactory.build({
      name: 'Custom Name',
      email: 'custom@example.com',
      age: 25,
    });
    
    expect(user.name).toBe('Custom Name');
    expect(user.email).toBe('custom@example.com');
    expect(user.age).toBe(25);
  });

  it('should create multiple users', () => {
    const users = userFactory.buildList(5);
    
    expect(users).toHaveLength(5);
    expect(users[0].id).toBe(0);
    expect(users[4].id).toBe(4);
  });
});
```

#### Related Factories

```typescript
// test/factories/post.factory.ts
import { Factory } from 'fishery';
import { faker } from '@faker-js/faker';
import userFactory from './user.factory';

interface Post {
  id: number;
  title: string;
  content: string;
  published: boolean;
  createdAt: Date;
  author: User;
}

const postFactory = Factory.define<Post>(({ sequence, associations }) => ({
  id: sequence,
  title: faker.lorem.sentence(5),
  content: faker.lorem.paragraph(),
  published: false,
  createdAt: new Date(),
  author: associations.author || userFactory.build(),
}));

export default postFactory;
```

```typescript
// test/post.test.ts
import { describe, it, expect } from '@jest/globals';
import postFactory from '../factories/post.factory';
import userFactory from '../factories/user.factory';

describe('Post Factory', () => {
  it('should create a post', () => {
    const post = postFactory.build();
    
    expect(post.id).toBeDefined();
    expect(post.title).toBeDefined();
    expect(post.content).toBeDefined();
    expect(post.author).toBeDefined();
  });

  it('should create a post with a custom author', () => {
    const customAuthor = userFactory.build({ name: 'Custom Author' });
    const post = postFactory.build({ author: customAuthor });
    
    expect(post.author.name).toBe('Custom Author');
  });
});
```

---

## Fixture Factories

### Pytest Fixtures

```python
# test/conftest.py
import pytest
from test.factories.user_factory import UserFactory
from test.factories.post_factory import PostFactory

@pytest.fixture
def user():
    """Create a user."""
    return UserFactory.create()

@pytest.fixture
def users():
    """Create multiple users."""
    return UserFactory.create_batch(5)

@pytest.fixture
def post(user):
    """Create a post with a user."""
    return PostFactory.create(author=user)

@pytest.fixture
def posts(user):
    """Create multiple posts with a user."""
    return PostFactory.create_batch(5, author=user)
```

```python
# test/test_user.py
import pytest

def test_with_user_fixture(user):
    """Test using user fixture."""
    assert user['id'] is not None
    assert user['name'] is not None

def test_with_users_fixture(users):
    """Test using users fixture."""
    assert len(users) == 5
    assert all(u['id'] is not None for u in users)
```

### Jest Fixtures

```typescript
// test/fixtures/user.fixture.ts
import userFactory from '../factories/user.factory';

export const userFixture = () => {
  return userFactory.build();
};

export const usersFixture = (count: number = 5) => {
  return userFactory.buildList(count);
};
```

```typescript
// test/user.test.ts
import { describe, it, expect } from '@jest/globals';
import { userFixture, usersFixture } from './fixtures/user.fixture';

describe('User Fixture', () => {
  it('should create a user', () => {
    const user = userFixture();
    
    expect(user.id).toBeDefined();
    expect(user.name).toBeDefined();
  });

  it('should create multiple users', () => {
    const users = usersFixture(5);
    
    expect(users).toHaveLength(5);
  });
});
```

---

## Faker Integration

### Python Faker

```python
# test/factories/faker_factory.py
from faker import Faker

fake = Faker()

def fake_user():
    """Generate fake user data."""
    return {
        'id': fake.random_int(min=1, max=10000),
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'city': fake.city(),
        'state': fake.state(),
        'zip_code': fake.zipcode(),
        'country': fake.country(),
        'age': fake.random_int(min=18, max=80),
        'active': fake.boolean(),
        'created_at': fake.date_time_this_year(),
    }

def fake_product():
    """Generate fake product data."""
    return {
        'id': fake.random_int(min=1, max=10000),
        'name': fake.word(),
        'description': fake.text(),
        'price': fake.pyfloat(left_digits=3, right_digits=2, positive=True),
        'stock': fake.random_int(min=0, max=100),
        'category': fake.word(),
        'sku': fake.uuid4(),
        'created_at': fake.date_time_this_year(),
    }

def fake_order():
    """Generate fake order data."""
    return {
        'id': fake.random_int(min=1, max=10000),
        'user_id': fake.random_int(min=1, max=1000),
        'status': fake.random_element(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
        'total': fake.pyfloat(left_digits=4, right_digits=2, positive=True),
        'created_at': fake.date_time_this_year(),
    }
```

### TypeScript Faker

```typescript
// test/factories/faker.factory.ts
import { faker } from '@faker-js/faker';

export const fakeUser = () => ({
  id: faker.number.int({ min: 1, max: 10000 }),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  phone: faker.phone.number(),
  address: faker.location.streetAddress(),
  city: faker.location.city(),
  state: faker.location.state({ abbreviated: true }),
  zipCode: faker.location.zipCode(),
  country: faker.location.country(),
  age: faker.number.int({ min: 18, max: 80 }),
  active: faker.datatype.boolean(),
  createdAt: faker.date.recent(),
});

export const fakeProduct = () => ({
  id: faker.number.int({ min: 1, max: 10000 }),
  name: faker.commerce.productName(),
  description: faker.commerce.productDescription(),
  price: parseFloat(faker.commerce.price()),
  stock: faker.number.int({ min: 0, max: 100 }),
  category: faker.commerce.department(),
  sku: faker.string.uuid(),
  createdAt: faker.date.recent(),
});

export const fakeOrder = () => ({
  id: faker.number.int({ min: 1, max: 10000 }),
  userId: faker.number.int({ min: 1, max: 1000 }),
  status: faker.helpers.arrayElement(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
  total: parseFloat(faker.commerce.price({ min: 10, max: 1000 })),
  createdAt: faker.date.recent(),
});
```

---

## Database Seeding

### Python Database Seeding

```python
# test/seeds/database_seed.py
from test.factories.user_factory import UserFactory
from test.factories.post_factory import PostFactory
from src.database import db

def seed_database():
    """Seed the database with test data."""
    # Create users
    users = UserFactory.create_batch(10)
    for user_data in users:
        db.session.add(User(**user_data))
    
    db.session.commit()
    
    # Create posts
    posts = PostFactory.create_batch(50)
    for post_data in posts:
        db.session.add(Post(**post_data))
    
    db.session.commit()
    
    print(f'Created {len(users)} users and {len(posts)} posts')

def clear_database():
    """Clear the database."""
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.commit()
    print('Database cleared')
```

```python
# test/conftest.py
import pytest
from test.seeds.database_seed import seed_database, clear_database

@pytest.fixture(scope='function')
def database():
    """Setup and teardown database."""
    clear_database()
    seed_database()
    yield
    clear_database()
```

### TypeScript Database Seeding

```typescript
// test/seeds/database.seed.ts
import userFactory from '../factories/user.factory';
import postFactory from '../factories/post.factory';
import { db } from '../src/database';

export const seedDatabase = async () => {
  // Create users
  const users = userFactory.buildList(10);
  for (const userData of users) {
    await db.user.create(userData);
  }
  
  // Create posts
  const posts = postFactory.buildList(50);
  for (const postData of posts) {
    await db.post.create(postData);
  }
  
  console.log(`Created ${users.length} users and ${posts.length} posts`);
};

export const clearDatabase = async () => {
  await db.post.deleteMany();
  await db.user.deleteMany();
  console.log('Database cleared');
};
```

---

## Realistic Test Data

### Domain-Specific Data

```python
# test/factories/ecommerce_factory.py
from faker import Faker

fake = Faker()

def fake_ecommerce_user():
    """Generate realistic e-commerce user data."""
    return {
        'id': fake.random_int(min=1, max=10000),
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'city': fake.city(),
        'state': fake.state(),
        'zip_code': fake.zipcode(),
        'country': fake.country(),
        'age': fake.random_int(min=18, max=80),
        'active': fake.boolean(),
        'created_at': fake.date_time_this_year(),
        'last_login': fake.date_time_this_month(),
        'order_count': fake.random_int(min=0, max=100),
        'total_spent': fake.pyfloat(left_digits=4, right_digits=2, positive=True),
    }

def fake_ecommerce_product():
    """Generate realistic e-commerce product data."""
    return {
        'id': fake.random_int(min=1, max=10000),
        'name': fake.word(),
        'description': fake.text(),
        'price': fake.pyfloat(left_digits=3, right_digits=2, positive=True),
        'stock': fake.random_int(min=0, max=100),
        'category': fake.word(),
        'sku': fake.uuid4(),
        'weight': fake.pyfloat(left_digits=2, right_digits=2, positive=True),
        'dimensions': f'{fake.random_int(min=1, max=20)}x{fake.random_int(min=1, max=20)}x{fake.random_int(min=1, max=20)}',
        'created_at': fake.date_time_this_year(),
    }
```

### Realistic Relationships

```python
# test/factories/realistic_factory.py
from faker import Faker

fake = Faker()

def realistic_order():
    """Generate realistic order with relationships."""
    # Create user
    user = fake_ecommerce_user()
    
    # Create products
    products = [fake_ecommerce_product() for _ in range(fake.random_int(min=1, max=5))]
    
    # Create order items
    order_items = []
    total = 0
    for product in products:
        quantity = fake.random_int(min=1, max=10)
        subtotal = product['price'] * quantity
        total += subtotal
        order_items.append({
            'product_id': product['id'],
            'quantity': quantity,
            'price': product['price'],
            'subtotal': subtotal,
        })
    
    # Create order
    order = {
        'id': fake.random_int(min=1, max=10000),
        'user_id': user['id'],
        'status': fake.random_element(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
        'total': total,
        'shipping_address': user['address'],
        'billing_address': user['address'],
        'payment_method': fake.random_element(['credit_card', 'debit_card', 'paypal']),
        'created_at': fake.date_time_this_year(),
        'items': order_items,
    }
    
    return {
        'user': user,
        'products': products,
        'order': order,
    }
```

---

## Data Relationships

### One-to-Many Relationships

```python
# test/factories/one_to_many_factory.py
from test.factories.user_factory import UserFactory
from test.factories.post_factory import PostFactory

def user_with_posts(post_count=5):
    """Create a user with multiple posts."""
    user = UserFactory.create()
    posts = PostFactory.create_batch(post_count, author=user)
    
    return {
        'user': user,
        'posts': posts,
    }
```

### Many-to-Many Relationships

```python
# test/factories/many_to_many_factory.py
from test.factories.user_factory import UserFactory
from test.factories/product_factory import ProductFactory

def users_with_products(user_count=5, product_count=10):
    """Create users with products (many-to-many)."""
    users = UserFactory.create_batch(user_count)
    products = ProductFactory.create_batch(product_count)
    
    # Assign products to users
    user_products = []
    for user in users:
        for product in products:
            if fake.boolean(chance_of_getting_true=30):  # 30% chance
                user_products.append({
                    'user_id': user['id'],
                    'product_id': product['id'],
                })
    
    return {
        'users': users,
        'products': products,
        'user_products': user_products,
    }
```

### Nested Relationships

```python
# test/factories/nested_factory.py
from test.factories.user_factory import UserFactory
from test.factories/order_factory import OrderFactory
from test.factories/order_item_factory import OrderItemFactory

def user_with_orders(order_count=3):
    """Create a user with orders and order items."""
    user = UserFactory.create()
    
    orders = []
    for _ in range(order_count):
        order = OrderFactory.create(user=user)
        items = OrderItemFactory.create_batch(fake.random_int(min=1, max=5), order=order)
        orders.append({
            'order': order,
            'items': items,
        })
    
    return {
        'user': user,
        'orders': orders,
    }
```

---

## Performance Considerations

### Batch Creation

```python
# test/factories/batch_factory.py
from test.factories.user_factory import UserFactory

def create_users_fast(count=1000):
    """Create users efficiently using batch operations."""
    users = UserFactory.create_batch(count)
    
    # Batch insert into database
    db.session.bulk_insert_mappings(User, users)
    db.session.commit()
    
    return users
```

### Lazy Loading

```typescript
// test/factories/lazy.factory.ts
import { Factory } from 'fishery';
import { faker } from '@faker-js/faker';

interface User {
  id: number;
  name: string;
  email: string;
  posts?: Post[];
}

interface Post {
  id: number;
  title: string;
  content: string;
  author: User;
}

const userFactory = Factory.define<User>(({ sequence }) => ({
  id: sequence,
  name: faker.person.fullName(),
  email: faker.internet.email(),
}));

const postFactory = Factory.define<Post>(({ sequence, associations }) => ({
  id: sequence,
  title: faker.lorem.sentence(5),
  content: faker.lorem.paragraph(),
  author: associations.author || userFactory.build(),
}));

// Lazy load posts
export const userWithPosts = () => {
  const user = userFactory.build();
  const posts = postFactory.buildList(5, { author: user });
  
  return {
    ...user,
    posts,
  };
};
```

---

## Reusability

### Generic Factory

```python
# test/factories/generic_factory.py
from typing import TypeVar, Generic, Dict, Any

T = TypeVar('T')

class GenericFactory(Generic[T]):
    """Generic factory for creating test data."""
    
    def __init__(self, defaults: Dict[str, Any]):
        self.defaults = defaults
    
    def create(self, **kwargs) -> T:
        """Create a single instance."""
        data = self.defaults.copy()
        data.update(kwargs)
        return data
    
    def create_batch(self, count: int, **kwargs) -> list:
        """Create multiple instances."""
        return [self.create(**kwargs) for _ in range(count)]
```

### Using Generic Factory

```python
# test/factories/user_factory.py
from test.factories.generic_factory import GenericFactory

user_factory = GenericFactory({
    'id': 1,
    'name': 'Test User',
    'email': 'test@example.com',
    'age': 30,
    'active': True,
})
```

---

## Best Practices

### 1. Use Factories for Test Data

```python
# Good: Use factories
from test.factories.user_factory import UserFactory

def test_create_user():
    user = UserFactory.create()
    assert user['id'] is not None

# Bad: Hardcode test data
def test_create_user():
    user = {
        'id': 1,
        'name': 'Test User',
        'email': 'test@example.com',
    }
    assert user['id'] is not None
```

### 2. Use Faker for Realistic Data

```python
# Good: Use Faker
from faker import Faker

fake = Faker()
user = {
    'name': fake.name(),
    'email': fake.email(),
}

# Bad: Hardcode data
user = {
    'name': 'Test User',
    'email': 'test@example.com',
}
```

### 3. Clean Up After Tests

```python
# Good: Clean up after tests
@pytest.fixture
def user():
    user = UserFactory.create()
    yield user
    UserFactory.delete(user['id'])

# Bad: No cleanup
@pytest.fixture
def user():
    return UserFactory.create()
```

### 4. Use Fixtures Effectively

```python
# Good: Reusable fixtures
@pytest.fixture
def user():
    return UserFactory.create()

@pytest.fixture
def users():
    return UserFactory.create_batch(5)

# Bad: Duplicated code
def test_1():
    user = UserFactory.create()

def test_2():
    user = UserFactory.create()
```

### 5. Keep Factories Simple

```python
# Good: Simple factory
class UserFactory(BaseFactory):
    @classmethod
    def create(cls, **kwargs):
        defaults = {
            'id': 1,
            'name': 'Test User',
        }
        defaults.update(kwargs)
        return defaults

# Bad: Complex factory
class UserFactory(BaseFactory):
    @classmethod
    def create(cls, **kwargs):
        # Complex logic
        if 'email' not in kwargs:
            kwargs['email'] = f'user{cls._counter}@example.com'
        # More complex logic
        return {**defaults, **kwargs}
```

---

## Summary

This skill covers comprehensive test data factory patterns including:

- **Factory Pattern**: Basic factory pattern, simple implementation, usage
- **Libraries**: Factory Boy (Python) and Fishery (TypeScript) with examples
- **Fixture Factories**: Pytest and Jest fixtures
- **Faker Integration**: Python and TypeScript Faker for realistic data
- **Database Seeding**: Database seeding and clearing
- **Realistic Test Data**: Domain-specific data, realistic relationships
- **Data Relationships**: One-to-many, many-to-many, nested relationships
- **Performance Considerations**: Batch creation, lazy loading
- **Reusability**: Generic factories
- **Best Practices**: Use factories, use Faker, clean up, use fixtures, keep simple
