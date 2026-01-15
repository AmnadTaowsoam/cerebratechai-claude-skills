# Test Data Factory

A comprehensive guide to test data factory patterns for applications.

## Table of Contents

1. [Factory Pattern for Tests](#factory-pattern-for-tests)
2. [Libraries](#libraries)
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

```typescript
// factories/UserFactory.ts
export class UserFactory {
  static create(overrides: Partial<User> = {}): User {
    return {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
      createdAt: new Date(),
      ...overrides,
    };
  }

  static createMany(count: number, overrides: Partial<User> = {}): User[] {
    return Array.from({ length: count }, (_, i) =>
      this.create({
        ...overrides,
        id: (i + 1).toString(),
      })
    );
  }
}

// Usage
const user = UserFactory.create();
const users = UserFactory.createMany(5);
```

```python
# factories/user_factory.py
class UserFactory:
    @staticmethod
    def create(overrides=None):
        if overrides is None:
            overrides = {}
        return {
            'id': '1',
            'name': 'John Doe',
            'email': 'john@example.com',
            'created_at': datetime.now(),
            **overrides
        }

    @staticmethod
    def create_many(count, overrides=None):
        if overrides is None:
            overrides = {}
        return [
            UserFactory.create({
                **overrides,
                'id': str(i + 1)
            })
            for i in range(count)
        ]

# Usage
user = UserFactory.create()
users = UserFactory.create_many(5)
```

### Factory with Sequences

```typescript
// factories/UserFactory.ts
let userIdSequence = 1;

export class UserFactory {
  static create(overrides: Partial<User> = {}): User {
    return {
      id: userIdSequence++.toString(),
      name: 'John Doe',
      email: `user${userIdSequence}@example.com`,
      createdAt: new Date(),
      ...overrides,
    };
  }
}
```

```python
# factories/user_factory.py
class UserFactory:
    _user_id_sequence = 1

    @classmethod
    def create(cls, overrides=None):
        if overrides is None:
            overrides = {}
        return {
            'id': str(cls._user_id_sequence),
            'name': 'John Doe',
            'email': f'user{cls._user_id_sequence}@example.com',
            'created_at': datetime.now(),
            **overrides
        }
        cls._user_id_sequence += 1
```

---

## Libraries

### Factory Boy (Python)

```python
# factories/user_factory.py
import factory
from datetime import datetime, timedelta
from myapp.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    email = factory.LazyAttribute(lambda o: f"{o.name.lower().replace(' ', '.')}@example.com")
    created_at = factory.LazyAttribute(lambda o: datetime.now() - timedelta(days=random.randint(0, 365)))
    is_active = True

# Usage
user = UserFactory()
users = UserFactory.create_batch(5)
```

### Fishery (TypeScript)

```typescript
// factories/UserFactory.ts
import { Factory } from 'fishery';
import { User } from '../models/User';

export const UserFactory = Factory.define<User, UserProps, UserBuild>(() => ({
  id: sequence(() => seq++),
  name: faker.name.fullName(),
  email: faker.internet.email(),
  createdAt: faker.date.recent(),
  isActive: true,
}));

// Usage
const user = UserFactory.build();
const users = UserFactory.buildMany(5);
```

### Rosie (Ruby)

```ruby
# spec/factories/user_factory.rb
FactoryBot.define do
  factory :user do
    id { 1 }
    name { "John Doe" }
    email { "user-#{id}@example.com" }
    created_at { Time.now }
    is_active { true }
  end
end

# Usage
user = create(:user)
users = create_list(:user, 5)
```

---

## Fixture Factories

### Pytest Fixtures

```python
# conftest.py
import pytest
from factories.user_factory import UserFactory

@pytest.fixture
def user():
    """Create a single user"""
    return UserFactory.create()

@pytest.fixture
def users():
    """Create multiple users"""
    return UserFactory.create_many(5)

@pytest.fixture
def admin_user():
    """Create an admin user"""
    return UserFactory.create({
        'is_admin': True,
        'role': 'admin'
    })
```

### Jest Fixtures

```typescript
// fixtures/userFixtures.ts
import { UserFactory } from '../factories/UserFactory';

export const userFixture = () => {
  return UserFactory.create();
};

export const usersFixture = (count: number = 5) => {
  return UserFactory.createMany(count);
};

// Usage in tests
import { userFixture, usersFixture } from '../fixtures/userFixtures';

beforeEach(() => {
  user = userFixture();
  users = usersFixture(10);
});
```

### Playwright Fixtures

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test';
import { UserFactory } from '../factories/UserFactory';

type MyFixtures = {
  user: User;
  users: User[];
};

const test = base.extend<MyFixtures>({
  user: async ({}, use) => {
    const user = UserFactory.create();
    await use(user);
  },
  users: async ({}, use) => {
    const users = UserFactory.createMany(5);
    await use(users);
  },
});

export { test };
```

---

## Faker Integration

### Basic Faker Usage (Python)

```python
from faker import Faker

fake = Faker()

# Generate fake data
name = fake.name()
email = fake.email()
phone = fake.phone_number()
address = fake.address()
text = fake.text()
date = fake.date()
company = fake.company()
job = fake.job()
```

### Basic Faker Usage (TypeScript)

```typescript
import { faker } from '@faker-js/faker';

// Generate fake data
const name = faker.person.fullName();
const email = faker.internet.email();
const phone = faker.phone.number();
const address = faker.location.streetAddress();
const text = faker.lorem.paragraph();
const date = faker.date.recent();
const company = faker.company.name();
const job = faker.person.jobTitle();
```

### Faker with Factory

```python
# factories/user_factory.py
import factory
from faker import Faker
from myapp.models import User

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: fake.name())
    email = factory.LazyAttribute(lambda o: fake.email())
    phone = factory.LazyAttribute(lambda o: fake.phone_number())
    address = factory.LazyAttribute(lambda o: fake.address())
    bio = factory.LazyAttribute(lambda o: fake.text(max_nb_chars=200))
    birth_date = factory.LazyAttribute(lambda o: fake.date_of_birth(minimum_age=18, maximum_age=90))
```

```typescript
// factories/UserFactory.ts
import { Factory } from 'fishery';
import { faker } from '@faker-js/faker';
import { User } from '../models/User';

export const UserFactory = Factory.define<User, UserProps, UserBuild>(() => ({
  id: sequence(() => seq++),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  phone: faker.phone.number(),
  address: faker.location.streetAddress(),
  bio: faker.lorem.paragraph(),
  birthDate: faker.date.birthdate({ min: 1970, max: 2000, mode: 'age' }),
}));
```

### Localization

```python
from faker import Faker

# English
fake_en = Faker('en_US')
name_en = fake_en.name()

# Thai
fake_th = Faker('th_TH')
name_th = fake_th.name()

# Japanese
fake_ja = Faker('ja_JP')
name_ja = fake_ja.name()
```

```typescript
import { faker } from '@faker-js/faker/locale/th';

// Thai
fakerTH = faker({ locale: 'th' });
const nameTH = fakerTH.person.fullName();
```

---

## Database Seeding

### Seeding with Factories (Python)

```python
# tests/conftest.py
import pytest
from factories.user_factory import UserFactory
from myapp.database import db
from myapp.models import User

@pytest.fixture(scope="session", autouse=True)
def seed_database():
    """Seed database with test data"""
    # Create users
    users = UserFactory.create_batch(10)

    # Save to database
    db.session.add_all([User(**user) for user in users])
    db.session.commit()

    yield

    # Cleanup
    db.session.query(User).delete()
    db.session.commit()
```

### Seeding with Factories (TypeScript)

```typescript
// tests/setup.ts
import { UserFactory } from '../factories/UserFactory';
import { prisma } from '../lib/prisma';

export async function seedDatabase() {
  // Create users
  const users = UserFactory.createMany(10);

  // Save to database
  for (const user of users) {
    await prisma.user.create({ data: user });
  }
}

export async function cleanupDatabase() {
  await prisma.user.deleteMany({});
}
```

### Seeding with Relationships

```python
# tests/conftest.py
import pytest
from factories.user_factory import UserFactory
from factories.post_factory import PostFactory
from myapp.database import db
from myapp.models import User, Post

@pytest.fixture(scope="session", autouse=True)
def seed_database_with_relationships():
    """Seed database with related data"""
    # Create users
    users = UserFactory.create_batch(5)

    # Save users to database
    db_users = [User(**user) for user in users]
    db.session.add_all(db_users)
    db.session.commit()

    # Create posts for each user
    for user in db_users:
        posts = PostFactory.create_batch(3, {'user_id': user.id})
        db.session.add_all([Post(**post) for post in posts])

    db.session.commit()

    yield

    # Cleanup
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.commit()
```

---

## Realistic Test Data

### Realistic User Data

```python
# factories/user_factory.py
import factory
from faker import Faker

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.LazyAttribute(lambda o: fake.name())
    email = factory.LazyAttribute(lambda o: fake.email())
    phone = factory.LazyAttribute(lambda o: fake.phone_number())
    birth_date = factory.LazyAttribute(lambda o: fake.date_of_birth(minimum_age=18, maximum_age=90))
    avatar_url = factory.LazyAttribute(lambda o: fake.image_url())
    bio = factory.LazyAttribute(lambda o: fake.paragraph(nb_sentences=3))
    website = factory.LazyAttribute(lambda o: fake.url())
    location = factory.LazyAttribute(lambda o: fake.city())
```

### Realistic E-commerce Data

```python
# factories/product_factory.py
import factory
from faker import Faker

fake = Faker()

class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda o: fake.sentence(nb_words=3))
    description = factory.LazyAttribute(lambda o: fake.paragraph(nb_sentences=5))
    price = factory.LazyAttribute(lambda o: fake.pyfloat(left_digits=2, right_digits=2, positive=True))
    sku = factory.LazyAttribute(lambda o: fake.bothify(text=fake.word()).upper())
    stock = factory.LazyAttribute(lambda o: fake.random_int(min=0, max=100))
    weight = factory.LazyAttribute(lambda o: fake.pyfloat(left_digits=1, right_digits=2, positive=True))
    category = factory.SubFactory(CategoryFactory)
    images = factory.LazyAttribute(lambda o: [fake.image_url() for _ in range(3)])
```

### Realistic Blog Data

```python
# factories/post_factory.py
import factory
from faker import Faker

fake = Faker()

class PostFactory(factory.Factory):
    class Meta:
        model = Post

    title = factory.LazyAttribute(lambda o: fake.sentence(nb_words=8))
    content = factory.LazyAttribute(lambda o: fake.paragraph(nb_sentences=10))
    excerpt = factory.LazyAttribute(lambda o: fake.paragraph(nb_sentences=2))
    slug = factory.LazyAttribute(lambda o: fake.slug())
    published_at = factory.LazyAttribute(lambda o: fake.date_time_this_year())
    view_count = factory.LazyAttribute(lambda o: fake.random_int(min=0, max=10000))
    like_count = factory.LazyAttribute(lambda o: fake.random_int(min=0, max=1000))
    comment_count = factory.LazyAttribute(lambda o: fake.random_int(min=0, max=100))
```

---

## Data Relationships

### One-to-Many Relationship

```python
# factories/user_factory.py
class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker('name')
    email = factory.Faker('email')

# factories/post_factory.py
class PostFactory(factory.Factory):
    class Meta:
        model = Post

    title = factory.Faker('sentence')
    content = factory.Faker('paragraph')
    author = factory.SubFactory(UserFactory)

# Usage
user = UserFactory()
posts = PostFactory.create_batch(5, author=user)
```

```typescript
// factories/UserFactory.ts
export const UserFactory = Factory.define<User, UserProps, UserBuild>(() => ({
  id: sequence(() => seq++),
  name: faker.person.fullName(),
  email: faker.internet.email(),
}));

// factories/PostFactory.ts
export const PostFactory = Factory.define<Post, PostProps, PostBuild>(() => ({
  id: sequence(() => seq++),
  title: faker.lorem.sentence(),
  content: faker.lorem.paragraph(),
  author: UserFactory,
}));
```

### Many-to-Many Relationship

```python
# factories/user_factory.py
class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker('name')
    email = factory.Faker('email')

# factories/group_factory.py
class GroupFactory(factory.Factory):
    class Meta:
        model = Group

    name = factory.Faker('word')

# Usage
users = UserFactory.create_batch(5)
group = GroupFactory()

# Add users to group
for user in users:
    group.users.append(user)
```

### Nested Relationships

```python
# factories/order_factory.py
class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    items = factory.RelatedFactoryList('ItemFactory', factory_related_name='order')
    total = factory.LazyAttribute(lambda o: sum(item.price for item in o.items))
    status = 'pending'
```

---

## Performance Considerations

### Lazy Loading

```python
# factories/user_factory.py
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User

    # Lazy evaluation
    name = factory.LazyAttribute(lambda o: fake.name())
    email = factory.LazyAttribute(lambda o: fake.email())
    profile = factory.SubFactory('ProfileFactory')
```

### Batch Creation

```python
# Efficient batch creation
def create_large_batch(count):
    batch_size = 1000
    for i in range(0, count, batch_size):
        users = UserFactory.create_batch(batch_size)
        db.session.add_all([User(**user) for user in users])
        db.session.commit()
        db.session.flush()
```

### Caching

```python
# Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_data():
    # Expensive operation
    return expensive_computation()
```

---

## Reusability

### Shared Traits

```python
# factories/traits.py
class UserTraits(factory.Factory):
    class Meta:
        abstract = True

    # Admin trait
    is_admin = False
    role = 'user'

    # Verified trait
    is_verified = False
    verified_at = None

# factories/admin_user_factory.py
class AdminUserFactory(UserTraits):
    is_admin = True
    role = 'admin'

# factories/verified_user_factory.py
class VerifiedUserFactory(UserTraits):
    is_verified = True
    verified_at = factory.LazyAttribute(lambda o: fake.date_time_this_year())
```

### Composition

```python
# factories/complete_user_factory.py
class CompleteUserFactory(AdminUserFactory, VerifiedUserFactory):
    """Combines admin and verified traits"""
    pass

# Usage
admin_verified_user = CompleteUserFactory()
```

### State-Based Factories

```python
# factories/order_factory.py
class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    status = 'pending'
    total = factory.LazyAttribute(lambda o: sum(item.price for item in o.items))

class PendingOrderFactory(OrderFactory):
    status = 'pending'

class ShippedOrderFactory(OrderFactory):
    status = 'shipped'
    shipped_at = factory.LazyAttribute(lambda o: fake.date_time_this_year())

class DeliveredOrderFactory(OrderFactory):
    status = 'delivered'
    delivered_at = factory.LazyAttribute(lambda o: fake.date_time_this_year())
```

---

## Best Practices

### 1. Use Factories for Test Data

```python
# ✅ GOOD: Use factory
user = UserFactory.create()

# ❌ BAD: Hardcoded data
user = {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}
```

### 2. Use Faker for Realistic Data

```python
# ✅ GOOD: Use faker
email = fake.email()

# ❌ BAD: Fake email
email = 'test@example.com'
```

### 3. Use Sequences for Unique Data

```python
# ✅ GOOD: Use sequence
id = factory.Sequence(lambda n: n)

# ❌ BAD: Random ID
id = random.randint(1, 1000)
```

### 4. Use Lazy Attributes

```python
# ✅ GOOD: Lazy evaluation
email = factory.LazyAttribute(lambda o: f"{o.name.lower()}@example.com")

# ❌ BAD: Eager evaluation
email = fake.email()
```

### 5. Use Traits for Reusable States

```python
# ✅ GOOD: Use traits
admin_user = AdminUserFactory.create()

# ❌ BAD: Duplicate code
admin_user = UserFactory.create(is_admin=True, role='admin')
```

### 6. Clean Up After Tests

```python
@pytest.fixture(autouse=True)
def cleanup_database():
    yield
    # Cleanup
    db.session.query(User).delete()
    db.session.commit()
```

### 7. Use Batch Creation for Large Datasets

```python
# ✅ GOOD: Batch creation
users = UserFactory.create_batch(1000)

# ❌ BAD: Loop creation
for i in range(1000):
    user = UserFactory.create()
```

### 8. Use Relationships for Complex Data

```python
# ✅ GOOD: Use relationships
post = PostFactory(author=user)

# ❌ BAD: Manual relationships
post = PostFactory()
post.author_id = user.id
```

### 9. Keep Factories Simple

```python
# ✅ GOOD: Simple factory
class UserFactory(factory.Factory):
    name = factory.Faker('name')
    email = factory.Faker('email')

# ❌ BAD: Complex factory
class UserFactory(factory.Factory):
    name = factory.Faker('name')
    email = factory.Faker('email')
    profile = factory.SubFactory('ProfileFactory')
    settings = factory.SubFactory('SettingsFactory')
    posts = factory.RelatedFactoryList('PostFactory')
    # ... more complexity
```

### 10. Document Your Factories

```python
# ✅ GOOD: Documented factory
class UserFactory(factory.Factory):
    """Factory for creating test users"""
    class Meta:
        model = User

    name = factory.Faker('name')  # Full name
    email = factory.Faker('email')  # Email address
```

---

## Resources

- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [Fishery Documentation](https://fishery.dev/)
- [Faker Documentation](https://faker.readthedocs.io/)
- [@faker-js/faker](https://fakerjs.dev/)
- [Rosie](https://github.com/rosie/rosie)
